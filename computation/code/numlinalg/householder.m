%% Householder 变换函数
function [v, beta] = householder(x)
    n = length(x);  % 向量 x 的长度
    eta = max(x);  % 计算 x 的最大值，避免溢出
    sigma = x(2:n).' * x(2:n);  % x(2:n) 部分的平方和
    x = x / eta;  % 对向量 x 进行归一化处理
    v = zeros(n, 1);  % 初始化 v 向量
    
    % 设置 v 向量的第 2 到第 n 个元素
    v(2:n) = x(2:n);
    
    if sigma == 0
        beta = 0;  % 若 x(2:n) 全为零，则 beta 设为 0
    else
        alpha = sqrt(x(1)^2 + sigma);  % 计算 alpha
        if x(1) <= 0
            v(1) = x(1) - alpha;  % 计算 v(1)
        else
            v(1) = -sigma / (x(1) + alpha);  % 计算 v(1)
        end
        beta = 2 * v(1)^2 / (sigma + v(1)^2);  % 计算 beta
    end
end  % 【修改点 1】 结束 householder 函数


%% Householder 分解求解 Ax = b
function x = householdersolve(A, b)
    [m, n] = size(A);  % 获取矩阵 A 的尺寸
    d = zeros(n, 1);  % 用于记录每一步的 beta 值
    
    for j = 1:n
        if j < n  % 进行 Householder 变换的条件
            % 获取当前列向量 A(j:n, j) 从第 j 行开始到最后一行
            x = A(j:n, j);  % 当前列向量
            [v, beta] = householder(x);  % 【修改点 2】 调用 householder 函数，返回 v 和 beta
            
            % 更新 A 的上三角部分
            A(j:n, j:n) = (eye(n-j+1) - beta * v * v.') * A(j:n, j:n);
            
            % 更新 d 向量，用来存储每一列的 beta
            d(j) = beta;
            
            % 更新矩阵 A 的一列，用于消去下三角的元素
            A(j+1:n, j) = v(2:n-j+1);
        end
    end
    
    % 求解 Rx = b，进行回代
    % 由于 A 已经变成了上三角矩阵 R
    % 使用回代求解 x
    for i = n:-1:1
        b(i) = b(i) - A(i, i+1:n) * b(i+1:n);  % 消去上三角部分
        b(i) = b(i) / A(i, i);  % 求解每个 x(i)
    end
    x = b;  % 输出解向量
end  % 【修改点 3】 结束 householdersolve 函数
