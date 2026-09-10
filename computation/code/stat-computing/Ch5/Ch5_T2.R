#Ch5 T2
library(bootstrap)
LSAT = law$LSAT
GPA = law$GPA
n = 15
B = 1000
R = 100
rho_my = function(x,y)
{
  rho = (mean(x*y)-mean(x)*mean(y))/(sqrt(mean(x^2)-(mean(x)^2))*sqrt(mean(y^2)-(mean(y))^2))
  return(rho)
}
rho_my(LSAT,GPA)
#Bootstrap的t置信区间估计
#bootstrap计算方差
set.seed(999)
rho.b = function(X,Y,B)
{
  X = as.matrix(X)
  m = nrow(X)
  data = rep(0,B)
  X = rep(0,m)
  Y = rep(0,m)
  for (b in 1:B)
  {
    j = sample(1:m,size = m, replace = TRUE)
    x = X[j, ]
    y = Y[j, ]
    data[b] = cov(x,y)
  }
  rho = mean(data)
  return (rho)
}
rho.se.b = function(x,y,B,f){
  x = as.matrix(x)
  y = as.matrix(y)
  m = nrow(x)
  th = replicate(B, expr = {
    i = sample(1:m, size = m, replace = TRUE)
    f(x[i, ],y[i, ])
  })
  return (sd(th))
}
rho.t_ci.b = function(X,Y,B = 500,R = 100,level=0.95,statistical){
  X = as.matrix(X)
  Y = as.matrix(Y)
  m = nrow(X)
  stat = rep(0,B)
  se = rep(0,B)
  for (b in 1:B){
    j = sample(1:m, size = m,replace = TRUE)
    x = X[j, ]
    y = Y[j, ]
    stat[b] = statistical(x,y)
    se[b] = rho.se.b(x,y,R,statistical)
  }
  
  stat0 = statistical(X,Y)
  se0 = sd(stat)
  alpha = 1-level
  t.stat = (stat-stat0) / se
  Qt = quantile(t.stat,c(alpha/2,1-alpha/2),type = 1)
  CI = rev(stat0-Qt*se0)
  return(CI)
}
rho_ci = rho.t_ci.b(LSAT,GPA,B,R,statistical= rho_my) 
rho_ci

