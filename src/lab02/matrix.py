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


if __name__ == '__main__':
    transpose_test = [
        [[1, 2, 3]],
        [[1], [2], [3]],
        [[1, 2], [3, 4]],
        [],
        [[1, 2], [3]],
    ]

    # for i in transpose_test:
    #     try:
    #         print(i, '=>', f'{transpose(i)}')
    #     except Exception as err:
    #         print(i, '=>', f'Тип ошибки: {type(err)}, Комментарий: {err}')

    row_sums_test = [
        [[1, 2, 3], [4, 5, 6]],
        [[-1, 1], [10, -10]],
        [[0, 0], [0, 0]],
        [[1, 2], [3]]
    ]

    # for i in row_sums_test:
    #     try:
    #         print(i, '=>', row_sums(i))
    #     except Exception as err:
    #         print(i, '=>', f'Тип ошибки: {type(err)}, Комментарий: {err}')

    col_sums_test = [
        [[1, 2, 3], [4, 5, 6]],
        [[-1, 1], [10, -10]],
        [[0, 0], [0, 0]],
        [[1, 2], [3]]
    ]

    for i in col_sums_test:
            try:
                print(i, '=>', col_sums(i))
            except Exception as err:
                print(i, '=>', f'Тип ошибки: {type(err)}, Комментарий: {err}')