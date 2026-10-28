import json
import csv
from pathlib import Path

def json_to_csv(json_path: str, csv_path: str) -> None:
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл {json_path} не найден.")
        
    # Проверка на пустой файл (0 байт)
    if path.stat().st_size == 0:
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    with open(json_path, 'r', encoding='utf-8') as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            raise ValueError("Пустой JSON или неподдерживаемая структура")
        
        if not isinstance(data, list):
            raise ValueError("Данные в файле не являются списком словарей.")
        
        if not data:
            raise ValueError("Пустой JSON или неподдерживаемая структура")
            
        # Валидация: все ли элементы списка являются словарями
        if not all(isinstance(item, dict) for item in data):
            raise ValueError("Список содержит элементы, не являющиеся словарями")
        
        # Собираем ВСЕ уникальные ключи из всех словарей (чтобы учесть отсутствующие поля)
        fields = []
        for item in data:
            for key in item.keys():
                if key not in fields:
                    fields.append(key)
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            restval='' # автоматически заполнит отсутствующие ключи пустыми строками
            csv_writer = csv.DictWriter(csv_file, fieldnames=fields, restval='')
            csv_writer.writeheader()
            csv_writer.writerows(data)
        
def csv_to_json(csv_path: str, json_path: str) -> None:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл {csv_path} не найден.")
        
    if path.stat().st_size == 0:
        raise ValueError("CSV-файл пуст или не содержит данных.")
    
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Проверка на наличие заголовков
        if csv_reader.fieldnames is None or not any(csv_reader.fieldnames):
            raise ValueError("CSV-файл пуст или не содержит данных.")
            
        data = [row for row in csv_reader]
        
        if not data:
            raise ValueError("CSV-файл пуст или не содержит данных.")
        
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)
