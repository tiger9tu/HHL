import numpy as np

matrix = np.array(
    [
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0, 0.0],
    ]
)

# 对角化矩阵
diag_matrix, eig_vectors = np.linalg.eig(matrix)

print("diagnal matrix")
print(diag_matrix)
print("\neigenmatrix")
print(eig_vectors)
