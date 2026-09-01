function res = genSparse(d, s, n, prob0)
    % generate s sparse symmetric matrix as sum of n
    % one sparse matrices
    hash_table = s*ones(1,d);
    res = cell(1,n);
    for i = 1:n
        [res{i}, zeroIndices] = gen1SparseByTable(d, prob0, find(hash_table > 0));
        % the zeroindicates the indices where the one sparse
        % matrix is zero, so the corresponding hash_table 
        % elements with such index does not subtract by 1
        % Example data

        mask = true(1, d); 
        mask(zeroIndices) = false;        
        hash_table(mask) = hash_table(mask) - 1;  
    end
end

function [sm, tab] = gen1SparseByTable(d, prob0, table)

    rows = [];
    cols = [];
    values = [];

    % set the seed tobe time random
    rng('shuffle');
    
    % count how many table elements has bee taken, including zero elements
    count = 0;

    % Repeat until table is empty
    while count < d && ~isempty(table)
        % Randomly select an element 'p' from the table
        p_idx = randi(length(table));
        
        p = table(p_idx);
        
        % Randomly select another element 'q' from the table
        q_idx = randi(length(table));
        q = table(q_idx);
        
        % Generate a random value 'v' between 0 and 1
        v = -1 + 2 * rand;

        iszero = rand < prob0;
        if iszero
            v = 0;
        end
        
        % Assign the value to ensure symmetry: res(p, q) = res(q, p) = v
        rows = [rows, p, q];
        cols = [cols, q, p];
        values = [values, v, v];
        
        % Remove 'p' and 'q' from the table
        if v ~= 0 
            table([p_idx, q_idx]) = [];
        end

        count = count + 1;
        if p ~= 1
            count = count + 1;
        end
        

    end

    % some functions do not support sparse gpuArray
    sm = sparse(rows, cols, values, d,d);
    tab = table;

end