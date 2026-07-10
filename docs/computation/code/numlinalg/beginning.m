function x = beginning(A,b)
n=3;
A=rand(n,n);
b=rand(n,1);
L=tril(A);
x=b;
[~,n]= size(L);
for j=(1:n)
   x(j)=x(j)/L(j,j);
   x(j+1:n)=x(j+1:n)-x(j)*L(j+1:n,j);
end
end