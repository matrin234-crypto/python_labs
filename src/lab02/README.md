# ЛР-2 по ПиА.

## Задание 1
### min_max
Просто сортировка пузырьком: пробегаемся циклом по списку, ищем числа большие x_max и меньшие x_min, записываем. Возвращаем кортеж.
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
![arrays_min_max](images/lab02/arrays_min_max.png)