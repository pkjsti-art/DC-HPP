import pandas as pd
import io
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side

def generate_excel_download(df_laporan, df_hasil_cek, df_adj, df_master_talang=None, df_rekap_talang=None):
    """
    Membungkus hasil pengolahan ke dalam satu file Excel.
    - Default: 3 sheet (Laporan, Hasil Cek Kartu Stok, Data ADJ)
    - Jika data Pindah Gudang tersedia: +2 sheet (DATA MASTER TALANG, DATA REKAP TALANG)
    """
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # --- SHEET WAJIB (TIDAK DIUBAH) ---
        df_laporan.to_excel(writer, sheet_name='Laporan', index=False)
        df_hasil_cek.to_excel(writer, sheet_name='Hasil Cek Kartu Stok', index=False)
        df_adj.to_excel(writer, sheet_name='Data ADJ', index=False)
        
        # 1. Format Sheet Laporan (Wrap Text)
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

        # 2. Format Sheet Hasil Cek (Persentase Excel)
        worksheet_hasil = writer.sheets['Hasil Cek Kartu Stok']
        col_idx_persen = None
        for idx, col_name in enumerate(df_hasil_cek.columns):
            if "Persentase Selisih" in str(col_name):
                col_idx_persen = idx + 1
                break
                
        if col_idx_persen:
            for row in range(2, worksheet_hasil.max_row + 1):
                cell = worksheet_hasil.cell(row=row, column=col_idx_persen)
                if isinstance(cell.value, (int, float)):
                    cell.number_format = '0.00%' 

        # --- SHEET OPSIONAL: MASTER & REKAP TALANG ---
        if df_master_talang is not None and df_rekap_talang is not None:
            df_master_talang.to_excel(writer, sheet_name='DATA MASTER TALANG', index=False)
            df_rekap_talang.to_excel(writer, sheet_name='DATA REKAP TALANG', index=False)
            
            # Styling Sheet DATA REKAP TALANG
            ws_rekap = writer.sheets['DATA REKAP TALANG']
            
            header_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
            header_font = Font(color='FFFFFF', bold=True)
            thin_border = Border(
                left=Side(style='thin', color='D9D9D9'),
                right=Side(style='thin', color='D9D9D9'),
                top=Side(style='thin', color='D9D9D9'),
                bottom=Side(style='thin', color='D9D9D9')
            )
            
            # Format Header (Baris 1)
            for col in range(1, 4):
                cell = ws_rekap.cell(row=1, column=col)
                cell.fill = header_fill
                cell.font = header_font
                cell.border = thin_border
                
            # Format Isi Data & Angka Ribuan Desimal
            last_data_row = ws_rekap.max_row
            for row in range(2, last_data_row + 1):
                for col in range(1, 4):
                    cell = ws_rekap.cell(row=row, column=col)
                    cell.border = thin_border
                    if col == 3:
                        cell.number_format = '#,##0.00'
                        
            # Tambahkan Baris Grand Total dengan Rumus SUM Dinamis
            total_row = last_data_row + 1
            for col in range(1, 4):
                cell = ws_rekap.cell(row=total_row, column=col)
                cell.fill = header_fill
                cell.font = header_font
                cell.border = thin_border
                
            total_cell = ws_rekap.cell(row=total_row, column=3)
            total_cell.value = f"=SUM(C2:C{last_data_row})" if last_data_row >= 2 else 0
            total_cell.number_format = '#,##0.00'
            
            # Auto-fit Lebar Kolom
            for col in ws_rekap.columns:
                max_length = 0
                col_letter = col[0].column_letter
                for cell in col:
                    val_str = str(cell.value) if cell.value is not None else ""
                    if len(val_str) > max_length:
                        max_length = len(val_str)
                ws_rekap.column_dimensions[col_letter].width = max_length + 5

    processed_data = output.getvalue()
    return processed_data
