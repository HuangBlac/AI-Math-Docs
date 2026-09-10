rm(list = ls())
mu = 0
sigma = 1
n = 100
m = 1000
set.seed(608)
#I,Monte-Carlo进行I型错误率的计算
mc_err = function(alpha,m,n,mu,sigma)
{
  e1 = rep(0,m)
  e2 = rep(0,m)
  for(i in 1:m){
    data = rnorm(n,mu,sd = sqrt(sigma))
    t1 = sqrt(n)*(mean(data)-mu)/sqrt(sigma)
    t2 = sqrt(n)*(mean(data)-mu)/sd(data)
    e1[i] = (abs(t1)>qnorm(1-alpha/2))
    e2[i] = (abs(t2)>qt(1-alpha/2,n-1))
  }
  return (c(mean(e1),mean(e2)))
}
mc_err1 = mc_err(0.1,m,n,mu,sigma)
mc_err2 = mc_err(0.05,m,n,mu,sigma)
mc_err3 = mc_err(0.01,m,n,mu,sigma)
#II,Power效度的计算
power_mc = function(mu0,m,n,mu,sigma)
{
  alpha = 0.05
  power1 = rep(0,m)
  power2 = rep(0,m)
  for(i in 1:m){
    data = rnorm(n,mu0,sd = sqrt(sigma))
    t1 = sqrt(n)*(mean(data)-mu)/sqrt(sigma)
    t2 = sqrt(n)*(mean(data)-mu)/sd(data)
    power1[i] = ( t1 >= qnorm(1-alpha) )
    power2[i] = ( t2 >= qt(1-alpha,n-1) )
  }
  return(c(mean(power1),mean(power2)))
}
power_mc1 = power_mc(0.3,m,n,mu,sigma)
power_mc2 = power_mc(0,m,n,mu,sigma)

