import sympy as sp
# import numpy as np

# 定义变量
epsilon, delta, k = sp.symbols('epsilon delta k', positive = True)
total, qpe, crx, qft, cus, cc, uss, nc, i = sp.symbols('total qpe crx qft cus cc uss nc i')

# 定义额外符号
s_sparse, trotter_reps, trotter_items,tri_const, t0, t0_const,graph_coloring_const, s, one_sparse, one_sparse_const, w_const, logN, c_query, oracle_m, oracle, o_query_const, iter_log_const, tofflike_const,r_controlled, maxh, tr_const, d_const, kappa, k_const= sp.symbols(
    's_sparse trotter_reps trotter_items tri_const t0 t0_const graph_coloring_const s one_sparse one_sparse_const w_const logN c_query oracle_m oracle o_query_const iter_log_const tofflike_const r_controlled maxh tr_const d_const kappa k_const'
)

# 公式定义顺序调整

# # epsilon = 0.1
w_const = 36
o_query_const = 1
# cc = 7
# tr_const = 1
d_const = 1
k_const = 1
# toff_const = 3
iter_log_const = 3 # iterated logarithm, increases so slow that we can use a constant to bound it 
one_sparse_const = 0
tofflike_const = 3
# t0_const = 1
graph_coloring_const = 1


delta = d_const * epsilon / kappa
nc = logN / delta
t0 = 2* 3 # we use simplified version of QPE, t0  - 2pi
oracle_m = o_query_const * iter_log_const * oracle + graph_coloring_const * logN * iter_log_const**2
one_sparse = 2 * (w_const * logN + tofflike_const * logN  + oracle_m) + one_sparse_const # include r-controlled and other, r-controlled is modest so I assume it is small

# k = 2 # k = round ..
m = 6 * s**2 # in the detailed paper , it has to multiply by 6, but we ignore it now
# trotter_step = 2*m *5**(k-1) # less than
# # trotter_reps = tr_const * (i * t0 * maxh)**2 / epsilon # This is not optimal
time = t0 * i
# trotter_reps = 4*5**(k - 1/2)*(m * maxh * time)**(1 + 1/(2*k)) / epsilon**(1/(2*k)) # let k = 1, we do not discuss the case where k > 1 
nexp = 2*m*5**(2*k)*(m*maxh*time)#**(1 + (1/(2*k))) / epsilon**(1/(2*k)) # this is an upper bound
s_sparse = nexp * one_sparse

uss = sp.summation(s_sparse, (i, 1, nc))
cus = 10 * uss
qft = 3 * nc**2
qpe = nc + cus + qft
total = k_const * kappa * (2 * qpe + crx)

# print(nexp)
print(total)
# print(qpe)