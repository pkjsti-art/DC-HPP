import streamlit as st

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
st.sidebar.title("Main Menu 🌐")
menu = st.sidebar.radio(
    "Pilih Modul Sistem:",
    ["Dashboard Utama", "Gabungkan File", "Cross Check HPP"]
)

# --- MENU: DASHBOARD UTAMA ---
if menu == "Dashboard Utama":
    st.title("🖥️ Data Control HPP (DC HPP)")
    st.write("Sistem pengolahan data terpusat untuk mendeteksi fluktuasi Harga Pokok Penjualan (HPP).")
    st.info("Silakan buka menu **Gabungkan File** di sebelah kiri untuk memulai proses.")

# --- MENU: GABUNGKAN FILE ---
elif menu == "Gabungkan File":
    st.title("📂 Gabungkan Data Kartu Stok")
    uploaded_files = st.file_uploader(
        "Import Data Master Kartu Stok (Bisa lebih dari 1 file)", 
        type=['xlsx', 'xls'], 
        accept_multiple_files=True
    )
    
    if st.button("🚀 Gabung Data"):
        if uploaded_files:
            # Menjalankan animasi loading saat sistem bekerja
            with st.spinner("Terminal: Membersihkan dan menggabungkan data..."):
                try:
                    # Memanggil fungsi pembersihan dan menyimpannya di memori
                    df_hasil = clean_and_merge_kartu_stok(uploaded_files)
                    st.session_state['gabungan_kartu_stok'] = df_hasil
                    st.success(f"✅ Berhasil! {len(df_hasil)} baris data berhasil digabungkan.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat menggabungkan data: {e}")
        else:
            st.warning("Harap upload file terlebih dahulu.")

# --- MENU: CROSS CHECK HPP ---
elif menu == "Cross Check HPP":
    st.title("🔍 Cross Check & Analisis HPP")
    template_file = st.file_uploader("Import File Template Laporan", type=['xlsx', 'xls'])
    
    data_ready = st.session_state['gabungan_kartu_stok'] is not None
    
    if not data_ready:
        st.error("⚠️ Data Master Kartu Stok belum digabungkan. Silakan ke menu 'Gabungkan File'.")
    elif template_file is not None:
        
        # Jika tombol Proses diklik
        if st.button("⚙️ Proses Data HPP"):
            with st.spinner("Terminal: Menganalisa fluktuasi HPP & menyusun laporan..."):
                try:
                    df_gabung = st.session_state['gabungan_kartu_stok']
                    
                    # 1. Jalankan proses kalkulasi
                    df_lap, df_cek, df_adj = process_hpp_data(df_gabung, template_file)
                    
                    # 2. Ambil metrik untuk KPI Card
                    max_naik = df_cek['Persentase Selisih (%)'].max()
                    max_turun = df_cek['Persentase Selisih (%)'].min()
                    
                    # Simpan metrik ke state
                    st.session_state['metrik_data'] = {
                        'total': len(df_cek),
                        'naik': max_naik if pd.notna(max_naik) else 0,
                        'turun': max_turun if pd.notna(max_turun) else 0
                    }
                    
                    # 3. Generate file excel di background dan simpan ke state
                    st.session_state['data_excel_siap'] = generate_excel_download(df_lap, df_cek, df_adj)
                    st.success("✅ Analisa selesai! Data siap diunduh.")
                    
                except Exception as e:
                    st.error(f"Gagal memproses data: {e}")
        
        # Tampilkan Metrik dan Tombol Download jika data sudah diproses
        if st.session_state['data_excel_siap'] is not None:
            st.markdown("---")
            
            # Tampilkan KPI Dashboard
            metrik = st.session_state['metrik_data']
            render_kpi_metrics(metrik['total'], round(metrik['naik'], 2), round(metrik['turun'], 2))
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tombol unduh khusus Streamlit yang tidak mereset halaman
            st.download_button(
                label="⬇️ Download Output Hasil (Excel)",
                data=st.session_state['data_excel_siap'],
                file_name="Hasil_CrossCheck_HPP.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
