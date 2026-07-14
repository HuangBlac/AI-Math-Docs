%%LU分解的一般形式
function x=solve(A,b)
n=size(A,1);
 if length(b) ~= n
        error('b的长度与原来的不匹配');
 end

% 初始化L,U矩阵
    L = eye(n);
    U = A;
%%矩阵的LU分解

%%L矩阵情况进行分析
%%利用初等变化来得到矩阵L、U的情况 
for i=(1:n-1)	
L(i+1:n,i)=U(i+1:n,i)/U(i,i);
U(i+1:n,i+1:n)=U(i+1:n,i+1:n)-L(i+1:n,i)*U(i,i+1:n);
U(i+1:n,i)=0;
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
for i=n:-1:1
    x(i)=y(i);
    for j=i:n
    x(i)=x(i)-U(i,j)*x(j);
    end
end