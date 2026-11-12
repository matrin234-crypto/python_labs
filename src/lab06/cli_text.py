"""CLI-утилиты для работы с текстом (ЛР6).

Подкоманды:
    stats --input <txt> [--top N]  — частотный анализ слов (функции из lab03)
    cat   --input <path> [-n]      — вывод содержимого файла построчно

Запуск из корня проекта:
    python -m src.lab06.cli_text stats --input data/samples/people.txt --top 5
    python -m src.lab06.cli_text cat --input data/samples/people.csv -n
"""

import argparse
import sys
from pathlib import Path

from src.lib.text import tokenize, count_freq, top_n

# Ширина номера строки для команды cat -n
LINE_NUMBER_WIDTH = 6


def positive_int(value: str) -> int:
    """Тип аргумента argparse: целое число больше нуля."""
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' не является целым числом")
    if number <= 0:
        raise argparse.ArgumentTypeError(f"значение должно быть > 0, получено {number}")
    return number


def read_text_file(path_str: str, *, allow_any_extension: bool = True) -> str:
    """Читает текстовый файл в UTF-8, проверяя его наличие и расширение."""
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"файл не найден: {path}")
    if not path.is_file():
        raise ValueError(f"это не файл: {path}")
    if not allow_any_extension and path.suffix.lower() != '.txt':
        raise ValueError(f"ожидался файл .txt, получен '{path.suffix}'")
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        raise ValueError(f"файл не является текстом в кодировке UTF-8: {path}")


def print_freq_table(top: list[tuple[str, int]]) -> None:
    """Печатает частоты слов в виде таблицы (как в lab03)."""
    max_word_len = max((len(word) for word, _ in top), default=0)
    max_word_len = max(max_word_len, len('Слово'))
    print(f"{'Слово':<{max_word_len}} | Частота")
    print('-' * (max_word_len + 3 + len('Частота')))  # 3 — символы ' | '
    for word, count in top:
        print(f"{word:<{max_word_len}} | {count}")


def cmd_stats(args: argparse.Namespace) -> int:
    """Подкоманда stats: топ частотных слов в тексте."""
    text = read_text_file(args.input)

    tokens = tokenize(text)
    freq = count_freq(tokens)
    top = top_n(freq, n=args.top)

    if not tokens:
        print(f"В файле '{args.input}' не найдено ни одного слова.")
        return 0

    print(f"Файл: {args.input}")
    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    print(f"Топ-{args.top}:")
    print_freq_table(top)
    return 0


def cmd_cat(args: argparse.Namespace) -> int:
    """Подкоманда cat: построчный вывод файла с нумерацией при -n."""
    text = read_text_file(args.input)

    for number, line in enumerate(text.splitlines(), start=1):
        if args.number:
            print(f"{number:>{LINE_NUMBER_WIDTH}}\t{line}")
        else:
            print(line)
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Собирает парсер с подкомандами stats и cat."""
    parser = argparse.ArgumentParser(
        prog='cli_text',
        description='CLI-утилиты ЛР6: частотный анализ текста и вывод файла.',
    )
    subparsers = parser.add_subparsers(dest='command', metavar='{stats,cat}')

    stats_parser = subparsers.add_parser(
        'stats',
        help='частоты слов в текстовом файле',
        description='Считает частоты слов (функции lab03) и выводит топ-N.',
    )
    stats_parser.add_argument(
        '--input', required=True,
        help='путь к текстовому файлу (.txt) для анализа',
    )
    stats_parser.add_argument(
        '--top', type=positive_int, default=5,
        help='сколько самых частых слов показать (по умолчанию 5)',
    )
    stats_parser.set_defaults(func=cmd_stats)

    cat_parser = subparsers.add_parser(
        'cat',
        help='вывести содержимое файла построчно',
        description='Выводит содержимое файла построчно (аналог cat/grep-lite).',
    )
    cat_parser.add_argument(
        '--input', required=True,
        help='путь к файлу для вывода',
    )
    cat_parser.add_argument(
        '-n', '--number', action='store_true',
        help='нумеровать строки',
    )
    cat_parser.set_defaults(func=cmd_cat)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Точка входа CLI. Возвращает код возврата процесса."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not getattr(args, 'func', None):
        parser.print_help()
        print('\nОшибка: не указана подкоманда (stats или cat).', file=sys.stderr)
        return 1

    try:
        return args.func(args)
    except FileNotFoundError as error:
        print(f'Ошибка: {error}', file=sys.stderr)
        return 1
    except ValueError as error:
        print(f'Ошибка: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
