import streamlit as st
from modules.ui_components import load_cyber_css

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Data Control HPP",
    page_icon="🖥️",
    layout="wide"
)

# Load tema Cyber
load_cyber_css()

# --- INISIALISASI SESSION STATE ---
# Menyimpan file gabungan agar tidak hilang saat pindah menu
if 'gabungan_kartu_stok' not in st.session_state:
    st.session_state['gabungan_kartu_stok'] = None
if 'hasil_crosscheck' not in st.session_state:
    st.session_state['hasil_crosscheck'] = None

# --- SIDEBAR & NAVIGASI ---
st.sidebar.title("Main Menu 🌐")
menu = st.sidebar.radio(
    "Pilih Modul Sistem:",
    ["Dashboard Utama", "Gabungkan File", "Cross Check HPP"]
)

# --- MENU: DASHBOARD UTAMA ---
if menu == "Dashboard Utama":
    st.title("🖥️ Data Control HPP (DC HPP)")
    st.write("Sistem pengolahan data terpusat untuk mendeteksi fluktuasi Harga Pokok Penjualan (HPP) berdasarkan riwayat Master Kartu Stok.")
    
    st.info("Silakan buka menu **Gabungkan File** di sebelah kiri untuk memulai proses pembersihan dan penggabungan data kartu stok.")

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
            # NANTI KITA PANGGIL FUNGSI DARI modules.cleaning.py DI SINI
            st.warning("Fungsi Cleaning & Penggabungan sedang disiapkan...")
            # Simulasi berhasil
            # st.session_state['gabungan_kartu_stok'] = df_hasil_gabung
        else:
            st.error("Harap upload minimal 1 file Master Kartu Stok terlebih dahulu.")

# --- MENU: CROSS CHECK HPP ---
elif menu == "Cross Check HPP":
    st.title("🔍 Cross Check & Analisis HPP")
    
    template_file = st.file_uploader(
        "Import File Template Laporan", 
        type=['xlsx', 'xls']
    )
    
    # Cek kesiapan data
    data_ready = st.session_state['gabungan_kartu_stok'] is not None
    
    if not data_ready:
        st.error("⚠️ Data Master Kartu Stok belum digabungkan. Silakan proses di menu 'Gabungkan File' terlebih dahulu.")
    elif template_file is None:
        st.info("ℹ️ File Master Kartu Stok sudah siap. Silakan upload Template Laporan untuk memulai.")
    else:
        st.success("✅ File Gabungan dan Template Laporan siap diproses.")
        
        if st.button("⚙️ Proses Data"):
            # NANTI KITA PANGGIL FUNGSI DARI modules.processing.py DI SINI
            st.warning("Mesin Kalkulasi & Processing sedang disiapkan...")
