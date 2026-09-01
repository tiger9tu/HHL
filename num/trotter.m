function [eiAt] = trotter(As,t,r)
% As is a cell list of one sparse matrices, As sum up to A 
% t is the time for evolution, r is the number
% of repetitions
n = length(As);
eiAt = eye(length(As{1}));

for j = 1:n
    eiAt = eiAt * expm(1i * As{j} * (t / r));
end

eiAt = eiAt^r;

