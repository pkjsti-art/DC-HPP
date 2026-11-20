import pandas as pd

def clean_and_merge_mb_to(uploaded_files):
    """
    Membersihkan dan menggabungkan file Master MB TO:
    - Header langsung di baris 1
    - Gabung semua file dengan 1 header
    - Filter Gudang == 'Gudang Mesin Dyeing'
    - Filter Helper TO == 'TO'
    """
    list_df = []
    
    for file in uploaded_files:
        df = pd.read_excel(file)
        df = df.dropna(how='all')
        df.columns = [str(col).strip() for col in df.columns]
        list_df.append(df)
        
    df_gabungan = pd.concat(list_df, ignore_index=True)
    
    # Deteksi nama kolom secara aman (case-insensitive)
    col_gudang = [col for col in df_gabungan.columns if col.lower() == 'gudang'][0]
    col_helper = [col for col in df_gabungan.columns if col.lower() == 'helper to'][0]
    
    # Filter Gudang == 'Gudang Mesin Dyeing' dan Helper TO == 'TO'
    df_clean = df_gabungan[
        (df_gabungan[col_gudang].astype(str).str.strip().str.lower() == 'gudang mesin dyeing') &
        (df_gabungan[col_helper].astype(str).str.strip().str.upper() == 'TO')
    ]
    
    return df_clean.reset_index(drop=True)


def add_jumlah_to_to_laporan(df_laporan, df_mb_to):
    """
    Menambahkan kolom 'Jumlah TO' di sebelah kanan kolom Indikasi Faktor pada sheet Laporan.
    Mencocokkan VARIANT CODE dengan Kode Barang Jadi, lalu menghitung jumlah Kode yang unik.
    """
    df_lap = df_laporan.copy()
    
    col_variant_lap = [col for col in df_lap.columns if 'variant code' in col.lower()][0]
    col_kbj = [col for col in df_mb_to.columns if col.lower() == 'kode barang jadi'][0]
    col_kode = [col for col in df_mb_to.columns if col.lower() == 'kode'][0]
    
    # Normalisasi key pencocokan (hapus spasi & huruf kapital)
    df_lap['_Variant_Key'] = df_lap[col_variant_lap].astype(str).apply(lambda x: x.replace(" ", "").upper())
    
    if not df_mb_to.empty:
        df_to_temp = df_mb_to.copy()
        df_to_temp['_Variant_Key'] = df_to_temp[col_kbj].astype(str).apply(lambda x: x.replace(" ", "").upper())
        
        # Hitung jumlah 'Kode' unik per 'Kode Barang Jadi'
        to_counts = df_to_temp.groupby('_Variant_Key')[col_kode].nunique().to_dict()
    else:
        to_counts = {}
        
    # Map hasil hitungan ke Laporan dengan format "0x", "1x", dst.
    df_lap['Jumlah TO'] = df_lap['_Variant_Key'].map(lambda k: f"{to_counts.get(k, 0)}x")
    
    # Hapus kolom bantuan
    df_lap = df_lap.drop(columns=['_Variant_Key'])
    
    return df_lap
