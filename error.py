t = int(input())

def check_parity(matrix):
    odd_row = []
    odd_col = []
    for i in range(len(matrix)):
        row_sum = 0
        col_sum = 0
        for j in range(len(matrix[i])):
            row_sum ^= matrix[i][j]
            col_sum ^= matrix[j][i]
        if row_sum == 1:
            odd_row.append(i) 
        if col_sum == 1:
            odd_col.append(i)
    
    if len(odd_row) > 1 or len(odd_col) > 1:
        print("Corrupt")
    elif len(odd_row) == 0 and len(odd_col) == 0:
        print("OK")
    else:
        print("({}, {})".format(odd_row[0]+1, odd_col[0]+1))

matrix_list = []
for t in range(t):
    matrix = []
    n = int(input())
    for i in range(n):
        input_str = input().split()
        for j in range(len(input_str)):
            input_str[j] = int(input_str[j])
        matrix.append(input_str)
    matrix_list.append(matrix)

for matrix in matrix_list:
    check_parity(matrix)



