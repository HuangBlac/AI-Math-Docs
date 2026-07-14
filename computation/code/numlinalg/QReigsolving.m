 %% implicit QR method
function[]=QReigsolving(A)
[m, n] = size(A);
    if m ~= n
        error("请输入一个方阵");
    end
    H=A;
    Q=eye(n);
for (n~=k)
[H,Q]=Hessenberge(A);
%%将H排列组合为拟上三角矩阵，不可约阵排列组合的形式，筛选出最大的一块进行处理
%%对H22进行双步位移的QR迭代
P=doublestepQR(H22);
Q=P*diag(eye(l),Q,eye(m));
%%将此对角线上|H(i,i-1)|<=(|H(i,i)|+|H(i-1,i-1)|)*u,u=1e(-14)全部置为零
end
%%