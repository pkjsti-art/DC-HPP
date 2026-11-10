import streamlit as st
import pandas as pd

# Import semua fungsi dari folder modules/
from modules.ui_components import load_cyber_css, render_kpi_metrics
from modules.cleaning import clean_and_merge_kartu_stok
from modules.processing import process_hpp_data
from modules.export import generate_excel_download

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Data Control HPP", page_icon="🖥️", layout="wide")
load_cyber_css()

# --- INISIALISASI SESSION STATE (Memori Web) ---
if 'gabungan_kartu_stok' not in st.session_state:
    st.session_state['gabungan_kartu_stok'] = None
if 'data_excel_siap' not in st.session_state:
    st.session_state['data_excel_siap'] = None
if 'metrik_data' not in st.session_state:
    st.session_state['metrik_data'] = None

# --- SIDEBAR & NAVIGASI ---
st.sidebar.markdown(
    "<h2 style='text-align: center; font-family: Space Grotesk;'>CONTROL PANEL ⚙️</h2>", 
    unsafe_allow_html=True
)
menu = st.sidebar.radio(
    "Navigasi Modul:",
    ["Dashboard Utama", "Gabungkan File", "Cross Check HPP"]
)

# --- MENU: DASHBOARD UTAMA ---
if menu == "Dashboard Utama":
    # Membuat Judul Terpusat (Center) dengan HTML & CSS Custom
    st.markdown("""
        <div class="custom-title-container">
            <h1 class="custom-title">🖥️ DATA CONTROL HPP (DC HPP)</h1>
            <p class="custom-subtitle">Sistem pengolahan data terpusat untuk mendeteksi fluktuasi Harga Pokok Penjualan (HPP)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("ℹ️ Silakan buka menu **Gabungkan File** di menu sebelah kiri untuk memulai proses penggabungan data kartu stok Anda.")
    
    st.markdown("<br>", unsafe_allow_html=True) # Jeda ruang
    
    # Menampilkan gambar flowchart
    try:
        st.image("flowchart.jpg", use_container_width=True)
    except Exception as e:
        st.error("Gambar flowchart gagal dimuat. Pastikan nama file di GitHub sudah benar (flowchart.jpg).")

# --- MENU: GABUNGKAN FILE ---
elif menu == "Gabungkan File":
    st.markdown("""
        <div class="custom-title-container">
            <h1 class="custom-title" style="font-size: 2.2rem !important;">📂 GABUNGKAN DATA KARTU STOK</h1>
            <p class="custom-subtitle">Pembersihan (data cleaning) dan penggabungan dataset kartu stok multi-gudang</p>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Import Data Master Kartu Stok (Bisa lebih dari 1 file)", 
        type=['xlsx', 'xls'], 
        accept_multiple_files=True
    )
    
    # Memusatkan tombol di bawah file uploader
    col_btn_left, col_btn_mid, col_btn_right = st.columns([1, 1, 1])
    with col_btn_mid:
        tombol_gabung = st.button("🚀 GABUNG DATA STOK", use_container_width=True)
        
    if tombol_gabung:
        if uploaded_files:
            with st.spinner("Sistem sedang membersihkan dan mengombinasikan file data..."):
                try:
                    df_hasil = clean_and_merge_kartu_stok(uploaded_files)
                    st.session_state['gabungan_kartu_stok'] = df_hasil
                    st.success(f"✅ Pembersihan & Penggabungan Berhasil! {len(df_hasil):,} baris data terintegrasi ke dalam memori sistem.")
                except Exception as e:
                    st.error(f"Gagal mengolah file: {e}")
        else:
            st.warning("Harap masukkan atau drag & drop sekurang-kurangnya 1 file data kartu stok.")

# --- MENU: CROSS CHECK HPP ---
elif menu == "Cross Check HPP":
    st.markdown("""
        <div class="custom-title-container">
            <h1 class="custom-title" style="font-size: 2.2rem !important;">🔍 ANALISIS & CROSS CHECK HPP</h1>
            <p class="custom-subtitle">Proses mapping otomatis dan ekstraksi deviasi lonjakan harga terhadap template laporan</p>
        </div>
    """, unsafe_allow_html=True)
    
    template_file = st.file_uploader("Import File Template Laporan yang akan diproses", type=['xlsx', 'xls'])
    
    data_ready = st.session_state['gabungan_kartu_stok'] is not None
    
    if not data_ready:
        st.error("⚠️ Proses ditolak: Data Gabungan Kartu Stok belum siap. Selesaikan menu 'Gabungkan File' terlebih dahulu.")
    elif template_file is not None:
        
        # Tombol Proses diposisikan di tengah agar seimbang
        col_btn_left, col_btn_mid, col_btn_right = st.columns([1, 1, 1])
        with col_btn_mid:
            tombol_proses = st.button("⚙️ PROSES ANALISA HPP", use_container_width=True)
            
        if tombol_proses:
            with st.spinner("Mesin HPP: Menganalisa deviasi dan menyusun laporan terperinci..."):
                try:
                    df_gabung = st.session_state['gabungan_kartu_stok']
                    
                    df_lap, df_cek, df_adj = process_hpp_data(df_gabung, template_file)
                    
                    # Ambil metrik (Kalikan 100 hanya untuk tampilan label dashboard)
                    max_naik = df_cek['Persentase Selisih (%)'].max()
                    max_turun = df_cek['Persentase Selisih (%)'].min()
                    
                    st.session_state['metrik_data'] = {
                        'total': len(df_cek),
                        'naik': (max_naik * 100) if pd.notna(max_naik) else 0,
                        'turun': (max_turun * 100) if pd.notna(max_turun) else 0
                    }
                    
                    st.session_state['data_excel_siap'] = generate_excel_download(df_lap, df_cek, df_adj)
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
