#CH3CousrseExercise
m = 10000
N = 1000
set.seed(999)
#1,使用Monte-Carlo模拟法
f = function(x)
{
  return (exp(-x^2)/(1+x))
}
int1 = function(m)
{
  u = runif(m)
  int = mean(f(u))
  return (int)
}
Int1 = int1(m)
#2,使用对偶变量法    
int2 = function(m)
{
  v1 = runif(m/2)
  v2 = 1-v1
  v = c(v1,v2)
  int = mean(f(v))
  return (int)
}
Int2 = int2(m)

g = function(x)
{
  return (exp(-0.5)/(1+x^2))
}
int3 = function(m)
{
  w = runif(m)
  #f为真实函数
  A = f(w)
  #g为一个期望已知的函数
  B = g(w)
  #计算因子c = -cov(A,B)/var(B)
  c  = -cov(A,B)/var(B)
  #int = int(A)+c(g-Eg)
  int = A+c * (g(w) - exp(-0.5)*pi/4)
  return (mean(int))
}
Int3 = int3(m)
?rexp
fg = function(x)
{
  ifelse(x < 1, pi*exp(-x), 0)
}
int4 = function(m)
{
  u = rcauchy(m)
  int = mean(fg(u))
  return (int)
}
Int4 = int4(m)
#3,使用数值模拟的方式计算两种方法的误差

var_mc = function(m,N)
{
  INT1 = rep(0,m)
  INT2 = rep(0,m)
  for(i in 1:m)
  {
    INT1[i] = int1(N)
    INT2[i] = int2(N)
  }
  return (c(var(INT1),var(INT2)))
}
var0 = var_mc(m,N)


      