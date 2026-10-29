# ЛР_05
## Установка
Для CSV => XLSX нужна библиотека 'openpyxl', она указана в 'requirements.txt'.

```bash
pip install -r requirements.txt
```
## Запуск
Все команды должны запускаться из корня проекта.

```bash
# JSON <=> CSV
python -m src.lab05.json_csv

# CSV => XLSX
python -m src.lab05.csv_xlsx
```

Для загрузки базовых семплов можно запустить файл 'run_demo.py'. [Файл](/src/lab05/run_demo.py)

## Результаты от базовых семплов ТЗ можно посмотреть тут:
- [people_from_json.csv](/data/out/people_from_json.csv)
- [people_from_csv.json](/data/out/people_from_csv.json)
- [people.xlsx](/data/out/people.xlsx)

# Задание А
## json_csv.py

```
import json
import csv
from pathlib import Path

def json_to_csv(json_path: str, csv_path: str) -> None:
    """Преобразует JSON-файл в CSV."""
    json_p = Path(json_path)
    csv_p = Path(csv_path)
    
    if not json_p.exists():
        raise FileNotFoundError('Файл не существует')
    if json_p.suffix != '.json':
        raise ValueError('Файл должен быть .json')
    if json_p.stat().st_size == 0:
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    with json_p.open('r', encoding='utf-8') as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            raise ValueError("Пустой JSON или неподдерживаемая структура")
        
        if not isinstance(data, list) or not data:
            raise ValueError("Пустой JSON или неподдерживаемая структура")
            
        if not all(isinstance(item, dict) for item in data):
            raise ValueError("Список содержит элементы, не являющиеся словарями")
        
        fields_set = set()
        for item in data:
            fields_set.update(item.keys())
        fields = sorted(list(fields_set))
        
        with csv_p.open('w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fields, restval='')
            csv_writer.writeheader()
            csv_writer.writerows(data)
        
def csv_to_json(csv_path: str, json_path: str) -> None:
    """Преобразует CSV в JSON (список словарей)."""
    csv_p = Path(csv_path)
    json_p = Path(json_path)
    
    if not csv_p.exists():
        raise FileNotFoundError('Файл не существует')
    if csv_p.suffix != '.csv':
        raise ValueError('Файл должен быть .csv')
    if csv_p.stat().st_size == 0:
        raise ValueError("CSV-файл пуст или не содержит данных.")
    
    with csv_p.open('r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        if csv_reader.fieldnames is None or not any(name.strip() for name in csv_reader.fieldnames if name):
            raise ValueError('Пустой CSV или нет заголовка')
            
        data = []
        for row in csv_reader:
            if any(val.strip() for val in row.values() if val):
                data.append(row)
        
        if not data:
            raise ValueError('В CSV нет данных')
        
        with json_p.open('w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    import sys
    
    # Если передали аргументы через консоль (длина sys.argv будет равна 3)
    if len(sys.argv) == 3:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        
        print(f"Запуск ручной конвертации по аргументам из консоли.")
        # Автоматически определяем направление по расширению входного файла
        if input_path.endswith('.json'):
            json_to_csv(input_path, output_path)
            print(f"JSON => CSV выполнен: {input_path} => {output_path}")
        elif input_path.endswith('.csv'):
            csv_to_json(input_path, output_path)
            print(f"CSV => JSON выполнен: {input_path} => {output_path}")
        else:
            print("Ошибка: Неподдерживаемый формат входного файла. Используйте .json или .csv")
            
    else:
        # Если запустили просто так, отрабатывает дефолтный сценарий для ЛР
        print("Аргументы не переданы. Запуск встроенного сценария.")
        json_to_csv('data/samples/products.json', 'data/out/products_from_json.csv')
        csv_to_json('data/samples/students.csv', 'data/out/students_from_csv.json')
        print("Встроенный сценарий JSON ↔ CSV завершен.")

```
### Образец:
### 1. JSON => CSV
[products.json](/data/samples/products.json) => [products_from_json.csv](/data/out/products_from_json.csv)
```
item,price,stock
Laptop,1200,5
Mouse,,50
Keyboard,,
```
У некоторых объектов различаются поля, но код с этим справился: недостающие стали пустыми ячейками. Было 3 объекта - стало 3 строки.
### 2. CSV => JSON
[students.csv](/data/samples/students.csv) => [students_from_csv.json](/data/out/students_from_csv.json)
```
[
  {
    "name": "Бобров",
    "group": "",
    "score": "4.8"
  },
  {
    "name": "Сидоров",
    "group": "B23-502",
    "score": ""
  },
  {
    "name": "",
    "group": "B23-501",
    "score": "5.0"
  }
]
```
Было 3 строки - стало 3 объекта. Код нормально работает с кириллицей. Пустые ячейки стали пустой строчкой.
# Задание B
## csv_xlsx.py
```
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
```
### Образец CSV => XLSX:
### [students.csv](/data/samples/students.csv) => [students.xlsx](/data/out/students.xlsx)

![image.png](/images/lab05/image.png)

### Что видим: код воспринимает кириллицу, выставляет нормальную ширину столбцам. Название листа соответствует ТЗ. Пустая ячейка .csv => пустая ячейка .xlsx


