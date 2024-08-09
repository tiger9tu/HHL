import numpy as np
from functools import reduce

X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
I = np.eye(2)


def tensor(*matrices):
    result = reduce(np.kron, matrices)
    return result


def get_half_Uf(A, maxi, maxval):
    sizeA = A.shape[0]
    # assert math.sqrt(sizeA).is_integer()
    assert maxval > maxi
    # otherwise we can not make it unitary

    maxx = sizeA
    sizeUf = maxx * maxval
    Uf = np.zeros((sizeUf, sizeUf), dtype=int)

    has_one_rows = np.zeros((sizeUf), dtype=int)

    for c in range(maxx * maxi):
        x = c // maxi % maxx
        i = c % maxi
        found = False
        yi = 0
        e = 0

        rank_nonzero = 0
        for y in range(sizeA):
            if A[x, y] != 0:
                if (rank_nonzero) == i:
                    yi = y
                    e = A[x, y]
                    found = True
                    break
                rank_nonzero += 1

        one_row = 0
        if found:
            one_row = yi * maxval + e
        else:
            one_row = x * maxval

        Uf[one_row, c] = 1
        has_one_rows[one_row] = 1

    return Uf, has_one_rows


# to fill the rest of columns with one, so that Uf is unitary
def fill_Uf(Uf, start_col, has_one_rows, permutation=None):
    sizeUf = Uf.shape[0]

    empty_rows = []
    for row in range(len(has_one_rows)):
        if has_one_rows[row] == 0:
            empty_rows.append(row)

    tmp_empty_rows = []
    if permutation:
        assert len(permutation) == sizeUf - start_col
        for rank in permutation:
            tmp_empty_rows.append(empty_rows[rank])
        empty_rows = tmp_empty_rows

    iter_empty_rows = 0
    for c in range(start_col, sizeUf):
        Uf[empty_rows[iter_empty_rows], c] = 1
        iter_empty_rows += 1

    return Uf


def get_Uf(A, maxi, maxval, permutation=None):
    half_Uf, has_one_rows = get_half_Uf(A, maxi, maxval)
    Uf = fill_Uf(half_Uf, maxi * A.shape[0], has_one_rows, permutation)
    return Uf


def reduce_Uf(Uf, sizeA, maxi, maxval):
    A = np.zeros((sizeA, sizeA), dtype=int)

    row_max_yi = 0
    no_more_val = False

    for c in range(sizeA * maxi):
        x = c // maxi % sizeA
        i = c % maxi

        if i == 0:
            row_max_yi = -1
            no_more_val = False

        # get the row index of one
        for rowUf in range(sizeA * maxval):
            if Uf[rowUf, c] == 1:
                yi = rowUf // maxval % sizeA
                val = rowUf % maxval

                if val != 0:
                    assert not no_more_val, f"x = {x}, i = {i}, yi = {yi}, val = {val}"
                    assert (
                        yi > row_max_yi
                    ), f"x = {x}, i = {i}, yi = {yi}, val = {val}, row_max_yi = {row_max_yi}"
                    A[x, yi] = val
                    row_max_yi = yi
                else:
                    assert x == yi
                    no_more_val = True

    return A


from qiskit.quantum_info import SparsePauliOp

# Uf_as_paulis = SparsePauliOp.from_operator(Uf)
# print(Uf_as_paulis)
# print(Uf_as_paulis.size)

import itertools


def get2x2A(Aconfig):
    A = np.zeros((2, 2), dtype=int)
    A[0, 0] = Aconfig[0]
    A[0, 1] = A[1, 0] = Aconfig[1]
    A[1, 1] = Aconfig[2]
    return A


## find best config:

# at the moment, fix the following super parameters
sizeA = 2
maxi = 2
maxval = 4
sizeUf = 8

# find best config for A
values = [i for i in range(maxval)]
# number of free entry is 3, since A[0,1] == A[1,0]
Aconfigs = list(itertools.product(values, repeat=3))

orders = [i for i in range(sizeUf - maxi * sizeA)]
fillUf_configs = list(itertools.permutations(orders))

configs = list(itertools.product(Aconfigs, fillUf_configs))

least_pauli_num = 99
best_config = None
for config in configs:
    Aconfig, fillUf_config = config
    A = get2x2A(Aconfig)
    Uf = get_Uf(A, maxi, maxval, fillUf_config)
    Uf_as_paulis = SparsePauliOp.from_operator(Uf)
    if Uf_as_paulis.size < least_pauli_num:
        least_pauli_num = Uf_as_paulis.size
        best_config = config

print("least_pauli_num = ", least_pauli_num)

print("best config: ", best_config)

# least_pauli_num =  4
# best config:  ((0, 3, 0), (2, 1, 0, 3))

A = np.array([[0, 3], [3, 0]])
sizeA = A.shape[0]
maxi = 2
maxval = 4
permutation = [2, 1, 0, 3]

# Uf = get_Uf(A, maxi, maxval)
half_Uf, has_one_rows = get_half_Uf(A, maxi, maxval)
Uf = fill_Uf(half_Uf, sizeA * maxi, has_one_rows, permutation)
print(Uf)

rUf = reduce_Uf(Uf, sizeA, maxi, maxval)
assert np.array_equal(rUf, A)

Uf_as_paulis = SparsePauliOp.from_operator(Uf)
print(Uf)

# LCUf = (
#     tensor(I, I, X)
#     + tensor(X, I, X)
#     + np.dot(tensor(i_I, I, I), tensor(Y, I, X))
#     + tensor(Z, I, X),
# )
# print(np.real(LCUf))
# print()
# print(Uf)
