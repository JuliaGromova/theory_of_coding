import itertools
import numpy as np

first_matrix_x = np.array([[1, 1, 1],
                           [1, 1, 0],
                           [1, 0, 1],
                           [0, 1, 1]])


second_matrix_x = np.array([[0, 1, 1, 1, 1, 0, 0],
                            [1, 1, 0, 1, 1, 1, 1],
                            [0, 0, 1, 1, 0, 1, 1],
                            [1, 0, 1, 0, 1, 1, 0]])


# 2.1
def G_matrix(x, k):
    G = np.eye(k, dtype=int)
    G = np.append(G, x, axis=1)
    return G


# 2.2
def H_matrix(x, n, k):
    H = np.copy(x)
    H = np.append(H, np.eye(n - k, dtype=int), axis=0)
    return H


# 2.3
def get_first_table_syndromes(H):
    table_syndromes = dict()
    for i in range(len(H)):
        table_syndromes[str(H[i])] = [i]
    return table_syndromes


# 2.4
def correct_one_mistake(table_syndromes, syndrom, word):
    k = table_syndromes.get(str(syndrom))
    if k is None:
        print("Синдрома нет в таблице синдромов", '\n')
    else:
        word[k] += 1
        word[k] %= 2
    return word


# 2.5
def correct_two_mistake(table_syndromes, syndrom, word):
    k, d = table_syndromes.get(str(syndrom), (-1, -1))
    if k == -1:
        print("Синдрома нет в матрице синдромов")
    if k != -1:
        word[k] += 1
        word[k] %= 2
        if d != -1:
            word[d] += 1
            word[d] %= 2
    return word


# 2.8
def get_second_table_syndromes(H, n):
    table_syndromes = dict()
    mistakes = np.eye(n, dtype=int)
    for i in range(len(H)):
        table_syndromes[str(H[i])] = [i]
    combinations = list(itertools.combinations(range(0, n, 1), 2))
    for combs in combinations:
        mistake = mistakes[combs[0]] + mistakes[combs[1]]
        mistake = mistake @ H % 2
        table_syndromes[str(mistake)] = combs
    return table_syndromes


def part_one():
    print("-------------------------------", '\n', "Часть 1", '\n')
    n = 7
    k = 4
    # 2.1
    G = G_matrix(first_matrix_x, k)
    print("Порождающая матрица G (7,4,3):", '\n', G, '\n')
    # 2.2
    H = H_matrix(first_matrix_x, n, k)
    print("Проверочная матрица H", '\n', H, '\n')
    # 2.3
    table_syndromes = get_first_table_syndromes(H)
    print('Таблица синдромов для однократных ошибок:', table_syndromes, sep='\n')
    # 2.4
    E = np.eye(n, dtype=int)
    true_word = [1, 0, 1, 0]
    print('\nИсходное слово: ', np.array(true_word))
    output_word = np.array(true_word) @ G % 2
    print('Отправленное слово: ', output_word)
    word_with_one_mistake = (output_word + E[5]) % 2
    print('Слово с одной ошибкой: ', word_with_one_mistake)
    syndrom = word_with_one_mistake @ H % 2
    print('Синдром: ', syndrom)
    corrected_word = correct_one_mistake(table_syndromes, syndrom, word_with_one_mistake)
    print('Слово после исправления ошибки: ', corrected_word)
    check_corrected_word = corrected_word @ H % 2
    print("Проверка исправленного слова с помощью умножения на матрицу H: ", check_corrected_word, '\n')
    # 2.5
    E = np.eye(n, dtype=int)
    true_word = [1, 0, 1, 0]
    print('\nИсходное слово: ', np.array(true_word))
    output_word = np.array(true_word) @ G % 2
    print('Отправленное слово: ', output_word)
    word_with_two_mistake = (output_word + E[2] + E[5]) % 2
    print('Слово с двумя ошибками: ', word_with_two_mistake)
    syndrom = word_with_two_mistake @ H % 2
    print('Синдром: ', syndrom)
    corrected_word = correct_one_mistake(table_syndromes, syndrom, word_with_two_mistake)
    print('Слово после исправления ошибки отличается от отправленного: ', corrected_word)
    check_corrected_word = corrected_word @ H % 2
    print("Проверка исправленного слова с помощью умножения на матрицу H: ", check_corrected_word, '\n')


def part_two():
    print("-------------------------------", '\n', "Часть 2", '\n')
    n = 11
    k = 4
    # 2.6
    G = G_matrix(second_matrix_x, k)
    print("Порождающая матрица G (11,4,5):", '\n', G, '\n')
    # 2.7
    H = H_matrix(second_matrix_x, n, k)
    print("Проверочная матрица H", '\n', H, '\n')
    # 2.8
    table_syndromes = get_second_table_syndromes(H, n)
    print('Таблица синдромов:', table_syndromes, sep='\n')
    # 2.9
    E = np.eye(n, dtype=int)
    true_word = [1, 0, 1, 0]
    print('\nИсходное слово: ', np.array(true_word))
    output_word = np.array(true_word) @ G % 2
    print('Отправленное слово: ', output_word)
    word_with_one_mistake = (output_word + E[5]) % 2
    print('Слово с одной ошибкой: ', word_with_one_mistake)
    syndrom = word_with_one_mistake @ H % 2
    print('Синдром: ', syndrom)
    corrected_word = correct_one_mistake(table_syndromes, syndrom, word_with_one_mistake)
    print('Слово после исправления ошибки: ', corrected_word)
    check_corrected_word = corrected_word @ H % 2
    print("Проверка исправленного слова с помощью умножения на матрицу H: ", check_corrected_word, '\n')
    # 2.10
    E = np.eye(n, dtype=int)
    true_word = [1, 0, 1, 0]
    print('\nИсходное слово: ', np.array(true_word))
    output_word = np.array(true_word) @ G % 2
    print('Отправленное слово: ', output_word)
    word_with_two_mistake = (output_word + E[2] + E[5]) % 2
    print('Слово с двумя ошибками: ', word_with_two_mistake)
    syndrom = word_with_two_mistake @ H % 2
    print('Синдром: ', syndrom)
    corrected_word = correct_two_mistake(table_syndromes, syndrom, word_with_two_mistake)
    print('Слово после исправления: ', corrected_word)
    check_corrected_word = corrected_word @ H % 2
    print("Проверка исправленного слова с помощью умножения на матрицу H: ", check_corrected_word, '\n')
    # 2.11
    E = np.eye(n, dtype=int)
    true_word = [0, 1, 1, 0]
    print('\nИсходное слово: ', np.array(true_word))
    output_word = np.array(true_word) @ G % 2
    print('Отправленное слово: ', output_word)
    word_with_three_mistake = (output_word + E[1] + E[3] + E[4]) % 2
    print('Слово с тремя ошибками: ', word_with_three_mistake)
    syndrom = word_with_three_mistake @ H % 2
    print('Синдром: ', syndrom)
    corrected_word = correct_two_mistake(table_syndromes, syndrom, word_with_three_mistake)
    print('Слово после исправления отличается от отправленного: ', corrected_word)
    check_corrected_word = corrected_word @ H % 2
    print("Проверка исправленного слова с помощью умножения на матрицу H: ", check_corrected_word, '\n')


part_one()
part_two()

