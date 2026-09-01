function [eps] = epsA(As,t,r)
    A = full(sumSparse(As)); 
    troExpA = trotter(As,t,r); 
    eigs = eig(troExpA);
    if any(eigs < 0)
        error('negative eigenvalue in trotter.');
    end
    troA = logm(troExpA);
    eps = norm(-1i * troA  / t - A, 2);
end