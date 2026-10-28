import csv
import openpyxl

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from pathlib import Path

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл {csv_path} не найден.")
        
    if path.stat().st_size == 0:
        raise ValueError("CSV-файл пуст или не содержит данных.")
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            try:
                headers = next(csv_reader)
            except StopIteration:
                raise ValueError("CSV-файл пуст или не содержит данных.")
            data = list(csv_reader)
    except csv.Error:
        raise ValueError(f"Неверный формат CSV-файла {csv_path}.")
    
    if not headers or not any(headers):
        raise ValueError("CSV-файл пуст или не содержит данных.")
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    
    # Используем ws.append для быстрой и безопасной записи (как в примере 3 из ТЗ)
    ws.append(headers)
    for row in data:
        ws.append(row)
    
    # Установка автоширины колонок без print()
    for col_num in range(1, len(headers) + 1):
        col_letter = get_column_letter(col_num)
        max_length = 0
        column = ws[col_letter]
        
        for cell in column:
            val_str = str(cell.value) if cell.value is not None else ""
            if len(val_str) > max_length:
                max_length = len(val_str)
                
        adjusted_width = max_length + 2
        if adjusted_width < 8:
            adjusted_width = 8
        ws.column_dimensions[col_letter].width = adjusted_width
    
    wb.save(xlsx_path)
