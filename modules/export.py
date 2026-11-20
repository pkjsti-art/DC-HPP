import pandas as pd
import io
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side

def _apply_standard_styling(ws, wrap_col_indices=None):
    """
    Menerapkan header biru gelap, border tipis, dan auto-fit lebar kolom
    untuk seluruh tabel pada sebuah worksheet.
    """
    if wrap_col_indices is None:
        wrap_col_indices = set()

    header_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
    header_font = Font(color='FFFFFF', bold=True)
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    max_row = ws.max_row
    max_col = ws.max_column

    # 1. Styling Header (Baris 1)
    for col in range(1, max_col + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = thin_border
        cell.alignment = Alignment(vertical='center')

    # 2. Border untuk seluruh baris data
    for row in range(2, max_row + 1):
        for col in range(1, max_col + 1):
            cell = ws.cell(row=row, column=col)
            cell.border = thin_border

    # 3. Auto-fit Lebar Kolom
    for col_idx in range(1, max_col + 1):
        col_letter = ws.cell(row=1, column=col_idx).column_letter
        if col_idx in wrap_col_indices:
            ws.column_dimensions[col_letter].width = 55
            continue

        max_length = 0
        for row_idx in range(1, max_row + 1):
            val = ws.cell(row=row_idx, column=col_idx).value
            if val is not None:
                val_str = str(val)
                # Jika ada enter di dalam sel, ambil baris terpanjang
                longest_line = max((len(line) for line in val_str.split('\n')), default=0)
                if longest_line > max_length:
                    max_length = longest_line

        ws.column_dimensions[col_letter].width = min(max(max_length + 4, 10), 65)


def generate_excel_download(
    df_laporan, 
    df_hasil_cek, 
    df_adj, 
    df_master_talang=None, 
    df_rekap_talang=None, 
    df_mb_to=None
):
    """
    Membungkus hasil pengolahan ke dalam satu file Excel dengan styling seragam
    di semua sheet (header biru gelap, border, auto-fit kolom, dan tipe angka murni).
    """
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # --- SHEET WAJIB ---
        df_laporan.to_excel(writer, sheet_name='Laporan', index=False)
        df_hasil_cek.to_excel(writer, sheet_name='Hasil Cek Kartu Stok', index=False)
        df_adj.to_excel(writer, sheet_name='Data ADJ', index=False)
        
        # ========================================================
        # 1. FORMAT SHEET LAPORAN
        # ========================================================
        ws_lap = writer.sheets['Laporan']
        wrap_cols_lap = set()

        for idx, col_name in enumerate(df_laporan.columns):
            col_idx = idx + 1
            col_lower = str(col_name).strip().lower()

            # Wrap Text pada kolom Indikasi Faktor
            if "indikasi faktor" in col_lower:
                wrap_cols_lap.add(col_idx)
                for row in range(2, ws_lap.max_row + 1):
                    cell = ws_lap.cell(row=row, column=col_idx)
                    cell.alignment = Alignment(wrap_text=True, vertical='top')

            # Konversi kolom QTY menjadi Number murni
            elif col_lower == 'qty':
                for row in range(2, ws_lap.max_row + 1):
                    cell = ws_lap.cell(row=row, column=col_idx)
                    val = cell.value
                    if val is None or str(val).strip() == "":
                        continue
                    try:
                        if isinstance(val, str):
                            clean_val = val.strip().replace(',', '')
                            num_val = float(clean_val)
                        else:
                            num_val = float(val)
                        
                        if num_val.is_integer():
                            cell.value = int(num_val)
                            cell.number_format = '#,##0'
                        else:
                            cell.value = num_val
                            cell.number_format = '#,##0.00'
                    except ValueError:
                        pass

            # Konversi kolom PRESENTASE / PERSENTASE NAIK TURUN menjadi Number (%)
            elif ('presentase' in col_lower or 'persentase' in col_lower) and 'naik turun' in col_lower:
                for row in range(2, ws_lap.max_row + 1):
                    cell = ws_lap.cell(row=row, column=col_idx)
                    val = cell.value
                    if val is None or str(val).strip() == "":
                        continue
                    try:
                        if isinstance(val, str):
                            s = val.strip()
                            if '%' in s:
                                num_val = float(s.replace('%', '').replace(',', '.').strip()) / 100.0
                            else:
                                num_val = float(s.replace(',', '.').strip())
                            cell.value = num_val
                        elif isinstance(val, (int, float)):
                            cell.value = float(val)
                        cell.number_format = '0.00%'
                    except ValueError:
                        pass

        _apply_standard_styling(ws_lap, wrap_col_indices=wrap_cols_lap)

        # ========================================================
        # 2. FORMAT SHEET HASIL CEK KARTU STOK & DATA ADJ
        # ========================================================
        ws_hasil = writer.sheets['Hasil Cek Kartu Stok']
        for idx, col_name in enumerate(df_hasil_cek.columns):
            if "persentase selisih" in str(col_name).lower():
                col_idx = idx + 1
                for row in range(2, ws_hasil.max_row + 1):
                    cell = ws_hasil.cell(row=row, column=col_idx)
                    if isinstance(cell.value, (int, float)):
                        cell.number_format = '0.00%'
        _apply_standard_styling(ws_hasil)

        ws_adj = writer.sheets['Data ADJ']
        _apply_standard_styling(ws_adj)

        # ========================================================
        # 3. SHEET OPSIONAL: MASTER & REKAP TALANG
        # ========================================================
        if df_master_talang is not None and df_rekap_talang is not None:
            df_master_talang.to_excel(writer, sheet_name='DATA MASTER TALANG', index=False)
            df_rekap_talang.to_excel(writer, sheet_name='DATA REKAP TALANG', index=False)
            
            _apply_standard_styling(writer.sheets['DATA MASTER TALANG'])

            ws_rekap = writer.sheets['DATA REKAP TALANG']
            header_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
            header_font = Font(color='FFFFFF', bold=True)
            thin_border = Border(
                left=Side(style='thin', color='D9D9D9'),
                right=Side(style='thin', color='D9D9D9'),
                top=Side(style='thin', color='D9D9D9'),
                bottom=Side(style='thin', color='D9D9D9')
            )
            
            last_data_row = ws_rekap.max_row
            for row in range(2, last_data_row + 1):
                ws_rekap.cell(row=row, column=3).number_format = '#,##0.00'
                        
            # Baris Grand Total dengan Rumus SUM Dinamis
            total_row = last_data_row + 1
            for col in range(1, 4):
                cell = ws_rekap.cell(row=total_row, column=col)
                cell.fill = header_fill
                cell.font = header_font
                cell.border = thin_border
                
            total_cell = ws_rekap.cell(row=total_row, column=3)
            total_cell.value = f"=SUM(C2:C{last_data_row})" if last_data_row >= 2 else 0
            total_cell.number_format = '#,##0.00'
            
            _apply_standard_styling(ws_rekap)
            # Pastikan baris total tetap berwarna biru gelap setelah styling standar
            for col in range(1, 4):
                cell = ws_rekap.cell(row=total_row, column=col)
                cell.fill = header_fill
                cell.font = header_font

        # ========================================================
        # 4. SHEET OPSIONAL: MASTER MB TO
        # ========================================================
        if df_mb_to is not None:
            df_mb_to.to_excel(writer, sheet_name='DATA MASTER MB TO', index=False)
            _apply_standard_styling(writer.sheets['DATA MASTER MB TO'])

    processed_data = output.getvalue()
    return processed_data
