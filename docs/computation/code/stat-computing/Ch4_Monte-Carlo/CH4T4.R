#统计计算第二题误差估计
alpha = 0.05
mu0 = 2
sigma = 1
n = 20
m = 100000
#Monte-Carlo法进行误差估计
mu_mc = function(mu,sigma,m,n)
{
  mu_hat = rep(0,m)
  for(i in (1:m))
  {
    x = rlnorm(n,mu,sigma)
    x_bar = mean(log(x))
    
    if(mu>x_bar+qnorm(alpha/2,0,sigma)/sqrt(n) && mu<x_bar+qnorm(1-alpha/2,0,sigma)/sqrt(n)){
      mu_hat[i] = 1 
    }
    else{
      mu_hat[i] = 0
    }
  }
  hat_mu = mean(mu_hat)
  return (hat_mu) 
}
mu_mc(mu0,sigma,m,n)
set.seed(608)
lambda0 = 50
n = 50
m = 1000
alpha = 0.05
lambda_mc = function(lambda0,m,n,alpha)
{
  lambda_hat = rep(0,m)
  interval = rep(0,m)
  for(i in (1:m))
  {
    x = rpois(n,lambda0)
    lambda = mean(x)
    var_x = mean(x)/n
    lambda_left = lambda + qnorm(alpha/2)*sqrt(var_x)
    lambda_right = lambda + qnorm(1-alpha/2)*sqrt(var_x)
    if(lambda0>lambda_left && lambda0<lambda_right)
    {
      lambda_hat[i] = 1  
    else{
      lambda_hat[i] = 0
    }
    interval[i] = 2*qnorm(1-alpha/2)*sqrt(mean(x)/n)
  }
  return (c(mean(lambda_hat),mean(interval)))
}
lambda_mc(lambda0,m,n,alpha)
s = rep(0,10)
for(i in 1:m){
  s[i] = lambda_mc(lambda0 = 1,m,n,alpha)
}
lambda_mc(lambda0 = 1,m,n,alpha = 0.05)
 #统计计算T4误差检验
m = 1000
n = 20
mu0 = 500
mu = c(seq(400,600,20))
sigma = 100
alpha = 0.05 

M=length(mu)
?t.test
power=rep(0, M)
for (i in 1:M) 
{
  mu1=mu[i]
  pv=rep(0, m)    
  for (j in 1:m) 
  {
    x=rnorm(n, mean=mu1, sd=sigma)
    ttest=t.test(x, alternative="two.sided", mu=mu0)
    pv[j]=ttest$p.value
  }
  power[i]=mean(pv<alpha)
}

# 找到第一类错误率（mu=mu0那一行）
type1_error = power[mu == mu0]
cat("第一类错误经验率 =", round(type1_error,4), "\n")

# 给出效度的计算
print(power)
# 绘图,给出一个经验功效
jpeg("fig3.jpeg", height=800, width=800, quality = 100)
plot(mu, power, type="b", lwd=2, main="t检验功效曲线", xlab=expression(mu), ylab="功效/第一类错误率")
abline(v = mu0, lty = 2, col="red") # H0真值
abline(h = 0.05, lty = 2, col="blue") # alpha水平
dev.off()
