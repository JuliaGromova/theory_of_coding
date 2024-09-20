import numpy as np


def change(x, i, j):
    x[[i, j]] = x[[j, i]]


def null_rows_delete(x):
    arr = np.copy(x)
    index_arr = []
    for i in range(arr.shape[0]):
        if not np.any(arr[i][:]) > 0:
            index_arr.append(i)
    arr = np.delete(arr, index_arr, axis=0)
    return arr


def sub_sets(x):
    return subsets_recursion([], sorted(x))


def subsets_recursion(current, x):
    if x:
        return subsets_recursion(current, x[1:]) + subsets_recursion(current + [x[0]], x[1:])
    return [current]


# Возвращает матрицу ступенчатого вида
def ref(matrix):
    arr = np.copy(matrix)
    index = 0
    flag = False
    for j in range(arr.shape[1]):
        for i in range(index, arr.shape[0]):
            if np.any(arr[:, j]) > 0:
                if arr[i, j] == 1:
                    if not flag:
                        change(arr, i, index)
                        flag = True
                    else:
                        arr[i] = (arr[i] + arr[index]) % 2
        if flag:
            index += 1
            flag = False

    arr = null_rows_delete(arr)
    return arr


# Возвращает приведенную матрицу ступенчатого вида
def rref(matrix):
    arr = ref(matrix)
    for i in range(arr.shape[0] - 1, 0, -1):
        index = 0
        for k in range(arr.shape[1]):
            if arr[i][k] == 1:
                index = k
                break
        for j in range(0, i):
            if arr[j][index] == 1:
                arr[j] = (arr[j] + arr[i]) % 2
    return arr


# Возвращает проверочную матрицу
def check_matrix(g):
    x = rref(g)
    k = g.shape[0]
    n = g.shape[1]
    lead = []
    for i in range(k):
        for j in range(n):
            if x[i][j] == 1:
                lead.append(j)
                break
    x = np.delete(x, lead, axis=1)
    new_n = n - len(lead)
    new_k = n - len(lead) + k
    e = np.eye(new_n)
    h = np.zeros((new_k, new_n), dtype=int)
    index_x = 0
    index_e = 0
    for i in range(len(h)):
        if i in lead:
            h[i] = x[index_x]
            index_x += 1
        else:
            h[i] = e[index_e]
            index_e += 1
    return h, lead


def words_by_sum_g(g):
    k = g.shape[0]
    n = g.shape[1]
    words_by_sum = np.array([])

    index = []
    for i in range(k):
        index.append(i)
    sub_index = sub_sets(index)

    for sub in sub_index:
        w = np.zeros(n)
        if sub:
            for i in sub:
                w += g[i]
        w %= 2
        words_by_sum = np.append(words_by_sum, w)

    words_by_sum = np.resize(words_by_sum, (2 ** k, n))
    words_by_sum = words_by_sum.astype(int)
    words_by_sum = np.unique(words_by_sum, axis=0)
    return words_by_sum


def distance(g):
    k = g.shape[0]
    n = g.shape[1]
    for i in range(k - 1):
        for j in range(i + 1, k):
            xor_rows = sum((g[i] + g[j]) % 2)
            if xor_rows < n:
                n = xor_rows
    return n, n - 1


class LinearCode:
    def __init__(self, matrix):
        self.matrix = matrix
        self.g = ref(matrix)
        self.h, self.lead = check_matrix(self.g)

    def shape_of_g(self):
        k = self.g.shape[0]
        n = self.g.shape[1]
        return n, k


def checking(g, h):
    words_by_sum = words_by_sum_g(g)
    print('\n Все слова по сумме G:', words_by_sum, sep='\n')
    matrix = np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0],
                       [0, 0, 0, 1, 1], [0, 0, 1, 0, 0], [0, 0, 1, 0, 1], [0, 0, 1, 1, 0],
                       [0, 0, 1, 1, 1], [0, 1, 0, 0, 0], [0, 1, 0, 0, 1], [0, 1, 0, 1, 0], [0, 1, 0, 1, 1],
                       [0, 1, 1, 0, 0], [0, 1, 1, 0, 1], [0, 1, 1, 1, 0], [0, 1, 1, 1, 1], [1, 0, 0, 0, 0],
                       [1, 0, 0, 0, 1], [1, 0, 0, 1, 0], [1, 0, 0, 1, 1], [1, 0, 1, 0, 0], [1, 0, 1, 0, 1],
                       [1, 0, 1, 1, 0], [1, 0, 1, 1, 1], [1, 1, 0, 0, 0], [1, 1, 0, 0, 1], [1, 1, 0, 1, 0],
                       [1, 1, 0, 1, 1], [1, 1, 1, 0, 0], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0], [1, 1, 1, 1, 1]])
    words_by_multi = matrix @ g % 2
    words_by_multi = np.unique(words_by_multi, axis=0)
    print(' ')
    print('Все слова c умножением на G:', words_by_multi, sep='\n')
    if np.array_equal(words_by_multi, words_by_sum):
        print('Массивы одинаковы')
    else:
        print('Массивы не одинаковы')
    # умножение всех кодовых слов на проверочную матрицу:
    check = words_by_multi @ h % 2
    print(' ')
    print('Умножение кодовых слов на проверочную матрицу:', check, sep='\n')


prim_arr = np.array([[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
                     [0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
                     [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                     [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0],
                     [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]])
print('Матрица в ступенчатом виде:')
print(ref(prim_arr), '\n')
print('Матрица в приведённом виде:')
print(rref(prim_arr), '\n')
array = LinearCode(prim_arr)
G = array.g
lead = array.lead
H = array.h
print('G:', G, sep='\n')
print('Результат: ', array.shape_of_g(), '\n')
print('lead: ', lead)
print('H:', H, sep='\n')

checking(G, H)
print('\nd = ', distance(G)[0])
print('t = ', distance(G)[1])
v = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1])
e1 = np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])  # ошибка
e2 = np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1])  # нет ошибки

res = (v + e1) @ H % 2
if np.any(res) > 0:
    print(res, '- ошибка')
else:
    print(res, '- ошибок нет')

res = (v + e2) @ H % 2
if np.any(res) > 0:
    print(res, '- ошибка')
else:
    print(res, '- ошибок нет')
