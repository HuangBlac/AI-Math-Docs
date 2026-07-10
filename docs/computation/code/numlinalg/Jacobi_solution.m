function x = Jacobi_solution(A, b)
    % 获取矩阵大小
    [~, n] = size(A);
    
    % 初始化 L, U, M 矩阵
    L = zeros(n, n);  % 严格下三角部分
    U = zeros(n, n);  % 严格上三角部分
    M = diag(diag(A));  % 对角矩阵
    
    for i = 1:n
        for j = 1:n
            if i > j
                L(i, j) = A(i, j);  % 下三角部分
            elseif i < j
                U(i, j) = A(i, j);  % 上三角部分
            end
        end
    end
    
    % 初始化 x1 和 x2，设初始解为零向量
    x1 = zeros(n, 1);  % 初始解
    x2 = M \ (b - (L + U) * x1);  % 初始迭代结果
    
    % 迭代至误差小于 1e-13
    while max(abs(x2 - x1)) > 1e-13
        x1 = x2;
        x2 = M \ (b - (L + U) * x1);  % 更新迭代解
    end
    
    % 最终解
    x = x2;
end
