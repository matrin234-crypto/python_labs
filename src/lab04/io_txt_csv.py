import csv
from pathlib import Path
from typing import Iterable, Sequence

def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """
    Открыть файл на чтение в указанной кодировке и вернуть содержимое как одну строку.

    Пример выбора другой кодировки (например, для Windows-файлов):
        text = read_text("document.txt", encoding="cp1251")

    Args:
        path: Путь к файлу (строка или объект Path).
        encoding: Кодировка файла (по умолчанию "utf-8").

    Returns:
        str: Содержимое файла.

    Raises:
        FileNotFoundError: Если файл не найден (всплывает автоматически).
        UnicodeDecodeError: Если указанная кодировка не подходит (всплывает автоматически).
    """
    p = Path(path)
    # По ТЗ FileNotFoundError должен всплывать сам при чтении
    return p.read_text(encoding=encoding)


def ensure_parent_dir(path: str | Path) -> None:
    """Создает родительские директории для указанного пути, если они не существуют."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def write_csv(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    """
    Создать или перезаписать CSV-файл с разделителем ",".

    Args:
        rows: Данные для записи (итерируемый объект из кортежей или списков).
        path: Путь, по которому будет сохранен файл (строка или объект Path).
        header: Заголовок таблицы (по умолчанию None).

    Raises:
        ValueError: Если строки в rows имеют разную длину.
    """
    p = Path(path)
    rows_list = list(rows)
    
    # Краевой случай: данных нет и заголовка нет => пустой файл
    if not rows_list and header is None:
        ensure_parent_dir(p)
        p.write_text("", encoding="utf-8")
        return

    # Определение ожидаемой длины строки
    if header is not None:
        expected_len = len(header)
    else:
        expected_len = len(rows_list[0]) if rows_list else 0

    # Валидация длин строк
    for r in rows_list:
        if len(r) != expected_len:
            raise ValueError(
                f"Несоответствие длины строки. Ожидалось элементов: {expected_len}, "
                f"найдено: {len(r)} в строке {r}"
            )

    ensure_parent_dir(p)

    with p.open("w", newline="", encoding="utf-8") as f: 
        w = csv.writer(f, delimiter=",")
        if header is not None:
            w.writerow(header)
        w.writerows(rows_list)

if __name__ == '__main__':
    # 0 - Тесты записи и вывода CSV, 1 - Тесты чтения
    test_type = 0

    test_dir = Path("data/lab04")
    test_dir.mkdir(parents=True, exist_ok=True)
    csv_file = test_dir / "check.csv"

    match test_type:
        case 0:
            # 1. Запись без явного заголовка (заголовок уже внутри rows)
            write_csv([("word", "count"), ("test", 3)], csv_file, header=None)
            print(csv_file.read_text(encoding="utf-8").strip())
            print("------------")

            # 2. Запись с передачей rows и явного header
            write_csv([("word", "count"), ("test", 3)], csv_file, header=("word", "count"))
            print(csv_file.read_text(encoding="utf-8").strip())
            print("------------")

            # 3. Краевой случай: пустой rows и header=None (создается пустой файл)
            write_csv([], csv_file, header=None)
            print(csv_file.read_text(encoding="utf-8").strip())
            print("------------")

            # 4. Краевой случай: пустой rows, но передан header
            write_csv([], csv_file, header=("word", "count"))
            print(csv_file.read_text(encoding="utf-8").strip())
            print("------------")

        case 1:
            # Быстрый тест чтения
            input_file = test_dir / "input.txt"
            input_file.write_text("Привет, мир!", encoding="utf-8")
            print(read_text(input_file))
            print("------------")

   
