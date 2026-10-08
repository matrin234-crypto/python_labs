def fio_unwrap(fio: str) -> list[str]:    
    return [i[0].upper() + i[1:] for i in fio.split()]

def fio_check(fio: str) -> bool:
    split_fio = fio.split()
    if len(split_fio) > 3 or len(split_fio) < 2:
        return False
    return True

def group_check(group: str) -> bool:
    if len(group.strip()) == 0:
        return False
    return True

def gpa_check(gpa: int | float) -> bool:
    if 0 <= gpa <= 5:
        return True
    return False

def format_record(rec: tuple[str, str, float]) -> str:
    
    #все ошибки \/ \/ \/ \/

    #длина кортежа \/
    if len(rec) !=3:
        raise ValueError('Запись должна состоять из 3 элементов.')
    #типы данных \/
    if not isinstance(rec, tuple):
        raise TypeError('Запись должна быть кортежем.')
    if not isinstance(rec[0], str):
        raise TypeError('ФИО должны быть строчным значением.')
    if not isinstance(rec[1], str):
        raise TypeError('Группа должна быть строчным значением.')
    if not isinstance(rec[2], float):
        raise TypeError('GPA должна быть числом с плавающей точкой.')
    #корректность данных \/
    if not fio_check(rec[0]):
        raise ValueError('Некорректные ФИО. Максимальное количество слов - 3, минимальное - 2.')
    if not group_check(rec[1]):
        raise ValueError('Некорректная группа. Номер группы состоит минимум из 1 символа.')
    if not gpa_check(rec[2]):
        raise ValueError('Некорректная GPA. Значение должно быть от 0 до 5.')

    fio_unwrapped = fio_unwrap(rec[0])
    target_fio = fio_unwrapped[0] + ' ' + '.'.join([fio_unwrapped[i][0] for i in range(1, len(fio_unwrapped))])+'.'

    return f'{target_fio}, гр. {rec[1].strip().upper()}, GPA {rec[2]:.2f}'

if __name__ == '__main__':
    format_record_tests = [
        ("Иванов Иван Иванович", "BIVT-25", 4.6),
        ("Петров Пётр", "IKBO-12", 5.0),
        ("Петров Пётр Петрович", "IKBO-12", 5.0),
        ("  сидорова  анна   сергеевна ", "ABB-01", 3.999)
    ]

    for i in format_record_tests:
        try:
            print(i, '=>', format_record(i))
        except Exception as err:
            print(i, '=>', f'Тип ошибки: {type(err)}, Комментарий: {err}')