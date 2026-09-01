function [vec_x] = hhl(mat_A, vec_b, T, t0)

nb = floor(log2(length(vec_b)));
vec_c = zeros(2^T, 1);
vec_c(1) = 1;
vec_c = gpuArray(vec_c / norm(vec_c));

vec_cb = kron(vec_c,vec_b);
vec_cb = vec_cb / norm(vec_cb);


% Hadarmard gates
H = gpuArray([1 1; 1 -1] / sqrt(2));
Hn_unitary = H;
for j = 2:T
    Hn_unitary = kron(Hn_unitary, H);
end

Hn_unitary = kron(Hn_unitary, eye(2^nb));
vec_cb = Hn_unitary * vec_cb;


% controlled unitaries

for j = 1:T
    t = t0 * 2^(j - 1);
    mat_iAt = 1i * mat_A * t;
    mat_expiAt = expm(mat_iAt);
    
    ctrl_set = [0 0; 0 1];
    ctrl_unset = [1 0; 0 0];
    
    c_unitary_set = gpuArray(kron(kron(ctrl_set, eye(2^(j - 1))), mat_expiAt));
    c_unitary_unset = gpuArray(kron(kron(ctrl_unset, eye(2^(j - 1))), eye(2^nb)));

    c_unitary = kron(eye(2^(T - j)), c_unitary_set + c_unitary_unset);

    % apply c_unitary to the system state
    vec_cb = c_unitary * vec_cb;
end

% qft diagger
F = gpuArray(dftmtx(2^T) / sqrt(2^T));
qft_diagger_unitary = kron(F, eye(2^nb));
vec_cb = qft_diagger_unitary * vec_cb;

% controlled rotation
vec_s = [1; 0]; % |0>
vec_scb = kron(vec_s, vec_cb);

for j = 1:2^T-1
    ket_j = zeros(2^T, 1);
    ket_j(j+1) = 1; %% must perform for each number because inverse is not additive
    ket_j_outer = gpuArray(ket_j * ket_j');

    compliment = gpuArray(eye(2^T) - ket_j_outer);
    
    % support for negative eigenvalues
    lambda = 1;
    if(j < 2^(T - 1))
        lambda = j;
    else
        lambda = j - 2^T; % negative eigenvalue
    end
    
    cos = sqrt(1 - 1/lambda^2);
    sin = 1/ lambda;
    rotation = [cos -sin; sin cos];

    c_r_unitary = kron(kron(rotation, ket_j_outer)+ kron(eye(2), compliment), eye(2^nb));
    vec_scb  = c_r_unitary * vec_scb;
end

% post selection
vec_cb = vec_scb(2^(T + nb)+1:end);
vec_cb = vec_cb / norm(vec_cb);

% qpe inverse
qft_unitary = kron(conj(F), eye(2^nb));
vec_cb = qft_unitary * vec_cb;
% controlled unitary diagger
for j = T:-1:1
    t = t0 * 2^(j - 1);
    mat_iAdgt = -1i * mat_A * t;
    mat_expiAdgt = expm(mat_iAdgt);
    
    ctrl_set = [0 0; 0 1];
    ctrl_unset = [1 0; 0 0];
    
    c_unitary_set = kron(kron(ctrl_set, eye(2^(j - 1))), mat_expiAdgt);
    c_unitary_unset = kron(kron(ctrl_unset, eye(2^(j - 1))), eye(2^nb));

    c_unitary = kron(eye(2^(T - j)), c_unitary_set + c_unitary_unset);
    
    % apply c_unitary to the system state
    vec_cb = c_unitary * vec_cb;
end

vec_cb = Hn_unitary * vec_cb;

% return answer
vec_x = vec_cb(1:2^nb);
vec_x = vec_x / norm(vec_x);

end

