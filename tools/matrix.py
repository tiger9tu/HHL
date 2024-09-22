import numpy as np

matrix = np.array(
    [
        [2.0, 0.0, 1.0, 0.0],
        [0.0, 3.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, -5.0],
        [0.0, 0.0, -5.0, 0.0],
    ]
)


# 对角化矩阵
diag_matrix, eig_vectors = np.linalg.eig(matrix)
print(diag_matrix)
print(eig_vectors)
