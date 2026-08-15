mu = 3
scale = 1
n = 200
set.seed(999)
x = rcauchy(n,mu,scale)
#求解mu = 2,首先给定似然函数
dl = function(mu)
{
  return (mean(-2*(x-mu)/(1+(x-mu)^2)))      
}
d2l = function(mu)
{
  return (mean(2/(1+(x-mu)^2)+4*(mu-x)^2/(1+(x-mu)^2)^2))
}
newton = function(f,df,mu0,eps = 10^(-4),max_iter = 100000)
{
  b0 = mu0-1
  b1 = mu0
  it = 0
  while(it<max_iter & abs(f(b0))>eps)
  {
    b0 = b1
    b1 = b0 - f(b0)/df(b0)
    it = it+1
  }
  return(b0)
}
x1=newton(dl,d2l,mu0 = 20000)
x1

