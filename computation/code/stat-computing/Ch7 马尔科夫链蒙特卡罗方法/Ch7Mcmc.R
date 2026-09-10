m = 10000
xt = rep(0,m)
xt[1] = rt(1,2)
y = rt(m,2)
u = runif(m)
for(i in 2:m)
{
  fy = dcauchy(y[i])*dt(xt[i-1],2)
  fx = dcauchy(xt[i-1])*dt(y[i],2)
  r = fy/fx
  if(u[i]<r)
  {
    xt[i] = y[i] 
  }
  else
  {
    xt[i] = xt[i-1]
  }
}
hist(xt[(0.4*m+1):m],main = "",xlab = "p",prob=TRUE)
qqplot(
  qcauchy(ppoints(length(xt[(0.4*m+1):m]))),
  sort(xt[0.4*m+1:m])
)
abline(0,1,col=2)
z = xt[()]