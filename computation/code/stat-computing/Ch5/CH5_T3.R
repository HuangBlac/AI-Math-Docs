library(boot)
data = aircondit$hours
lambda_hat = 1/(mean(data))
lambda_hat
#bootstrap估计lambda
#每轮采样的样本数
n = 12
#总采样次数
B = 1000
theta.b = function(data,n,B){
  rf = rep(0,B)
  for(b in 1:B)
  {
    xb=sample(data, n, replace=T)
    rf[b]=1/mean(xb)
  }
  return (rf)
}

lambda.b = theta.b(data,n,B)
bias = mean(lambda.b)-lambda_hat
se = sd(lambda.b)

bias
se
#bootsrap求解1/lambda置信水平位95%的标准正态，百分位数，和基本置信区间
theta = function(x){
  return (mean(x))
}

B=2000
theta.Boot = function(data,theta,B){
  n = length(data)
  theta.Boot = rep(0,B)
  for (b in 1:B) 
  {
    x=sample(data, size=n, replace=TRUE)
    theta.Boot[b]=theta(x)
  }
  return(theta.Boot)
}
theta.hat = theta(data)
theta.b = theta.Boot(data,theta,B)
theta.bias=mean(theta.b)-theta.hat
theta.se=sd(theta.b)
alpha=0.05
ci1.left =theta.hat-qnorm(1-alpha/2)*theta.se
ci1.right=theta.hat+qnorm(1-alpha/2)*theta.se

ci2.left =quantile(theta.b, alpha/2)
ci2.right=quantile(theta.b, 1-alpha/2)

ci3.left =2*theta.hat-quantile(theta.b, 1-alpha/2)
ci3.right=2*theta.hat-quantile(theta.b, alpha/2)
