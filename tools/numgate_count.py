import sympy as sp

# n is the size of problem in terms of qubits
# r is the number of bits used to represent real number
# nc is the number of clock qubits
# s is sparsity
# tr is trotter repetitions
# o is the oracle
(n, k, r, nc, ctl, s, tr, o, co, uwo, logstar) = sp.symbols(
    "n k r nc ctl s tr o co uwo logstar", positive=True
)


# this is just my implementation, but the scaling is constant
# we actually need color hamiltonian simulation

cdct = 45 * n + (logstar - 2) * uwo

ocolor = 2 * (2 * uwo + n * 20 + cdct) + co

osh = 2 * uwo + 2 * n * 39 + 2 * r * 18 + 6

csh = osh - 2 * uwo + ocolor
# osh : one sparse hamiltonian simulation
sh = tr * 6 * s**2 * csh

# sh : sparse hamiltonian simulation
qpe = nc * ctl * sh

hhl = k * 2 * qpe


print(hhl)
