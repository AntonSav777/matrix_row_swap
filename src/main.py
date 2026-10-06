n = int(input("Введите количество строк: "))
m = int(input("Введите количество столбцов: "))

matrix = []

for i in range(n):
    row = list(map(float, input(f"Введите строку {i + 1}: ").split()))

    while len(row) != m:
        print(f"Нужно ввести ровно {m} чисел.")
        row = list(map(float, input(f"Введите строку {i + 1}: ").split()))

    matrix.append(row)

max_value = matrix[0][0]
min_value = matrix[0][0]

max_row = 0
min_row = 0

for i in range(n):
    for j in range(m):
        if matrix[i][j] > max_value:
            max_value = matrix[i][j]
            max_row = i

        if matrix[i][j] < min_value:
            min_value = matrix[i][j]
            min_row = i

matrix[max_row], matrix[min_row] = matrix[min_row], matrix[max_row]

print("\nГотовая матрица:")

for row in matrix:
    print(row)
