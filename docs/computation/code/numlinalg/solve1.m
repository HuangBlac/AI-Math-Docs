%LU选列主元法分解
%%LU分解的一般形式
function x=solve1(A,b) 
%%矩阵的LU分解
	L(1:n,1:n)=1;
%%L矩阵情况进行分析
%%利用初等变化来得到矩阵L、U的情况 
for i=(1:n)	
L(i+1:n,i)=A(i,1:i)/A(i,i);
%%找到每列之中最大的元素
  % 如果最大元素不在对角线上，进行行交换
        if max_idx ~= i
            % 交换A的行
            A([i, max_idx], :) = A([max_idx, i], :);
            % 交换b的元素
            b([i, max_idx]) = b([max_idx, i]);
            % 更新置换向量
            P([i, max_idx]) = P([max_idx, i]);
            % 交换L矩阵已计算的部分
            if i > 1
                L([i, max_idx], 1:i-1) = L([max_idx, i], 1:i-1);
            end
        end
        
%%得到上三角阵U，此处仍用A表示
A(i+1:n,i+1:n)=A(i+1:n,i+1:n)-A(i+1:n,i)*L(i+1:n,i);
end
%%下三角矩阵的求解
	y = b;
for i=1:n
    y(i)=b(i);
for j=1:i-1
    y(i)=y(i)-L(i,j)*y(j);
end
end
%%上三角矩阵的求解
	x = y;
for i=n:1
    x(i)=y(i);
    for j=i:n
    x(i)=x(i)-A(i,j)*x(j);
    end
end 
