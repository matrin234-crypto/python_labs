import argparse
import sys
from pathlib import Path

# Подгружаем корень, чтобы импорты из src.* работали без ошибок
sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.lib.text import normalize, tokenize, count_freq, top_n
from src.lab04.io_txt_csv import read_text, write_csv


def print_pretty_table(rows: list[tuple], headers: tuple[str, ...]) -> None:
    """★ Вывод отформатированной таблицы в консоль."""
    if not rows:
        return
    widths = [max(len(str(cell)) for cell in col) for col in zip(*([headers] + rows))]
    border = "+" + "+".join(["-" * (w + 2) for w in widths]) + "+"
    fmt = "| " + " | ".join([f"{{:<{w}}}" for w in widths]) + " |"
    
    print(border)
    print(fmt.format(*headers))
    print(border)
    for r in rows:
        print(fmt.format(*r))
    print(border)


def main():
    parser = argparse.ArgumentParser(description="ЛР4 — Отчёты по текстовой статистике")
    parser.add_argument("--in", nargs="+", dest="inputs", help="Входные файлы")
    parser.add_argument("--out", dest="output", default="data/lab04/report.csv", help="Выходной CSV базовой версии")
    parser.add_argument("--encoding", default="utf-8", help="Кодировка файлов")
    
    parser.add_argument("--per-file", default="data/lab04/report_per_file.csv", help="Путь к отчету по каждому файлу")
    parser.add_argument("--total", default="data/lab04/report_total.csv", help="Путь к общему сводному отчету")
    
    args = parser.parse_args()

    input_paths = [Path(p) for p in args.inputs] if args.inputs else [Path("data/lab04/input.txt")]

    for p in input_paths:
        if not p.exists():
            print(f"Ошибка: Файл не найден: {p}", file=sys.stderr)
            sys.exit(1)

    # --- РЕЖИМ А: Базовый (один файл) ---
    if len(input_paths) == 1:
        target_path = input_paths[0]
        tokens = tokenize(read_text(target_path, encoding=args.encoding))
        freq = count_freq(tokens)
        
        all_sorted = top_n(freq, n=len(freq))

        print(f"Всего слов: {len(tokens)}")
        print(f"Уникальных слов: {len(freq)}")
        print("Топ-5:")
        for word, count in all_sorted[:5]:
            print(f"  {word}:{count}")

        print("\nПолный отчёт:")
        print_pretty_table(all_sorted, ("word", "count"))
        write_csv(all_sorted, args.output, header=("word", "count"))

    # --- РЕЖИМ Б: Несколько файлов (★) ---
    else:
        per_file_rows = []
        total_freq = {}

        for p in input_paths:
            raw_text = read_text(p, encoding=args.encoding)
            tokens = tokenize(raw_text)
            freq = count_freq(tokens)
            
            for word, count in freq.items():
                per_file_rows.append((p.name, word, count))
                total_freq[word] = total_freq.get(word, 0) + count

        # Сортировка: имя файла ↑, количество ↓, слово ↑
        per_file_rows.sort(key=lambda x: (x[0], -x[2], x[1]))

        # Общий сводный отчёт
        total_sorted = top_n(total_freq, n=len(total_freq))

        # Запись в CSV
        write_csv(per_file_rows, args.per_file, header=("file", "word", "count"))
        write_csv(total_sorted, args.total, header=("word", "count"))

        # Вывод результатов в консоль
        print("\nСводный топ-10 по всем файлам:")
        print_pretty_table(total_sorted[:10], ("word", "count"))
        print(f"\n[Успешно] Отчёты сохранены в:\n  - {args.per_file}\n  - {args.total}")


if __name__ == "__main__":
    main()
