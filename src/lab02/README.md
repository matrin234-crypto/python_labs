# ЛР-2 по ПиА.

## Задание 1
### min_max
Простая сортировка: пробегаемся циклом по списку, ищем числа большие x_max и меньшие x_min, записываем. Возвращаем кортеж.
```
def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    # защита от неграмотности пользователя (ввод пустого массива)
    if not nums:
        raise ValueError('В массиве должен быть хотя бы 1 элемент.')

    x_min = 2**31
    x_max = -(2**31)

    for i in nums:
        if i < x_min:
            x_min = i
        if i > x_max:
            x_max = i

    return (x_min, x_max)
```
### Тесткейсы:
![arrays_min_max](/images/lab02/arrays_min_max.png)
### unique_sorted
Чтобы избавиться от повторяющихся элементов превращаю список во множество, затем ещё раз в список. Далее идёт базовая сортировка пузырьком: второй цикл пробегает по всему списку, идёт сравнение пар, стоящих друг за другом. Сравнение повторяется, пока не получится порядок возрастания.
```
def unique_sorted(nums: list[float | int]) -> list[float | int]:

    set_nums = list(set(nums))

    #сортировка пузырьком
    for i in range(len(set_nums)):
        for j in range(len(set_nums) - 1 - i):
            if set_nums[j] > set_nums[j+1]:
                set_nums[j], set_nums[j+1] = set_nums[j+1], set_nums[j]

    return set_nums
```
### Тесткейсы:
![arrays_unique_sorted](/images/lab02/arrays_unique_sorted.png)
### flatten
Через цикл проверяю, корректны ли вводные (являются ли элементы матрицы списком/кортежем). В этом же цикле добавляю в новый список все значения через метод .extend(...).
```
def flatten(mat: list[list | tuple]) -> list:
    #защита от неграмотности пользователя («строка не строка строк матрицы»)
    m = []
    for i in mat:
        if not isinstance(i, list | tuple):
            raise TypeError('Элемент матрицы должен быть списком или кортежем.')
        m.extend(i)
    return m
```
### Тесткейсы:
![arrays_flatten](/images/lab02/arrays_flatten.png)
## Задание B
### transpose
Через функцию (которая будет в коде ниже) проверяю матрицу на прямоугольность. Подготавливаю пустую матрицу. Заполняю её строки сначала всеми первыми элементами, затем всеми вторыми и т.д.
```
def matrix_check(mat: list[list[float | int]]) -> bool:
    expected_length = len(mat[0])
    for i in mat:
        if len(i) != expected_length:
            # raise ValueError('Рваная матрица.')
            return False
    return True

def transpose(mat: list[list[float | int]]) -> list[list]:
    if not mat:
        return []
    for i in mat:
        if not isinstance(i, list):
            raise TypeError('Элемент матрицы должен быть списком.')
    if matrix_check(mat) == False:
        raise ValueError('Матрица должна быть прямоугольной.')

    mat_transpose = [[] for e in range(len(mat[0]))]
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            mat_transpose[j].append(mat[i][j])
    return mat_transpose
```
### Тесткейсы:
![matrix_transpose](/images/lab02/matrix_transpose.png)
### row_sums
Выполняю базовые проверки через ранее использованную функцию. Подготовил список для сумм строк. Через цикл пробегаюсь по строкам, складывая всё в s. Когда строка заканчивается - s записывается в row_sum. S обнуляется. Цикл повторяется. Возвращаю список из сумм строк.
```
def row_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return []
    for i in mat:
        if not isinstance(i, list):
            raise TypeError('Элемент матрицы должен быть списком.')
    if matrix_check(mat) == False:
        raise ValueError('Матрица должна быть прямоугольной.')
    row_sum = []
    for i in range(len(mat)):
        s = 0
        for j in range(len(mat[i])):
            s += mat[i][j]
        row_sum.append(s)
    return row_sum
```
### Тесткейсы:
![matrix_row_sums](/images/lab02/matrix_row_sums.png)
### col_sums
Выполняю базовые проверки с использованием уже знакомой функции. Подготовил список для сумм столбцов. Пробегаюсь по всем первым элементам строк, суммируя их в s. Записываю s в col_sum. S обнуляется. Пробегаюсь по всем вторым и так далее. Результат - список из сумм столбцов матрицы.
```
def col_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return []
    for i in mat:
        if not isinstance(i, list):
            raise TypeError('Элемент матрицы должен быть списком.')
    if matrix_check(mat) == False:
        raise ValueError('Матрица должна быть прямоугольной.')
    col_sum = []
    for i in range(len(mat[0])):
        s = 0
        for j in range(len(mat)):
            s += mat[j][i]
        col_sum.append(s)
    return col_sum
```
### Тесткейсы:
![matrix_col_sums](/images/lab02/matrix_col_sums.png)
## Задание C
Кратко о функциях:
    fio_unwrap - разбивает ФИО, переделывает в список и фиксит всякие проблемы от пользователя (ФИО написано со строчных букв, много пробелов и т.п.) Результат - список из слов.
    fio_check - проверка количества слов в ФИО. Отсекает всё, что меньше 2 и больше 3.
    group_check - сначала убирает лишние пробелы, затем проверяет, что в значении есть хотя бы 1 реальный символ.
    gpa_check - проверка корректности среднего балла успеваемости. Отсекает всё, что не находится в пределе от 0 до 5.
Работа format_record:

    Первоначально сверяемся, что длина кортежа вообще равна трём, иначе попадём на IndexError во всех последующих действиях.

    Блок проверки типов данных отвечает за проверку типов данных в исходниках. (GPA не может быть массивом, ФИО не может быть цельным числом и т.п.)

    Блок корректности данных отвечает за проверку нормальности значений в исходниках. (GPA не может быть равен 1000, у человека не может быть ФИО из 10000 слов и т.д.)

    Форматирование выполняет все основные операции по подготовке к выводу в стандартизированной форме. 

![Код здесь (тык)](/src/lab02/tuples.py)

Это было интересно.