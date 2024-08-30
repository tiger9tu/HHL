import sympy as sp
# import numpy as np

# 定义变量
total, qpe, crx, qft, cus, cc, uss, nc, i = sp.symbols('total qpe crx qft cus cc uss nc i')

# 定义额外符号
s_sparse, trotter_reps, t0, epsilon, s, one_sparse, w_const, nx, c_query, oracles, o_query_const, maxh, tr_const = sp.symbols(
    's_sparse trotter_reps t0 epsilon s one_sparse w_const nx c_query oracles o_query_const maxh tr_const'
)

# 公式定义顺序调整

epsilon = 0.1
w_const = 70
o_query_const = 7

one_sparse = 2 * (w_const * nx + o_query_const * oracles)
trotter_reps = tr_const * (i * t0 * maxh)**2 / epsilon
s_sparse = trotter_reps * s**2 * one_sparse
uss = sp.summation(s_sparse, (i, 1, nc))
cus = cc * uss
qft = cc * nc**2
qpe = qft + cus
total = 2 * qpe + crx


print(total)