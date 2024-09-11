import numpy as np

matrix0 = np.array(
    [
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0, 0.0],
    ]
)


matrix1 = np.array(
    [
        [0.0, 1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
)

matrix0add1 = matrix0 + matrix1

# 对角化矩阵
diag_matrix, eig_vectors = np.linalg.eig(matrix1)

print("diagnal matrix")
print(diag_matrix)
print("\neigenmatrix")
print(eig_vectors)
