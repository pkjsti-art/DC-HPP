import pandas as pd
import numpy as np

def process_hpp_data(df_gabungan, template_file):
    """
    Fungsi untuk mengecek fluktuasi harga antar baris di varian yang sama,
    dan menuliskan narasinya ke dalam Template Laporan.
    """
    
    # 1. PENCARIAN KOLOM SPESIFIK
    # Di Master: Cari kolom yang namanya PERSIS 'variant'
    col_variant = [col for col in df_gabungan.columns if col.strip().lower() == 'variant'][0]
    col_price = [col for col in df_gabungan.columns if 'price per unit' in col.lower()][0]
    col_desc = [col for col in df_gabungan.columns if 'deskripsi' in col.lower() or 'desc' in col.lower()][0]
    col_wh = [col for col in df_gabungan.columns if 'wh label' in col.lower() or 'wh' in col.lower()][0]
    
    # ========================================================
    # TAHAP 1: PERHITUNGAN BARIS (SELISIH & PERSENTASE)
    # ========================================================
    
    df_gabungan = df_gabungan.sort_values(by=[col_variant])
    
    df_gabungan['Harga_Atas'] = df_gabungan.groupby(col_variant)[col_price].shift(1)
    df_gabungan['Selisih (GR)'] = df_gabungan[col_price] - df_gabungan['Harga_Atas']
    
    def hitung_persentase(row):
        bawah = row[col_price]
        atas = row['Harga_Atas']
        
        if pd.isna(atas): 
            return None 
            
        if atas == 0:
            return 1.0 if bawah > 0 else 0.0 # 1.0 = 100% di Excel
            
        return (bawah - atas) / atas
        
    df_gabungan['Persentase Selisih (%)'] = df_gabungan.apply(hitung_persentase, axis=1)
    
    # ========================================================
    # TAHAP 2: MAPPING & PERAKITAN NARASI TEMPLATE LAPORAN
    # ========================================================
    
    df_template = pd.read_excel(template_file)
    
    # Di Template: Cari kolom yang MENGANDUNG kata 'variant code'
    col_variant_template = [col for col in df_template.columns if 'variant code' in col.lower()][0]
    
    if "Indikasi Faktor Persentase Naik Turun HPP" not in df_template.columns:
        df_template["Indikasi Faktor Persentase Naik Turun HPP"] = ""
        
    # Memotong sebelum strip "-", menghapus SEMUA spasi, dan menjadikan huruf kapital
    df_gabungan['Variant_Key'] = df_gabungan[col_variant].astype(str).apply(lambda x: x.split('-')[0].replace(" ", "").upper())
    df_template['Variant_Key'] = df_template[col_variant_template].astype(str).apply(lambda x: str(x).replace(" ", "").upper())
    
    for variant_map in df_gabungan['Variant_Key'].unique():
        df_kelompok = df_gabungan[df_gabungan['Variant_Key'] == variant_map]
        
        if df_kelompok.empty or df_kelompok['Persentase Selisih (%)'].isna().all():
            continue
            
        # FILTER LOGIKA: Abaikan 0%, pisahkan murni yang Naik (>0) dan Turun (<0)
        df_naik = df_kelompok[df_kelompok['Persentase Selisih (%)'] > 0]
        df_turun = df_kelompok[df_kelompok['Persentase Selisih (%)'] < 0]
        
        narasi = ""
        
        # Ambil SATU yang paling NAIK ekstrim (jika ada)
        if not df_naik.empty:
            idx_max = df_naik['Persentase Selisih (%)'].idxmax()
            val_max = df_naik.loc[idx_max, 'Persentase Selisih (%)']
            desc_max = df_naik.loc[idx_max, col_desc]
            wh_max = df_naik.loc[idx_max, col_wh]
            narasi += f"ADA KENAIKAN SIGNIFIKAN PADA {desc_max} DI {wh_max} SEBESAR {(val_max * 100):.2f}%."
            
        # Ambil SATU yang paling TURUN ekstrim (jika ada)
        if not df_turun.empty:
            idx_min = df_turun['Persentase Selisih (%)'].idxmin()
            val_min = df_turun.loc[idx_min, 'Persentase Selisih (%)']
            desc_min = df_turun.loc[idx_min, col_desc]
            wh_min = df_turun.loc[idx_min, col_wh]
            narasi += f" DAN PENURUNAN PADA {desc_min} DI {wh_min} SEBESAR {(abs(val_min) * 100):.2f}%."
            
        if narasi:
            # Merapikan kalimat jika kebetulan HANYA ada penurunan (tidak ada kenaikan)
            if narasi.startswith(" DAN "):
                narasi = narasi.replace(" DAN ", "ADA ", 1)
                
            # Masukkan ke Template
            df_template.loc[df_template['Variant_Key'] == variant_map, "Indikasi Faktor Persentase Naik Turun HPP"] = narasi.strip()
            
    # ========================================================
    # TAHAP 3: FILTER DATA 'ADJ' UNTUK REKAPITULASI
    # ========================================================
    
    df_adj = df_gabungan[df_gabungan[col_desc].astype(str).str.contains('ADJ', case=False, na=False)]
    
    # Hapus kolom bantuan sistem (Variant_Key dan Harga_Atas) agar output bersih
    df_template = df_template.drop(columns=['Variant_Key'])
    df_gabungan = df_gabungan.drop(columns=['Harga_Atas', 'Variant_Key'])
    
    return df_template, df_gabungan, df_adj
