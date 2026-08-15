#Ch4T2
###(1)构造对数正态分布的一个区间估计
alpha = 0.05
mu = 0
sigma = 1
###(2)使用蒙特卡罗方法说明(1)中构造的置信区间的可靠性.
m = 1000
n = 100
count = rep(0, m)
for (j in 1:m)
{
  x = rlnorm(n,mu,sigma)
  mu_hat = mean(log(x))
  sd_hat = sd(log(x))
  left = mu_hat+qt(alpha/2,n-1)*sd_hat/sqrt(n)
  right = mu_hat+qt(1-alpha/2,n-1)*sd_hat/sqrt(n)
  if(mu>left & mu<right)
  {
    count[j] = 1;
  }
}
t = mean(count)
c(1-alpha,t)

