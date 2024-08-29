import numpy as np
from qiskit import QuantumCircuit
from qiskit.synthesis import qs_decomposition
import qiskit.qasm2 as qs2
import itertools
import math

from copy import deepcopy


def find_zero_rows_and_cols(matrix):
    zero_rows = []
    zero_columns = []

    for i, row in enumerate(matrix):
        if np.all(row == 0):
            zero_rows.append(i)

    for j in range(matrix.shape[1]):
        if np.all(matrix[:, j] == 0):
            zero_columns.append(j)

    return zero_rows, zero_columns


# Function to find the index of number
# at first position of kth sequence of
# set of size n
def find_first_num_index(k, n):
    if n == 1:
        return 0, k
    n -= 1

    first_num_index = 0
    # n_actual_fact = n!
    n_partial_fact = n

    while k >= n_partial_fact and n > 1:
        n_partial_fact = n_partial_fact * (n - 1)
        n -= 1
    # First position of the kth sequence
    # will be occupied by the number present
    # at index = k / (n-1)!
    first_num_index = k // n_partial_fact
    k = k % n_partial_fact

    return first_num_index, k


# Function to find the
# kth permutation of n numbers
def find_kth_permutation(s, k):
    # Store final answer
    ans = []
    n = len(s)
    # Subtract 1 to get 0 based indexing
    k = k - 1
    for i in range(n):
        # Mark the first position
        itr = list(s)
        index, k = find_first_num_index(k, n - i)
        # itr now points to the
        # number at index in set s
        ans.append(itr[index])
        # remove current number from the set
        itr.pop(index)
        s = set(itr)
    return ans


# to fill the rest of columns with one, so that Uf is unitary
# permutation is the dictionary order of a perticular ordering
def fill_Uf(half_Uf, permutation=0):
    zero_rows, zero_cols = find_zero_rows_and_cols(half_Uf)
    zero_cols_permuted = find_kth_permutation(zero_cols, permutation)

    Uf = deepcopy(half_Uf)
    for i in range(len(zero_rows)):
        Uf[zero_rows[i], zero_cols_permuted[i]] = 1

    return Uf


def find_optimal_circ(half_Uf, permute_num=0):
    zero_rows, _ = find_zero_rows_and_cols(half_Uf)

    max_permute_num = math.factorial(len(zero_rows))
    if permute_num == 0:
        permute_num = math.factorial(len(zero_rows))
    else:
        permute_num = min(permute_num, max_permute_num)

    optimal_qasm_size = np.Infinity
    optimal_circ = QuantumCircuit()

    for i in range(permute_num):
        Uf = fill_Uf(half_Uf, i)
        circ = qs_decomposition(Uf)
        if i % 100 == 0:
            print(
                "now i = ",
                i,
                "   current size = ",
                circ.size(),
                "   min size = ",
                optimal_qasm_size,
            )
        if circ.size() < optimal_qasm_size:
            optimal_qasm_size = circ.size()
            optimal_circ = circ

    return optimal_circ


# |x>|0> -> |x>|m(x)>
def get_half_Uf11(s1_d1_hermitian):
    size_m = len(s1_d1_hermitian)
    oracle_u = np.zeros((size_m**2, size_m**2), dtype=int)

    for y in range(size_m):
        for x in range(size_m):
            if s1_d1_hermitian[x, y] == 1:
                # [x*size_m + y][x*size_m]
                oracle_u[x * size_m + y, x * size_m] = 1
                break
    return oracle_u


def reduce_Uf11(Uf):
    size_Uf = len(Uf)
    size_H = int(np.sqrt(size_Uf))

    H = np.zeros((size_H, size_H), dtype=int)

    for x in range(size_H):
        y = 0
        for row in range(size_Uf):
            if Uf[row, x * size_H] == 1:
                y = row % size_H
                break
        H[x, y] = 1

    return H


H = np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
half_Uf11 = get_half_Uf11(H)
U = fill_Uf(half_Uf11)
print(U)
# assert np.array_equal(reduce_Uf11(half_Uf11), H)
# opt_circ = find_optimal_circ(half_Uf11, 300)
# qasm_code = qs2.dump(opt_circ, "oracle.qasm2")

# # print(qasm_code)

# print("\n circ size: ", opt_circ.size())
