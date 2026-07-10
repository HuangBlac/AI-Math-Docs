%%QR分解Householder变换
%%先需要求解的矩阵A
%%接下来求解A=QR的情况
function x=householderfenjie(A,~)
[n,n]=size(A);
d= zeros(n,1);
for j=1:n
    if j<n
        [v,beta] = householder(A(j:n,j));
        A(j:n,j:n)=(eye(n-j+1)-beta*v*v.')*A(j:n,j:n);
        d(j)=beta;
        A(j+1:n,j) = v(2:n-j+1);
    end
end
  for i = n:-1:1
        b(i) = b(i) - A(i, i+1:n) * b(i+1:n);  % 消去上三角部分
        b(i) = b(i) / A(i, i);  % 求解每个 x(i)
    end
    x = b;  % 输出解向量
end
