function[Q,R]=doublestepQR(H)
[n, ~] = size(H);
Q = eye(n);      
m=n-1;
s=H(m,m)+H(n,n);
t=H(m,m)*H(n,n)-H(m,n)*H(n,m);
x=H(1,1)*H(1,1)+H(1,2)*H(2,1)-s*H(1,1)+t;
y=H(2,1)*(H(1,1)+H(2,2)-s);
z=H(3,2)*H(2,1);
for k=0:n-3
    [v,beta]=householder([x;y;z]);
    q=max(1,k);
    H(k+1:k+3,q:n)=(eye(n)-beta*v*v.')*H(k+1:k+3,q:n);
    r=min(k+4,n);
    H(1:r,k+1:k+3)=H(1:r,k+1:k+3)*(eye(n)-beta*v*v.');
    x=H(k+2,k+3);
    y=H(k+3,k+1);
    if k<n-3
        z=H(k+4,k+1);
    end
end