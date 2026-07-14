%%平方根法
%%LU分解的一般形式
function x=solve2(A,b) 
   % 获取矩阵A的大小
    n = size(A, 1);
    
    % 确保A是方阵
    if size(A, 2) ~= n
        error('不是方阵啊哥');
    end
    
    % 确保b的大小正确
    if length(b) ~= n
        error('b向量长度不对称');
    end
    
    % 检查A是否是对称矩阵
    if ~isequal(A, A')
        error('矩阵不对称');
    end
%%矩阵的平方根法分解;
%%利用初等变化来得到矩阵L的情况 
for i=(1:n)	
A(i,i)=sqrt(A(i,i));
A(i+1:n,i)=A(i+1:n,i)/A(i,i);
for j = i+1:n
    A(j:n,j)=A(j:n,j)-A(j:n,i)*A(j,i);
end
end
%%下三角矩阵的求解
	y = b;
for i=1:n
    y(i)=b(i);
for j=1:i-1
    y(i)=y(i)-A(i,j)*y(j);
end
end
A1=A.';
%%上三角矩阵的求解
	x = y;
for i=n:1
    x(i)=y(i);
    for j=i:n
    x(i)=x(i)-A1(i,j)*x(j);
    end
end 
