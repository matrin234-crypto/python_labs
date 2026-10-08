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

def unique_sorted(nums: list[float | int]) -> list[float | int]:

    set_nums = list(set(nums))

    #сортировка пузырьком
    for i in range(len(set_nums)):
        for j in range(len(set_nums) - 1):
            if set_nums[j] > set_nums[j+1]:
                set_nums[j], set_nums[j+1] = set_nums[j+1], set_nums[j]

    return set_nums

def flatten(mat: list[list | tuple]) -> list:
    #защита от неграмотности пользователя («строка не строка строк матрицы»)
    m = []
    for i in mat:
        if not isinstance(i, list | tuple):
            raise TypeError('Элемент матрицы должен быть списком или кортежем.')
        m.extend(i)
    return m

if __name__ == '__main__':
    min_max_tests = [
        [3, -1, 5, 5, 0],
        [42],
        [-5, -2, -9],
        [],
        [1.5, 2, 2.0, -3.1]
    ]

    # for i in min_max_tests:
    #     try:
    #         print(i, '=>', min_max(i))
    #     except Exception as err:
    #         print(i, '=>', f'Тип ошибки: {type(err)}, Комментарий: {err}')

    unique_sorted_tests = [
        [3, 1, 2, 1, 3],
        [],
        [-1, -1, 0, 2, 2],
        [1.0, 1, 2.5, 2.5, 0]
        ]

    # for i in unique_sorted_tests:
    #     try:
    #         print(i, '=>', unique_sorted(i))
    #     except Exception as err:
    #         print(i, '=>', f'Тип ошибки: {type(err)}, Комментарий: {err}')

    flatten_tests = [
        [[1, 2], [3, 4]],
        [[1, 2], (3, 4, 5)],
        [[1], [], [2, 3]],
        [[1, 2], "ab"]
    ]

    for i in flatten_tests:
        try:
            print(i, '=>', flatten(i))
        except Exception as err:
            print(i, '=>', f'Тип ошибки: {type(err)}, Комментарий: {err}')

