import pandas as pd
import streamlit as st

def clean_and_merge_kartu_stok(uploaded_files):
    """
    Fungsi untuk membersihkan dan menggabungkan beberapa file Master Kartu Stok.
    """
    list_dataframe = []
    
    for file in uploaded_files:
        # 1. Membaca Excel dengan melewati (skip) 5 baris teratas (karena merupakan judul)
        df = pd.read_excel(file, skiprows=5)
        
        # 2. Menghapus 4 baris paling bawah (baris total)
        df = df.iloc[:-4]
        
        # 3. Menghapus baris yang jika di semua kolomnya kosong
        df = df.dropna(how='all')
        
        # 4. Mencari kolom tanggal & Memastikan formatnya adalah Datetime sejati
        # Kita menggunakan deteksi otomatis jika nama kolomnya mengandung kata 'tanggal' atau 'date'
        col_tanggal = [col for col in df.columns if 'tanggal' in col.lower() or 'date' in col.lower()]
        
        if col_tanggal:
            nama_kolom = col_tanggal[0] # Mengambil nama kolom yang ditemukan
            # Konversi paksa ke datetime agar urutan waktunya presisi sampai ke detik
            df[nama_kolom] = pd.to_datetime(df[nama_kolom], errors='coerce')
            
            # Mengurutkan data berdasarkan tanggal kronologis (dari terlama ke terbaru)
            df = df.sort_values(by=nama_kolom)
        
        # Masukkan ke daftar sementara
        list_dataframe.append(df)
    
    # 5. Menggabungkan semua file 
    # (Fungsi pandas concat otomatis hanya mengambil 1 header/judul kolom)
    df_gabungan = pd.concat(list_dataframe, ignore_index=True)
    
    # 6. Menghapus kolom yang tidak diperlukan
    kolom_dihapus = ["Line Total", "Transactional Qty", "Transactional Unit", "Customer"]
    
    # Validasi: Hanya hapus jika nama kolom tersebut benar-benar ada di dalam data
    kolom_ada = [col for col in kolom_dihapus if col in df_gabungan.columns]
    df_gabungan = df_gabungan.drop(columns=kolom_ada)
    
    return df_gabungan
