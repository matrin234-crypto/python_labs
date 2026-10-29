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
