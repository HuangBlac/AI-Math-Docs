#计算Monte-Carlo积分
n = 1000
m = 500
x = rep(0,m)
for(i in 1:m){
  u = runif(n,0,0.5)
  x[i] = mean(exp(-u))*0.5
}
mean(x)
var1 = var(x)
print(var1)

#(2)指数分布中抽样
x2 = rep(0,m)
for(i in 1:m)
{
  u = rexp(n)
  x2[i] = mean(u<=0.5)
}
mean(x2)
var2 = var(x2) 
var2

##3-2MC方法，估计标准正态分布的分布函数：
f = function(x)
{
  n = 1000
  u = runif(n,0,abs(x))
  y = mean(exp(-1/2*u^2)/(sqrt(2*pi)))*x
  if(x>0)
    return (1/2+y)
  else
    return (1/2-y)
}
f(2)
pnorm(2)
m = 1000
var_mc = function(m){
  x = rep(0,m)
  for (i in 1:m)
  {
   x[i] = f(2) 
  }
  var = var(x)
  return (var)
}
var_mc(m)

##3-3对偶变量的构造方法
n = 100
x1 = runif(n/2)
x2 = 1-x1
dual_mc = function(n)
{
  x = rep(0,n)
  x1 = runif(n/2)
  x2 = 1-x1
  x = c(exp(-x1)/(1+x1^2),exp(-x2)/(1+x2^2))
  return(x)
}
u = runif(n)
mean(exp(-u)/(1+u^2))
int = mean(dual_mc(x1,x2))
int
var_dual = function(m,n)
{
  int = rep(0,m)
  for(i in 1:m)
  {
    int[i] = mean(dual_mc(n))
  }
  var = var(int)
  return(var)
}
m = 1000
var_dual(m,n)

##重要变量法
###int g dx = int g/f fdx
import_MC = function(n)
{
 x = rnorm(n)
 flag = rep(0,n)
 for(i in 1:n)
 {
   flag[i] = (x[i]>=1)
 }
 y = x^2 * flag
 int = mean(y)
 return (int)
}
import_var = function(m,n)
{
  int = rep(0,m)
  for(i in 1:m)
  {
    int[i] = import_MC(n)
  }
  return (var(int))
}
m = 10000
n = 2000