function totalSum = sumSparse(As)
    % sumSparseMatrices calculates the sum of sparse matrices stored in a cell array
    % Input:
    %   As - a cell array of sparse matrices
    % Output:
    %   totalSum - the sum of all sparse matrices in the cell array
    
    % Ensure the input is a non-empty cell array
    if isempty(As) || ~iscell(As)
        error('Input must be a non-empty cell array of sparse matrices.');
    end
    
    % Initialize the sum as a sparse zero matrix of the same size as the first matrix
    [rows, cols] = size(As{1});
    totalSum = sparse(rows, cols);
    
    % Iterate through the cell array and add each matrix to the total sum
    for i = 1:numel(As)
        if ~issparse(As{i})
            error('All elements in the cell array must be sparse matrices.');
        end
        totalSum = totalSum + As{i};
    end
end
