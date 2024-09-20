import numpy as np

matrix = np.array(
    [
        [0.0, 2.5, 1.0, 0.0],
        [2.5, 0.0, 0.0, 0.0],
        [1.0, 0.0, 2.5, 0.0],
        [0.0, 0.0, 0.0, 2.5],
    ]
)


# 对角化矩阵
diag_matrix, eig_vectors = np.linalg.eig(matrix)
print(diag_matrix, eig_vectors)
