import pandas as pd
import io
from openpyxl.styles import Alignment

def generate_excel_download(df_laporan, df_hasil_cek, df_adj):
    """
    Fungsi untuk membungkus 3 DataFrame ke dalam satu file Excel (di memori)
    beserta format styling seperti Wrap Text.
    """
    # Membuat objek BytesIO sebagai wadah memori untuk menyimpan file Excel
    # Ini mencegah file harus disimpan ke hardisk server dan mencegah web refresh
    output = io.BytesIO()
    
    # Menggunakan engine openpyxl untuk bisa memodifikasi format Excel (seperti wrap text)
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        
        # 1. Menulis data ke masing-masing Sheet
        # Tipe data numerik (int/float) dari Pandas akan otomatis dibaca sebagai Angka (Number) di Excel
        df_laporan.to_excel(writer, sheet_name='Laporan', index=False)
        df_hasil_cek.to_excel(writer, sheet_name='Hasil Cek Kartu Stok', index=False)
        df_adj.to_excel(writer, sheet_name='Data ADJ', index=False)
        
        # 2. Mengambil akses ke file Excel yang sedang dibuat
        workbook = writer.book
        worksheet_laporan = writer.sheets['Laporan']
        
        # 3. Menerapkan Wrap Text pada kolom "Indikasi Faktor Persentase Naik Turun HPP"
        # Kita cari dulu kolom tersebut ada di urutan ke berapa (index)
        col_idx = None
        for idx, col_name in enumerate(df_laporan.columns):
            if "Indikasi Faktor" in col_name:
                col_idx = idx + 1  # openpyxl menggunakan urutan mulai dari 1 (A=1, B=2, dst)
                break
        
        if col_idx:
            # Looping ke semua baris di kolom indikasi tersebut (mulai dari baris 2 karena baris 1 adalah judul)
            for row in range(2, worksheet_laporan.max_row + 1):
                cell = worksheet_laporan.cell(row=row, column=col_idx)
                # Terapkan wrap text dan buat posisi teks berada di atas (top)
                cell.alignment = Alignment(wrap_text=True, vertical='top')
                
            # Lebarkan sedikit ukuran kolomnya agar lebih enak dibaca (lebar 50)
            col_letter = worksheet_laporan.cell(row=1, column=col_idx).column_letter
            worksheet_laporan.column_dimensions[col_letter].width = 50

    # Mengembalikan (return) file Excel yang sudah jadi dalam bentuk data biner siap unduh
    processed_data = output.getvalue()
    return processed_data
