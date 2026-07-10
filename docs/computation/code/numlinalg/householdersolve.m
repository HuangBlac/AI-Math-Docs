%% Householder 分解求解 Ax = b
function x = householdersolve(A, b)
    [m, n] = size(A);  % 获取矩阵 A 的尺寸
    d = zeros(n, 1);  % 用于记录每一步的 beta 值
    
    for j = 1:n
        if j < n  % 进行 Householder 变换的条件
            % 获取当前列向量 A(j:n, j) 从第 j 行开始到最后一行
            x = A(j:n, j);  % 当前列向量
            [v, beta] = householder(x);  % 调用 householder 函数，返回 v 和 beta
            
            % 更新 A 的上三角部分
            A(j:n, j:n) = (eye(n-j+1) - beta * v * v.') * A(j:n, j:n);
            
            % 更新 d 向量，用来存储每一列的 beta
            d(j) = beta;
            
            % 更新矩阵 A 的一列，用于消去下三角的元素
            A(j+1:n, j) = v(2:n-j+1);
        end
    end
    
    % 求解 Rx = b，进行回代
    for i = n:-1:1
        b(i) = b(i) - A(i, i+1:n) * b(i+1:n);  % 消去上三角部分
        b(i) = b(i) / A(i, i);  % 求解每个 x(i)
    end
    x = b;  % 输出解向量
end

