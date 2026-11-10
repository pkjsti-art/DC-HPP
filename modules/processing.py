import pandas as pd
import numpy as np

def process_hpp_data(df_gabungan, template_file):
    # 1. PENCARIAN KOLOM SPESIFIK YANG LEBIH AKURAT
    col_variant = [col for col in df_gabungan.columns if col.strip().lower() == 'variant'][0]
    col_price = [col for col in df_gabungan.columns if 'price per unit' in col.lower()][0]
    col_desc = [col for col in df_gabungan.columns if 'deskripsi' in col.lower() or 'desc' in col.lower()][0]
    col_wh = [col for col in df_gabungan.columns if 'wh label' in col.lower() or ('wh' in col.lower() and 'label' in col.lower())][0]
    
    # ========================================================
    # TAHAP 1: PERHITUNGAN BARIS
    # ========================================================
    df_gabungan = df_gabungan.sort_values(by=[col_variant])
    df_gabungan['Harga_Atas'] = df_gabungan.groupby(col_variant)[col_price].shift(1)
    df_gabungan['Selisih (GR)'] = df_gabungan[col_price] - df_gabungan['Harga_Atas']
    
    def hitung_persentase(row):
        bawah = row[col_price]
        atas = row['Harga_Atas']
        if pd.isna(atas): return None 
        if atas == 0: return 1.0 if bawah > 0 else 0.0
        return (bawah - atas) / atas
        
    df_gabungan['Persentase Selisih (%)'] = df_gabungan.apply(hitung_persentase, axis=1)
    
    # ========================================================
    # TAHAP 2: MAPPING & PERAKITAN NARASI
    # ========================================================
    df_template = pd.read_excel(template_file)
    col_variant_template = [col for col in df_template.columns if 'variant code' in col.lower()][0]
    
    if "Indikasi Faktor Persentase Naik Turun HPP" not in df_template.columns:
        df_template["Indikasi Faktor Persentase Naik Turun HPP"] = ""
        
    df_gabungan['Variant_Key'] = df_gabungan[col_variant].astype(str).apply(
        lambda x: x.replace('—', '-').replace('–', '-').split('-')[0].replace(" ", "").upper()
    )
    df_template['Variant_Key'] = df_template[col_variant_template].astype(str).apply(
        lambda x: str(x).replace(" ", "").upper()
    )
    
    for variant_map in df_gabungan['Variant_Key'].unique():
        df_kelompok = df_gabungan[df_gabungan['Variant_Key'] == variant_map]
        
        if df_kelompok.empty or df_kelompok['Persentase Selisih (%)'].isna().all():
            continue
            
        df_naik = df_kelompok[df_kelompok['Persentase Selisih (%)'] > 0]
        df_turun = df_kelompok[df_kelompok['Persentase Selisih (%)'] < 0]
        
        narasi_parts = []
        
        # Ekstraksi Kenaikan menggunakan simbol ▲ standar (tanpa emoji warna)
        if not df_naik.empty:
            idx_max = df_naik['Persentase Selisih (%)'].idxmax()
            val_max = df_naik.loc[idx_max, 'Persentase Selisih (%)']
            desc_max = df_naik.loc[idx_max, col_desc]
            wh_max = df_naik.loc[idx_max, col_wh]
            narasi_parts.append(f"▲ NAIK {(val_max * 100):.2f}% Di {wh_max} -> {desc_max}")
            
        # Ekstraksi Penurunan menggunakan simbol ▼ standar (tanpa emoji warna)
        if not df_turun.empty:
            idx_min = df_turun['Persentase Selisih (%)'].idxmin()
            val_min = df_turun.loc[idx_min, 'Persentase Selisih (%)']
            desc_min = df_turun.loc[idx_min, col_desc]
            wh_min = df_turun.loc[idx_min, col_wh]
            narasi_parts.append(f"▼ TURUN {(abs(val_min) * 100):.2f}% Di {wh_min} -> {desc_min}")
            
        if narasi_parts:
            narasi_final = "\n".join(narasi_parts)
            df_template.loc[df_template['Variant_Key'] == variant_map, "Indikasi Faktor Persentase Naik Turun HPP"] = narasi_final
            
    # ========================================================
    # TAHAP 3: FILTER DATA 'ADJ'
    # ========================================================
    df_adj = df_gabungan[df_gabungan[col_desc].astype(str).str.contains('ADJ', case=False, na=False)]
    df_template = df_template.drop(columns=['Variant_Key'])
    df_gabungan = df_gabungan.drop(columns=['Harga_Atas', 'Variant_Key'])
    
    return df_template, df_gabungan, df_adj
