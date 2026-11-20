import pandas as pd

def clean_and_merge_pindah_gudang(uploaded_files):
    """
    Membersihkan dan menggabungkan file Master Data Pindah Gudang:
    - Hapus 3 baris teratas per file
    - Gabung semua file dengan 1 header
    - Filter Status == 'active'
    - Filter Keterangan mengandung kata 'TALANG'
    - Render ulang kolom No urut dari 1
    """
    list_df = []
    
    for file in uploaded_files:
        df = pd.read_excel(file, skiprows=3)
        df = df.dropna(how='all')
        df.columns = [str(col).strip() for col in df.columns]
        list_df.append(df)
        
    df_gabungan = pd.concat(list_df, ignore_index=True)
    
    # Deteksi nama kolom secara aman (case-insensitive)
    col_status = [col for col in df_gabungan.columns if col.lower() == 'status'][0]
    col_ket = [col for col in df_gabungan.columns if col.lower() == 'keterangan'][0]
    col_masuk = [col for col in df_gabungan.columns if col.lower() == 'masuk'][0]
    
    # Filter Status == 'active' & Keterangan mengandung 'TALANG'
    df_gabungan = df_gabungan[
        df_gabungan[col_status].astype(str).str.strip().str.lower() == 'active'
    ]
    df_gabungan = df_gabungan[
        df_gabungan[col_ket].astype(str).str.contains('TALANG', case=False, na=False)
    ]
    
    # Pastikan kolom Masuk bertipe angka murni
    df_gabungan[col_masuk] = pd.to_numeric(df_gabungan[col_masuk], errors='coerce').fillna(0)
    df_gabungan = df_gabungan.reset_index(drop=True)
    
    # Render ulang kolom 'No' urut dari 1
    no_cols = [col for col in df_gabungan.columns if col.lower() == 'no']
    if no_cols:
        df_gabungan[no_cols[0]] = range(1, len(df_gabungan) + 1)
    
    return df_gabungan


def create_rekap_talang(df_master_talang):
    """
    Merekap Kode Variant dan Nama Variant yang unik,
    serta menjumlahkan kolom Masuk menjadi TOTAL PG (GR).
    """
    col_kode = [col for col in df_master_talang.columns if col.lower() == 'kode variant'][0]
    col_nama = [col for col in df_master_talang.columns if col.lower() == 'nama variant'][0]
    col_masuk = [col for col in df_master_talang.columns if col.lower() == 'masuk'][0]
    
    df_rekap = (
        df_master_talang
        .groupby([col_kode, col_nama], as_index=False, sort=False)[col_masuk]
        .sum()
    )
    
    df_rekap.columns = ['KODE VARIANT', 'NAMA VARIANT', 'TOTAL PG (GR)']
    
    return df_rekap
