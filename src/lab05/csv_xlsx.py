import csv
from openpyxl import Workbook
from pathlib import Path

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """Конвертирует CSV в XLSX с автоматическим расчетом ширины колонок."""
    csv_p = Path(csv_path)
    
    if not csv_p.exists():
        raise FileNotFoundError('Файл не существует')
    if csv_p.suffix != '.csv':
        raise ValueError('Файл не .csv')
    if csv_p.stat().st_size == 0:
        raise ValueError("CSV-файл пуст или не содержит данных.")
    
    try:
        with csv_p.open('r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            try:
                headers = next(csv_reader)
            except StopIteration:
                raise ValueError("CSV-файл пуст или не содержит данных.")
            
            data = [row for row in csv_reader if any(val.strip() for val in row if val)]
    except csv.Error:
        raise ValueError("Неверный формат CSV-файла.")
    
    if not headers or not any(h.strip() for h in headers if h):
        raise ValueError("CSV-файл пуст или не содержит данных.")
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    
    ws.append(headers)
    for row in data:
        ws.append(row)
    
    # обход колонок
    for col in ws.columns:
        max_len = 0
        for cell in col:
            if cell.value is not None:
                val_len = len(str(cell.value))
                if val_len > max_len:
                    max_len = val_len
        
        # Безопасно берем букву колонки из первой ячейки в этой колонке
        col_letter = col[0].column_letter
        ws.column_dimensions[col_letter].width = max(max_len + 2, 8)
    
    wb.save(xlsx_path)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) == 3:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        
        print(f"Запуск ручной конвертации по аргументам из консоли.")
        csv_to_xlsx(input_path, output_path)
        print(f"CSV => XLSX выполнен: {input_path} => {output_path}")
        
    else:
        print("Аргументы не переданы. Запуск встроенного сценария.")
        csv_to_xlsx('data/samples/students.csv', 'data/out/students.xlsx')
        print("Встроенный сценарий CSV => XLSX успешно завершен.")