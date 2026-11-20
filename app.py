import streamlit as st
import pandas as pd

# Import semua fungsi dari folder modules/
from modules.ui_components import load_cyber_css, render_kpi_metrics
from modules.cleaning import clean_and_merge_kartu_stok
from modules.processing import process_hpp_data
from modules.talang import clean_and_merge_pindah_gudang, create_rekap_talang
from modules.export import generate_excel_download

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Data Control HPP", page_icon="🖥️", layout="wide")
load_cyber_css()

# --- INISIALISASI SESSION STATE (Memori Web) ---
if 'gabungan_kartu_stok' not in st.session_state:
    st.session_state['gabungan_kartu_stok'] = None
if 'master_talang' not in st.session_state:
    st.session_state['master_talang'] = None
if 'data_excel_siap' not in st.session_state:
    st.session_state['data_excel_siap'] = None
if 'metrik_data' not in st.session_state:
    st.session_state['metrik_data'] = None

# --- SIDEBAR & NAVIGASI ---
menu = st.sidebar.radio(
    "",
    ["Dashboard Utama", "Gabungkan File", "Cross Check HPP"],
    label_visibility="collapsed"
)

# --- MENU: DASHBOARD UTAMA ---
if menu == "Dashboard Utama":
    st.markdown("""
        <div class="custom-title-container">
            <h1 class="custom-title">🖥️ DATA CONTROL HPP (DC HPP)</h1>
            <p class="custom-subtitle">Sistem pengolahan data terpusat untuk mendeteksi fluktuasi Harga Pokok Penjualan (HPP)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("ℹ️ Silakan buka menu **Gabungkan File** di menu sebelah kiri untuk memulai proses penggabungan data kartu stok Anda.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    try:
        st.image("flowchart.jpg", use_container_width=True)
    except Exception as e:
        st.error("Gambar flowchart gagal dimuat. Pastikan nama file di GitHub sudah benar (flowchart.jpg).")

# --- MENU: GABUNGKAN FILE ---
elif menu == "Gabungkan File":
    st.markdown("""
        <div class="custom-title-container">
            <h1 class="custom-title" style="font-size: 2.2rem !important;">📂 GABUNGKAN DATA MASTER</h1>
            <p class="custom-subtitle">Pembersihan (data cleaning) dan penggabungan dataset kartu stok serta pindah gudang</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 1. Upload Wajib: Master Kartu Stok
    uploaded_files = st.file_uploader(
        "Import Data Master Kartu Stok (Wajib - Bisa lebih dari 1 file)", 
        type=['xlsx', 'xls'], 
        accept_multiple_files=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Upload Opsional: Master Data Pindah Gudang
    uploaded_pg_files = st.file_uploader(
        "Import Master Data Pindah Gudang / Talang (Opsional - Bisa lebih dari 1 file)", 
        type=['xlsx', 'xls'], 
        accept_multiple_files=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1 Tombol untuk menggabungkan Kartu Stok & Pindah Gudang (jika ada)
    col_btn_left, col_btn_mid, col_btn_right = st.columns([1, 1, 1])
    with col_btn_mid:
        tombol_gabung = st.button("🚀 GABUNG DATA", use_container_width=True)
        
    if tombol_gabung:
        if uploaded_files:
            with st.spinner("Sistem sedang membersihkan dan mengombinasikan file data..."):
                try:
                    # Proses Master Kartu Stok (Wajib)
                    df_hasil = clean_and_merge_kartu_stok(uploaded_files)
                    st.session_state['gabungan_kartu_stok'] = df_hasil
                    
                    # Reset hasil excel lama agar tidak tertukar dengan sesi sebelumnya
                    st.session_state['data_excel_siap'] = None
                    
                    # Proses Master Pindah Gudang (Opsional)
                    if uploaded_pg_files:
                        df_pg = clean_and_merge_pindah_gudang(uploaded_pg_files)
                        st.session_state['master_talang'] = df_pg
                        st.success(
                            f"✅ Berhasil! Master Kartu Stok ({len(df_hasil):,} baris) & "
                            f"Master Pindah Gudang Talang ({len(df_pg):,} baris) siap diproses."
                        )
                    else:
                        st.session_state['master_talang'] = None
                        st.success(
                            f"✅ Berhasil! Master Kartu Stok ({len(df_hasil):,} baris) siap diproses. "
                            f"(Tanpa data Pindah Gudang)."
                        )
                except Exception as e:
                    st.error(f"Gagal mengolah file: {e}")
        else:
            st.warning("Harap masukkan minimal 1 file Master Kartu Stok terlebih dahulu.")

# --- MENU: CROSS CHECK HPP ---
elif menu == "Cross Check HPP":
    st.markdown("""
        <div class="custom-title-container">
            <h1 class="custom-title" style="font-size: 2.2rem !important;">🔍 ANALISIS & CROSS CHECK HPP</h1>
            <p class="custom-subtitle">Proses mapping otomatis dan ekstraksi deviasi lonjakan harga terhadap template laporan</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Info status ketersediaan data di memori
    data_ready = st.session_state['gabungan_kartu_stok'] is not None
    talang_ready = st.session_state['master_talang'] is not None
    
    if data_ready:
        if talang_ready:
            st.info("✅ Data Siap: Master Kartu Stok + Master Pindah Gudang (Talang) akan diproses (Output 5 Sheet).")
        else:
            st.info("✅ Data Siap: Master Kartu Stok saja yang akan diproses (Output 3 Sheet).")
            
    template_file = st.file_uploader("Import File Template Laporan yang akan diproses", type=['xlsx', 'xls'])
    
    if not data_ready:
        st.error("⚠️ Proses ditolak: Data Gabungan Kartu Stok belum siap. Selesaikan menu 'Gabungkan File' terlebih dahulu.")
    elif template_file is not None:
        
        col_btn_left, col_btn_mid, col_btn_right = st.columns([1, 1, 1])
        with col_btn_mid:
            tombol_proses = st.button("⚙️ PROSES ANALISA HPP", use_container_width=True)
            
        if tombol_proses:
            with st.spinner("Mesin HPP: Menganalisa deviasi dan menyusun laporan terperinci..."):
                try:
                    df_gabung = st.session_state['gabungan_kartu_stok']
                    df_lap, df_cek, df_adj = process_hpp_data(df_gabung, template_file)
                    
                    # Ambil metrik KPI
                    max_naik = df_cek['Persentase Selisih (%)'].max()
                    max_turun = df_cek['Persentase Selisih (%)'].min()
                    
                    st.session_state['metrik_data'] = {
                        'total': len(df_cek),
                        'naik': (max_naik * 100) if pd.notna(max_naik) else 0,
                        'turun': (max_turun * 100) if pd.notna(max_turun) else 0
                    }
                    
                    # Proses Rekap Talang secara opsional jika datanya ada
                    df_master_talang = st.session_state['master_talang']
                    df_rekap_talang = None
                    if df_master_talang is not None:
                        df_rekap_talang = create_rekap_talang(df_master_talang)
                    
                    # Generate Excel (3 sheet atau 5 sheet secara otomatis)
                    st.session_state['data_excel_siap'] = generate_excel_download(
                        df_lap, df_cek, df_adj, df_master_talang, df_rekap_talang
                    )
                    st.success("🎉 Analisis selesai! Output data HPP sekarang siap untuk diunduh.")
                    
                except Exception as e:
                    st.error(f"Gagal memproses data: {e}")
        
        # Tampilkan Metrik dan Tombol Download jika data sudah diproses
        if st.session_state['data_excel_siap'] is not None:
            st.markdown("---")
            
            metrik = st.session_state['metrik_data']
            render_kpi_metrics(metrik['total'], round(metrik['naik'], 2), round(metrik['turun'], 2))
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_dl_left, col_dl_mid, col_dl_right = st.columns([1, 1, 1])
            with col_dl_mid:
                st.download_button(
                    label="⬇️ DOWNLOAD OUTPUT EXCEL",
                    data=st.session_state['data_excel_siap'],
                    file_name="Laporan_Analisa_HPP.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
