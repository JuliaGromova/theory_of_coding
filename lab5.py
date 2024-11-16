from itertools import combinations, product
from statistics import mode
import numpy as np


# 1.1 Генерация базиса: двоичные вектора длины cols с обратным порядком битов
def get_basis(cols):
    return [list(c)[::-1] for c in product([0, 1], repeat=cols)]


# 1.2 Функция f: возвращает 1, если u[i] = 0 для всех i из indexes
def f(indexes, u):
    return int(len(indexes) == 0 or np.all(np.asarray(u)[indexes] == 0))


# 1.3 Векторная форма для функции f
def vectorize_f(indexes, size):
    return [f(indexes, b) for b in get_basis(size)]


# 2.1 Порождающая матрица для кода Рида-Маллера
def G_matrix(r, m):
    return np.asarray([vectorize_f(idx, m) for idx in get_all_indexes(r, m)])


# 2.2 Множество H: базисные слова, для которых f равен 1
def H_set(index, m):
    return [u for u in get_basis(m) if f(index, u) == 1]


# 2.3 Дополнение множества индексов index до полного множества
def complementary_indices(indexes, m):
    return [i for i in range(m) if i not in indexes]


# 3.1 Подмножества индексов заданной мощности size
def get_index_combinations(size, m):
    return [list(comb) for comb in combinations(range(m - 1, -1, -1), size)]


# 3.2 Полное множество индексов до мощности r
def get_all_indexes(r, m):
    index_array = []
    for i in range(r + 1):
        index_array.extend(get_index_combinations(i, m))
    return index_array


# 4.1 Функция f с добавлением вектора t
def f_with_t(index, t, m):
    return [int(np.array_equal(np.asarray(b)[index], np.asarray(t)[index])) for b in get_basis(m)]


# 4.2 Мажоритарное декодирование для заданного индекса
def majority_decoding(w, H, idx, m):
    c = complementary_indices(idx, m)
    vote_vectors = [f_with_t(c, u, m) for u in H]
    votes = [np.dot(np.asarray(v), np.asarray(w)) % 2 for v in vote_vectors]
    return mode(votes)


# 5.1 Алгоритм декодирования
def decode_word(word_with_mistake, r, m, G):
    a = np.zeros((G.shape[0]), dtype=int)
    index_array = get_all_indexes(r, m)

    for step in range(r, -1, -1):
        indices = get_index_combinations(step, m)
        first = []
        for idx in indices:
            H = H_set(idx, m)
            first.append(majority_decoding(word_with_mistake, H, idx, m))
        pos = index_array.index(indices[0])

        for i in range(len(first)):
            a[i + pos] = first[i]

        if step != 0:
            word_with_mistake = (a.T @ G + word_with_mistake) % 2
        else:
            word_with_mistake = a.T @ G % 2
        print(f'Слово после шага {abs(step - r - 1)}: {word_with_mistake}')

    return word_with_mistake

def research_RM():
    r, m = 2, 4
    G = G_matrix(r, m)
    print('G: \n', G)
    word = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0])
    print('Исходное слово: ', word)
    crypt_word = word @ G % 2
    print('Отправленное слово: ', crypt_word)
    E = np.eye(16, dtype=int)
    word_with_mistake = (crypt_word + E[4]) % 2
    print('Слово с одной ошибкой: ', word_with_mistake)
    decoded_word = decode_word(word_with_mistake, r, m, G)
    print('Исправленное сообщение: ', decoded_word)
    if np.array_equal(crypt_word, decoded_word):
        print("Отправленное слово и декодированное совпадают.\n")
    else:
        print("Отправленное слово и декодированное не совпадают.\n")

# Основная часть для эксперимента с кодом Рида-Маллера
if __name__ == '__main__':
    research_RM()