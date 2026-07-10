%%上Hessenberge化
function [H,Q] = Hessenberge(A);
 [m, n] = size(A);
    if m ~= n
        error("请输入一个方阵");
    end
Q=eye(n);
for k=1:n-2
    [v,beta]=householder(A(k+1:n,k));
    A(k+1:n,k:n)=(eye(n)-beta*(v)*v.')*A(k+1:n,k:n);
    A(1:n,k+1:n)=A(1:n,k+1:n)*(eye(n)-beta*(v)*v.');
    Q=(eye(n)-beta*(v)*v.')*Q;
end
H=A;