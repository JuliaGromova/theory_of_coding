import numpy as np
import random

# Расширенный код Голея
B = np.array([
    [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
    [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
    [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
    [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]])


# 4.1 Написать функцию формирования порождающей и проверочной матриц расширенного кода Голея (24,12,8).
def G_H(B):
    G = np.hstack((np.eye(12, dtype=int), B))
    H = np.vstack((np.eye(12, dtype=int), B))
    return G, H

# 4.2 Провести исследование расширенного кода Голея для одно-, двух-,трёх- и четырёхкратных ошибок.
def create_errors(word, G, count):
    crypt_word = word @ G % 2
    print(f"\nИсходное слово: {word}")
    print(f"Отправленное слово: {crypt_word}")
    err_positions = random.sample(range(crypt_word.shape[0]), count)
    error = np.zeros(crypt_word.shape[0], dtype=int)
    for index in err_positions:
        error[index] = 1
    word_with_mistake = (crypt_word + error) % 2
    print(f"Слово с {count} кратной ошибкой: {word_with_mistake}")
    return word_with_mistake

def find_mistake(word_with_mistake, H, B):
    s = word_with_mistake @ H % 2
    mistakes = None
    if sum(s) <= 3:
        mistakes = np.array(s)
        mistakes = np.hstack((mistakes, np.zeros(len(s), dtype=int)))
    else:
        for i in range(len(B)):
            temp = (s + B[i]) % 2
            if sum(temp) <= 2:
                mistake_index = np.zeros(len(s), dtype=int)
                mistake_index[i] = 1
                mistakes = np.hstack((temp, mistake_index))
    if mistakes is None:
        sB = s @ B % 2
        if sum(sB) <= 3:
            mistakes = np.hstack((np.zeros(len(s), dtype=int), sB))
        else:
            for i in range(len(B)):
                temp = (sB + B[i]) % 2
                if sum(temp) <= 2:
                    mistake_index = np.zeros(len(s), dtype=int)
                    mistake_index[i] = 1
                    mistakes = np.hstack((mistake_index, temp))
    return mistakes

def correct_mistake(true_word, word_with_mistake, H, B, G):
    mistakes = find_mistake(word_with_mistake, H, B)
    if mistakes is None:
        print("Ошибка обнаружена, исправить невозможно!")
        return
    corrected_word = (word_with_mistake + mistakes) % 2
    print("Исправленное отправленное сообщение:", corrected_word)
    word = true_word @ G % 2
    if not np.array_equal(word, corrected_word):
        print("Сообщение было декодировано с ошибкой!")

# 4.1 - 4.2
def part_one():
    print("-------------------------------\n Часть 1")

    G, H = G_H(B)
    print(f"G:\n{G}\nH:\n{H}")

    word = np.array([i % 2 for i in range(len(G))])

    for i in range(5):
        word_with_mistake = create_errors(word, G, i)
        correct_mistake(word, word_with_mistake, H, B, G)
        print('')

# 4.3 Написать функцию формирования порождающей и проверочных матриц кода Рида-Маллера RM(r, m) на основе параметров r и m.
def G_RM(r, m):
    if 0 < r < m:
        leftup = G_RM(r, m - 1)
        rightlow = G_RM(r - 1, m - 1)
        return np.hstack([np.vstack([leftup, np.zeros((len(rightlow), len(leftup.T)), int)]), \
                          np.vstack([leftup, rightlow])])
    elif r == 0:
        return np.ones((1, 2 ** m), dtype=int)
    elif r == m:
        up = G_RM(m - 1, m)
        low = np.zeros((1, 2 ** m), dtype=int)
        low[0][len(low.T) - 1] = 1
        return np.vstack([up, low])

def H_RM(i, m):
    H = np.array([[1, 1], [1, -1]])
    result = np.kron(np.eye(2 ** (m - i)), H)
    result = np.kron(result, np.eye(2 ** (i - 1)))
    return result

# 4.4. Провести исследование кода Рида-Маллера RM(1,3) для одно- и двукратных ошибок.
# 4.5. Провести исследование кода Рида-Маллера RM(1,4) для одно-, двух-,трёх- и четырёхкратных ошибок.
def research_with_RM(word, G, count, m):
    word_with_mistake = create_errors(word, G, count)
    for i in range(len(word_with_mistake)):
        if word_with_mistake[i] == 0:
            word_with_mistake[i] = -1
    w_t = [word_with_mistake @ H_RM(1, m)]
    for i in range(2, m + 1):
        w_t.append(w_t[-1] @ H_RM(i, m))
    maximum = w_t[0][0]
    index = -1
    for i in range(len(w_t)):
        for j in range(len(w_t[i])):
            if abs(w_t[i][j]) > abs(maximum):
                index = j
                maximum = w_t[i][j]
    counter = 0
    for i in range(len(w_t)):
        for j in range(len(w_t[i])):
            if abs(w_t[i][j]) == abs(maximum):
                counter += 1
            if counter > 1:
                print("Исправить ошибку невозможно.\n")
                return
    corrected_word = list(map(int, list(('{' + f'0:0{m}b' + '}').format(index))))
    if maximum > 0:
        corrected_word.append(1)
    else:
        corrected_word.append(0)
    print(f"Исправленное сообщение: {np.array(corrected_word[::-1])}")


# 4.3 - 4.5
def part_two():
    print("-------------------------------\n Часть 2")
    m = 3
    print(f"\nПорождающая матрица Рида-Маллера (1,3): \n{G_RM(1, m)}\n")
    word = np.array([i % 2 for i in range(len(G_RM(1, m)))])
    for j in range(1, 3):
        research_with_RM(word, G_RM(1, m), j, m)

    m = 4
    print(f"\nПорождающая матрица Рида-Маллера (1,4)\n{G_RM(1, m)}\n")
    word = np.array([i % 2 for i in range(len(G_RM(1, m)))])
    for j in range(1, 5):
        research_with_RM(word, G_RM(1, m), j, m)

if __name__ == '__main__':
    part_one()
    part_two()