import sympy as sp

# n is the size of problem in terms of qubits
# r is the number of bits used to represent real number
# nc is the number of clock qubits
# s is sparsity
# tr is trotter repetitions
# o is the oracle
(n, k, r, nc, csh, s, tr, o, co, uwo, logstar, c1, c2, c3, c4, c5) = sp.symbols(
    "n k r nc csh s tr o co uwo logstar c1 c2 c3 c4 c5", positive=True
)


# this is just my implementation, but the scaling is constant
# we actually need color hamiltonian simulation

# deterministic coin tossing
# cdct = 45 * n + (logstar - 2) * uwo

# ocolor = 2 * (2 * uwo + n * 20 + cdct) + co

# osh = 2 * uwo + 2 * n * 39 + 2 * r * 18 + 6

# csh = osh - 2 * uwo + ocolor
# osh : one sparse hamiltonian simulation

# my implementation
logstar = 5
c1 = 2 * 39
c2 = 2 * 18
c3 = 6
c4 = 45
c5 = 1

# We now analyze the time to implement M'.
# It first uses the black box M twice to find y, if it exists.
# It then must use deterministic coin tossing to compute a new label for x,
# and see if it matches with c.
# To do this, we have seen that the coin tossing method requires time
# O(n(lg* n)^2).
# It also requires O(lg* n) black box queries to M, to find up to O(lg* n)
# vertices along the (j,k)-coloured path.
# Note that if we ...
dct = c4 * n + c5 * (logstar) * o

oc = 2 * (2 * o + dct)

csh = 2 * (oc + c1 * n + c2 * r + c3)

u = tr * 6 * s**2 * csh

# u : sparse hamiltonian simulation
# we assume that the power of u is just by repeating u, this helps to
# make error analysis easy
qpe = (2**nc - 1) * u

hhl = k * 2 * qpe


print(hhl)
