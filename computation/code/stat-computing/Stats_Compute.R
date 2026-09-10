data = read.csv("exam5.csv")
x = data$x

#Cauchy分布的newton法求解
newton = function(x,mu0 = 3.016682,eps = 10^(-4),max_iter = 200)
{
  f = function(x,mu)
  {
    return (mean(-2*(x-mu)/(1+(x-mu)^2)))      
  }
  df = function(x,mu)
  {
    return (mean(2/(1+(x-mu)^2)+4*(mu-x)^2/(1+(x-mu)^2)^2))
  }
  b0 = mu0-1
  b1 = mu0
  it = 0
  while(it<max_iter & abs(f(x,b0))>eps)
  {
    b0 = b1
    b1 = b0 - f(x,b0)/df(x,b0)
    it = it+1
  }
  return(b0)
}
mu_hat = newton(x)
mu_hat
#Bootstrap法求解
B = 2000
theta.b = function(data,n,B){
  rf = rep(0,B)
  for(b in 1:B)
  {
    xb=sample(data, n, replace=T)
    rf[b]=newton(xb)
  }
  return (rf)
}

mu.b = theta.b(x,n,B)
bias = mean(mu.b)-mu_hat
se = sd(mu.b)
alpha=0.05
theta.hat = mu_hat
theta.se = se
ci1.left =theta.hat-qnorm(1-alpha/2)*theta.se
ci1.right=theta.hat+qnorm(1-alpha/2)*theta.se

ci2.left =quantile(mu.b, alpha/2)
ci2.left
ci2.right=quantile(mu.b, 1-alpha/2)
ci2.right
#JackKnife水手刀法
n = 1000
theta.jack = rep(0,n)
newton(x[-586])
for (i in (1:n)) 
{
  theta.jack[i] = newton(x[-i])
}

bias.jack = (n - 1) * (mean(theta.jack) - theta.hat)
se.jack = ((n - 1) / sqrt(n)) * sd(theta.jack)

#MLE极大似然，bisection,uniroot,Newton