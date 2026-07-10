%%全主元分解
function x = fullPivotGauss(A,b)
    [~ , n] = size(A);
    % 初始化行列交换记录
    u = 1:n; % 行交换记录
    v = 1:n; % 列交换记录
for k=1:n-1
% 计算矩阵每个元素的绝对值
absA = abs(A);

% 找到绝对值最大的元素及其线性索引
[~ , linearIndex] = max(absA(:));

% 将线性索引转换为行列坐标
[p, q] = ind2sub(size(A), linearIndex);
        
        p = p + k - 1; % 行交换的实际索引
        q = q + k - 1; % 列交换的实际索引
    %%确定交换矩阵
     % 交换行 p 和 k
        if p ~= k
            A([k, p], :) = A([p, k], :); % 交换矩阵的行
            b([k, p]) = b([p, k]); % 更新右侧向量
            u([k, p]) = u([p, k]); % 更新行交换记录
        end
        
        % 交换列 q 和 k
        if q ~= k
            A(:, [k, q]) = A(:, [q, k]); % 交换矩阵的列
            v([k, q]) = v([q, k]); % 更新列交换记录
        end
    %%消元过程
    if(A(k,k)~=0)
        A(k+1:n,k)=A(k+1:n,k)/A(k,k);
        A(k+1:n,k+1:n)=A(k+1:n,k+1:n)-A(k+1:n,k)*A(k,k+1:n);
        b(k+1:n)=b(k+1:n)-b(k)*A(k+1:n,k);
    else
        stop
    end
end

    % 回代求解
    x = zeros(n, 1);  % 初始化解向量
    x(n) = b(n) / A(n, n);  % 对最后一个元素直接求解
    for k = n-1:-1:1  % 从倒数第二行开始回代
        % 计算当前解，注意维度匹配
        x(k) = (b(k) - A(k, k+1:n) * x(k+1:n)) / A(k, k);  
    end

    % 还原解：根据列交换顺序
    x(v) = x;  % 按照列交换顺序还原解
end
