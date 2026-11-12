"""CLI-конвертеры данных (ЛР6).

Подкоманды (используются функции из lab05):
    json2csv --in <json> --out <csv>
    csv2json --in <csv> --out <json>
    csv2xlsx --in <csv> --out <xlsx>

Запуск из корня проекта:
    python -m src.lab06.cli_convert json2csv --in data/samples/people.json --out data/out/people.csv
"""

import argparse
import sys
from pathlib import Path

from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx


def check_file(path_str: str, expected_suffix: str) -> Path:
    """Проверяет существование входного файла и его расширение."""
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"файл не найден: {path}")
    if not path.is_file():
        raise ValueError(f"это не файл: {path}")
    if path.suffix.lower() != expected_suffix:
        raise ValueError(f"ожидался файл {expected_suffix}, получен '{path.suffix}': {path}")
    return path


def prepare_output(path_str: str, expected_suffix: str) -> str:
    """Проверяет расширение выходного файла и создаёт каталог при необходимости."""
    path = Path(path_str)
    if path.suffix.lower() != expected_suffix:
        raise ValueError(f"выходной файл должен быть {expected_suffix}, получен '{path.suffix}'")
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


def cmd_json2csv(args: argparse.Namespace) -> int:
    """JSON-список словарей => CSV."""
    check_file(args.input, '.json')
    output = prepare_output(args.output, '.csv')
    json_to_csv(args.input, output)
    print(f"JSON => CSV выполнен: {args.input} => {output}")
    return 0


def cmd_csv2json(args: argparse.Namespace) -> int:
    """CSV => JSON-список словарей."""
    check_file(args.input, '.csv')
    output = prepare_output(args.output, '.json')
    csv_to_json(args.input, output)
    print(f"CSV => JSON выполнен: {args.input} => {output}")
    return 0


def cmd_csv2xlsx(args: argparse.Namespace) -> int:
    """CSV => XLSX (нужна библиотека openpyxl)."""
    check_file(args.input, '.csv')
    output = prepare_output(args.output, '.xlsx')
    csv_to_xlsx(args.input, output)
    print(f"CSV => XLSX выполнен: {args.input} => {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Собирает парсер с подкомандами-конвертерами."""
    parser = argparse.ArgumentParser(
        prog='cli_convert',
        description='CLI-конвертеры данных ЛР6: JSON <-> CSV, CSV -> XLSX.',
    )
    subparsers = parser.add_subparsers(dest='command', metavar='{json2csv,csv2json,csv2xlsx}')

    commands = (
        ('json2csv', 'JSON => CSV', cmd_json2csv, '.json', '.csv'),
        ('csv2json', 'CSV => JSON', cmd_csv2json, '.csv', '.json'),
        ('csv2xlsx', 'CSV => XLSX', cmd_csv2xlsx, '.csv', '.xlsx'),
    )

    for name, description, handler, in_suffix, out_suffix in commands:
        subparser = subparsers.add_parser(
            name,
            help=description,
            description=f'Конвертация {description}.',
        )
        subparser.add_argument(
            '--in', dest='input', required=True,
            metavar='PATH',
            help=f'входной файл ({in_suffix})',
        )
        subparser.add_argument(
            '--out', dest='output', required=True,
            metavar='PATH',
            help=f'выходной файл ({out_suffix})',
        )
        subparser.set_defaults(func=handler)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Точка входа CLI. Возвращает код возврата процесса."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not getattr(args, 'func', None):
        parser.print_help()
        print('\nОшибка: не указана подкоманда (json2csv, csv2json или csv2xlsx).', file=sys.stderr)
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
