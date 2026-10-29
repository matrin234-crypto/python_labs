import json
import csv
from pathlib import Path

from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx

def count_csv_rows(csv_path: str) -> int:
    """Вспомогательная функция для подсчета строк в CSV (минус заголовок)."""
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        return max(0, len(rows) - 1)

def count_json_objects(json_path: str) -> int:
    """Вспомогательная функция для подсчета объектов в JSON-списке."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return len(data) if isinstance(data, list) else 0

def main():
    # Настраиваем пути (относительно корня проекта python_labs)
    base_dir = Path(__file__).resolve().parent.parent.parent
    
    samples_dir = base_dir / "data" / "samples"
    out_dir = base_dir / "data" / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=== ДЕМОНСТРАЦИЯ ЛР_05 ===\n")

    print("[Сценарий 1] Конвертация JSON => CSV")
    json_in = str(samples_dir / "people.json")
    csv_out = str(out_dir / "people_from_json.csv")
    
    try:
        json_to_csv(json_in, csv_out)
        json_count = count_json_objects(json_in)
        csv_count = count_csv_rows(csv_out)
        print(f"  - Успешно: {json_in} => {csv_out}")
        print(f"  - Проверка: JSON объектов = {json_count}, CSV строк = {csv_count}")
        print(f"  - Результат совпадения: {'100% совпадение' if json_count == csv_count else 'не совпало'}")
    except Exception as e:
        print(f"  - Ошибка в Сценарии 1: {e}")

    print("-" * 50)

    print("[Сценарий 2] Конвертация CSV => JSON")
    csv_in = str(samples_dir / "people.csv")
    json_out = str(out_dir / "people_from_csv.json")
    
    try:
        csv_to_json(csv_in, json_out)
        csv_count = count_csv_rows(csv_in)
        json_count = count_json_objects(json_out)
        print(f"  - Успешно: {csv_in} => {json_out}")
        print(f"  - Проверка: CSV строк = {csv_count}, JSON объектов = {json_count}")
        print(f"  - Результат совпадения: {'100% совпадение' if json_count == csv_count else 'не совпало'}")
    except Exception as e:
        print(f"  - Ошибка в Сценарии 2: {e}")

    print("-" * 50)

    print("[Сценарий 3] Конвертация CSV => XLSX")
    cities_csv = str(samples_dir / "cities.csv")
    cities_xlsx = str(out_dir / "cities.xlsx")
    people_xlsx = str(out_dir / "people.xlsx")
    
    try:
        csv_to_xlsx(cities_csv, cities_xlsx)
        print(f"  - Успешно: {cities_csv} => {cities_xlsx}")
        
        csv_to_xlsx(csv_in, people_xlsx)
        print(f"  - Успешно: {csv_in} => {people_xlsx}")
        print("  - Проверка: Откройте файлы в Excel/LibreOffice для проверки ширины колонок.")
    except Exception as e:
        print(f"  - Ошибка в Сценарии 3: {e}")

    print("\n=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===")

if __name__ == "__main__":
    main()
