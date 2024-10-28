import random
import numpy as np

def get_table_syndromes(H):
    table_syndromes = dict()
    for i in range(len(H)):
        table_syndromes[str(H[i])] = [i]
    return table_syndromes

def find_index(table_syndromes, syndrom):
    return table_syndromes.get(str(syndrom), [])


def encoding(table_syndromes, syndrom, word):
    k = table_syndromes.get(str(syndrom))
    if k is None:
        print("Синдрома нет в таблице синдромов")
    else:
        word[k] += 1
        word[k] %= 2
    return word

def hemming_matrix(r):
    t = np.array([[int(digit) for digit in format(i, '0' + str(r) + 'b')] for i in range(2 ** r)])
    index = [i for i, row in enumerate(t) if sum(row) <= 1]
    t = np.delete(t, index, axis=0)
    t = np.flip(t, 0)
    G = np.hstack((np.eye(len(t), dtype=int), t))
    H = np.vstack((t, np.eye(r, dtype=int)))
    return G, H


def extend_hemming_matrix(r):
    G, H = hemming_matrix(r)
    H = np.append(H, [np.zeros(len(H.T), dtype=int)], axis=0)
    H = np.append(H, np.ones((len(H), 1), dtype=int), axis=1)
    G = np.append(G, np.zeros((len(G), 1), dtype=int), axis=1)
    for i in range(len(G)):
        if sum(G[i]) % 2 == 1:
            G[i][len(G.T) - 1] = 1
    return G, H


def check_mistakes_hemming(G, H, table_syndromes, r, extend):
    e = np.eye(G.shape[1], dtype=int)
    x = np.random.randint(0, 2, 2**r - r - 1)
    word = x @ G % 2
    if extend:
        number_mistake = 5
    else:
        number_mistake = 4
    for step in range(1, number_mistake):
        print("\nИсходное слово: ", x)
        print("Отправленное слово: ", word)
        index = random.sample(range(0, e.shape[0]), step)
        word_with_mistake = word
        for i in index:
            word_with_mistake = (word_with_mistake + e[i]) % 2
        print("Слово с", step, "кратной ошибкой: ", word_with_mistake)
        syndrom = word_with_mistake @ H % 2
        print("Синдром: ", syndrom)
        corrected_word = encoding(table_syndromes, syndrom, word_with_mistake)
        print("Слово после исправления ошибки: ", corrected_word)
        check_corrected_word = corrected_word @ H % 2
        print("Проверка исправленного слова с помощью умножения на матрицу H: ", check_corrected_word, '\n')


def simple_hemming():
    print("-------------------------------", '\n', "Для кода Хемминга", '\n')
    for r in range(2, 5):
        print("------------------------------- Параметр r = ", r, "-------------------------------", '\n')
        g, h = hemming_matrix(r)
        table_syndromes = get_table_syndromes(h)
        print("G:", g, sep='\n')
        print("H:", h, sep='\n')
        print("Таблица синдромов: ", table_syndromes)
        check_mistakes_hemming(g, h, table_syndromes, r, False)


def extend_hemming():
    print("-------------------------------", '\n', "Для расширенного кода Хемминга", '\n')
    for r in range(2, 5):
        print("------------------------------- Параметр r = ", r, "-------------------------------", '\n')
        g, h = extend_hemming_matrix(r)
        table_syndromes = get_table_syndromes(h)
        print("G:", g, sep='\n')
        print("H:", h, sep='\n')
        print("Таблица синдромов: ", table_syndromes)
        check_mistakes_hemming(g, h, table_syndromes, r, True)


if __name__ == '__main__':
    simple_hemming()
    extend_hemming()