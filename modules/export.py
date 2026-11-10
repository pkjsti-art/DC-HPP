import pandas as pd
import io
from openpyxl.styles import Alignment

def generate_excel_download(df_laporan, df_hasil_cek, df_adj):
    """
    Fungsi untuk membungkus 3 DataFrame ke dalam satu file Excel,
    lengkap dengan Wrap Text dan Formatting Persentase murni.
    """
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        
        df_laporan.to_excel(writer, sheet_name='Laporan', index=False)
        df_hasil_cek.to_excel(writer, sheet_name='Hasil Cek Kartu Stok', index=False)
        df_adj.to_excel(writer, sheet_name='Data ADJ', index=False)
        
        workbook = writer.book
        
        # --- 1. FORMAT SHEET LAPORAN (WRAP TEXT) ---
        worksheet_laporan = writer.sheets['Laporan']
        col_idx_lap = None
        
        for idx, col_name in enumerate(df_laporan.columns):
            if "Indikasi Faktor" in str(col_name):
                col_idx_lap = idx + 1
                break
        
        if col_idx_lap:
            for row in range(2, worksheet_laporan.max_row + 1):
                cell = worksheet_laporan.cell(row=row, column=col_idx_lap)
                cell.alignment = Alignment(wrap_text=True, vertical='top')
                
            col_letter = worksheet_laporan.cell(row=1, column=col_idx_lap).column_letter
            worksheet_laporan.column_dimensions[col_letter].width = 50

        # --- 2. FORMAT SHEET HASIL CEK (PERSENTASE EXCEL) ---
        worksheet_hasil = writer.sheets['Hasil Cek Kartu Stok']
        col_idx_persen = None
        
        for idx, col_name in enumerate(df_hasil_cek.columns):
            if "Persentase Selisih" in str(col_name):
                col_idx_persen = idx + 1
                break
                
        if col_idx_persen:
            for row in range(2, worksheet_hasil.max_row + 1):
                cell = worksheet_hasil.cell(row=row, column=col_idx_persen)
                # Terapkan format Persentase jika sel tersebut berisi angka
                if isinstance(cell.value, (int, float)):
                    cell.number_format = '0.00%' 

    processed_data = output.getvalue()
    return processed_data
