import pandas as pd
import numpy as np

def process_hpp_data(df_gabungan, template_file):
    """
    Fungsi untuk mengecek fluktuasi harga antar baris di varian yang sama,
    dan menuliskan narasinya ke dalam Template Laporan.
    """
    
    # --- DETEKSI OTOMATIS NAMA KOLOM ---
    # Bertujuan agar sistem tidak error jika ada sedikit perbedaan spasi pada nama kolom dari ERP
    col_variant = [col for col in df_gabungan.columns if 'variant' in col.lower()][0]
    col_price = [col for col in df_gabungan.columns if 'price per unit' in col.lower()][0]
    col_desc = [col for col in df_gabungan.columns if 'deskripsi' in col.lower() or 'desc' in col.lower()][0]
    col_wh = [col for col in df_gabungan.columns if 'wh label' in col.lower() or 'wh' in col.lower()][0]
    
    # ========================================================
    # TAHAP 1: PERHITUNGAN BARIS (SELISIH & PERSENTASE)
    # ========================================================
    
    # Mengurutkan berdasarkan Kode Variant untuk mengelompokkan data yang sama
    df_gabungan = df_gabungan.sort_values(by=[col_variant])
    
    # Membuat kolom bantu "Harga Atas" dengan cara menggeser (shift) 1 baris ke bawah
    # Penggeseran dilakukan "per kelompok varian" agar harga varian A tidak tercampur varian B
    df_gabungan['Harga_Atas'] = df_gabungan.groupby(col_variant)[col_price].shift(1)
    
    # Rumus Selisih: Baris bawah (saat ini) dikurangi baris atas (sebelumnya)
    df_gabungan['Selisih (GR)'] = df_gabungan[col_price] - df_gabungan['Harga_Atas']
    
    # Fungsi khusus menangani perhitungan persentase dan zero division (pembagi 0)
    def hitung_persentase(row):
        bawah = row[col_price]
        atas = row['Harga_Atas']
        
        if pd.isna(atas): 
            return None # Baris pertama pada suatu varian tidak punya pembanding
            
        if atas == 0:
            return 100.0 if bawah > 0 else 0.0 # Logika Inovasi: Atas 0, Bawah >0 = 100%
            
        return ((bawah - atas) / atas) * 100
        
    df_gabungan['Persentase Selisih (%)'] = df_gabungan.apply(hitung_persentase, axis=1)
    
    
    # ========================================================
    # TAHAP 2: MAPPING & PERAKITAN NARASI TEMPLATE LAPORAN
    # ========================================================
    
    df_template = pd.read_excel(template_file)
    col_variant_template = [col for col in df_template.columns if 'variant' in col.lower()][0]
    
    # Siapkan kolom baru di template laporan
    if "Indikasi Faktor Persentase Naik Turun HPP" not in df_template.columns:
        df_template["Indikasi Faktor Persentase Naik Turun HPP"] = ""
        
    # Memotong karakter Variant (Ambil sebelum strip "-", hapus spasi tersembunyi)
    df_gabungan['Variant_Key'] = df_gabungan[col_variant].astype(str).apply(lambda x: x.split('-')[0].strip())
    df_template['Variant_Key'] = df_template[col_variant_template].astype(str).apply(lambda x: str(x).strip())
    
    # Eksekusi pencarian nilai ekstrem di setiap kelompok varian
    for variant_map in df_gabungan['Variant_Key'].unique():
        df_kelompok = df_gabungan[df_gabungan['Variant_Key'] == variant_map]
        
        # Lewati jika tidak ada persentase untuk dianalisa
        if df_kelompok.empty or df_kelompok['Persentase Selisih (%)'].isna().all():
            continue
            
        # Mencari letak baris (index) yang naik tertinggi dan turun terdalam
        idx_max = df_kelompok['Persentase Selisih (%)'].idxmax()
        idx_min = df_kelompok['Persentase Selisih (%)'].idxmin()
        
        val_max = df_kelompok.loc[idx_max, 'Persentase Selisih (%)']
        val_min = df_kelompok.loc[idx_min, 'Persentase Selisih (%)']
        
        narasi = ""
        
        # Jika nilai maksimalnya naik (> 0)
        if pd.notna(val_max) and val_max > 0:
            desc_max = df_kelompok.loc[idx_max, col_desc]
            wh_max = df_kelompok.loc[idx_max, col_wh]
            narasi += f"ADA KENAIKAN SIGNIFIKAN PADA {desc_max} DI {wh_max} SEBESAR {val_max:.2f}%."
            
        # Jika nilai minimalnya turun (< 0)
        if pd.notna(val_min) and val_min < 0:
            desc_min = df_kelompok.loc[idx_min, col_desc]
            wh_min = df_kelompok.loc[idx_min, col_wh]
            # abs() digunakan untuk menghilangkan tanda minus pada narasi teks
            narasi += f" DAN PENURUNAN PADA {desc_min} DI {wh_min} SEBESAR {abs(val_min):.2f}%."
            
        # Memasukkan teks narasi tersebut ke file template laporan di baris variant yang cocok
        if narasi:
            # Gunakan mapping Variant_Key untuk akurasi pencocokan
            df_template.loc[df_template['Variant_Key'] == variant_map, "Indikasi Faktor Persentase Naik Turun HPP"] = narasi.strip()
            
            
    # ========================================================
    # TAHAP 3: FILTER DATA 'ADJ' UNTUK REKAPITULASI
    # ========================================================
    
    # Mencari baris yang kolom deskripsinya memiliki kata 'ADJ' (case-insensitive)
    df_adj = df_gabungan[df_gabungan[col_desc].astype(str).str.contains('ADJ', case=False, na=False)]
    
    # Membersihkan kolom bantuan/memori agar tabel akhir terlihat profesional
    df_template = df_template.drop(columns=['Variant_Key'])
    df_gabungan = df_gabungan.drop(columns=['Harga_Atas', 'Variant_Key'])
    
    # Output berupa 3 DataFrame yang siap diekspor menjadi 3 Sheet Excel
    return df_template, df_gabungan, df_adj
