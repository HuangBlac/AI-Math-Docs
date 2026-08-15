#统计计算总复习
## 2.随机变量的构造
###2-1:IT逆变换法生成Pareto随机变量
library(VGAM)
a = 2
b = 2
#生成随机变量的数目
num = 1000
F_inv = function(x,a,b) {
  return ((1-x)^(-1/a)*b)
}

r.target = function(n) {
  u = runif(n)
  x = F_inv(u,a,b)
  return(x)
}
pareto = r.target(num)
print(pareto)
hist(pareto, breaks = 50, prob = TRUE, 
     xlim = c(2, 10), ylim = c(0, 0.6),
     xlab = "x", main = "Pareto(2,2) 密度比较", col = "lightblue")

curve(dpareto(x, 2, 2), add = TRUE, 
      from = 2, to = 40, col = "red", lwd = 2)

dev.off()
###2-2:逆变换法生成离散随机变量
set.seed(999)
F_inv = function(n)
{
  x = rep(0,n)
  uniform = runif(n)
  for(i in 1:n)
  {
    u = uniform[i]
    if(u<0.1)
      x[i] = 0
    else if(u<0.3)
      x[i] = 1
    else if(u<0.5)
      x[i] = 2
    else if(u<0.7)
      x[i] = 3
    else
      x[i] = 4 
  }
  return (x)
}
num = 1000
x_22 = F_inv(num)
x_22
prop.table(table(x_22))
x_22real = sample(0:4,num,replace = T,prob = c(0.1,0.2,0.2,0.2,0.3))
x_22real
prop.table(table(x_22real))
###2-3接受拒绝法生成beta分布
f_beta = function(n,alpha,beta){
  X_beta = rep(0,n)
  k = 1
  m = (alpha-1)/(alpha+beta-2)
  M = m^(alpha-1)*(1-m)^(beta-1)
  while(k <= n){
    u = runif(1)
    x = runif(1)
    x1 = x^(alpha-1)*(1-x)^(beta-1)
    if(u<x1/M)
    {
      X_beta[k] = x
      k = k+1
    }
  }
  return(X_beta)
}
n = 2000
alpha = 3
beta = 2
x_beta = f_beta(n,alpha,beta)
# 绘制直方图（概率密度）
hist(x_beta, breaks = 50, prob = TRUE, 
     xlim = c(0, 1), ylim = c(0, 4.0),
     xlab = "x", main = "beta分布的概率密度", col = "lightblue")
dev.off()
### 2-4trans生成服从对数正态分布的随机样本
myrLNorm = function(n,mu,sigma)
{
  x = rnorm(n,mu,sigma)
  return(exp(x))
}
n = 1000
mu = 0
sigma = 1
x_lognorm = myrLNorm(n,mu,sigma)
hist(x_lognorm, breaks = 50, prob = TRUE, 
     xlim = c(0, 6), ylim = c(0, 1.0),
     xlab = "x", main = "对数正态分布的概率密度", col = "lightblue")
curve(dlnorm(x,0,1),add = TRUE, 
      from = 0, to = 20, col = "red", lwd = 2)
### 2-5混合正态分布
f_mixnorm = function(n,p)
{
  x = sample(0:1,size = n,replace = T,c(1-p,p))
  data = rep(0,n)
  for(i in 1:n){
    if(x[i] == 1)
      data[i] = rnorm(1)
    else
      data[i] = rnorm(1,mean = 3)
  }
  return (data)
}
n = 1000
for(p in c(0.1,0.3,0.5,0.7,0.9)){
  data = f_mixnorm(n,p)
}
## 3.Monte-Carlo求解积分
## 4.Monte-Carlo假设检验
mu = 0
sigma = 2
n = 100
alpha = 0.05
m = 1000
x = rnorm(n,mu,sigma)
theta.mc = function(n,m,mu,sigma,alpha)
{
  t = rep(0,m)
  for(i in 1:m)
  {
    x = rnorm(n,mu,sigma)
    if(sqrt(n)*abs((mean(x)-mu)/sigma)>qnorm(1-alpha/2))
    {
      t[i] = 1     
    }
  }
  return (mean(t))
}
theta.mc = function(n,m,mu,alpha)
{
  t = rep(0,m)
  for(i in 1:m)
  {
    x = rnorm(n,mu,sigma)
    if(sqrt(n)*(mean(x)-mu)/sqrt(var(x))>qt(1-alpha,n-1))
    {
      t[i] = 1     
    }
  }
  return (mean(t))
}
theta.mc(n,m,mu,mu0,alpha)
##经验功效的计算power
power.mc = function(n,m,lambda,lambda0,alpha)
{
  e = rep(0,m)
  for(i in 1:m)
  {
    x = rexp(n,lambda)
    if(sqrt(n)*abs((mean(x)-lambda0)/sqrt(var(x)))>qnorm(1-alpha/2))
    {
      e[i] = 1     
    }
  }
  return (mean(e))
}
power.mc(n = 1000,m,lambda = 1.04,lambda0 = 1,alpha)

## 5boostrap抽样法
mu = 0
sigma = sqrt(2)
n = 1000
x = rnorm(n,mu,sigma)
theta = function(x) {
  # return statistic of x
  sigma.hat = (n-1)*var(x)/n
  return (sigma.hat)
}

B = 2000
n = length(x)
var(x)
theta.hat = theta(x)
theta.b = numeric(B)

for (b in 1:B) {
  ind = sample(1:n, size = n, replace = TRUE)
  xb = x[ind]
  theta.b[b] = theta(xb)
}

bias.hat = mean(theta.b) - theta.hat
se.hat = sd(theta.b)
###JackKnife
library(bootstrap)
y = patch$y
z = patch$z
theta = function(y,z)
{
  theta = mean(y)/mean(z)
  return (theta)
}
B = 2000
n = length(y)
theta.hat = theta(y,z)
theta.b = numeric(B)

for (b in 1:B) {
  ind = sample(1:n, size = n, replace = TRUE)
  yb = y[ind]
  zb = z[ind]
  theta.b[b] = theta(yb,zb)
}

bias.hat = mean(theta.b) - theta.hat
se.hat = sd(theta.b)
alpha = 0.05
# Normal
ci.normal = c(
  theta.hat - qnorm(1 - alpha / 2) * se.hat,
  theta.hat + qnorm(1 - alpha / 2) * se.hat
)

# Percentile
ci.perc = quantile(theta.b, c(alpha / 2, 1 - alpha / 2))

# Basic
q = quantile(theta.b, c(alpha / 2, 1 - alpha / 2))
ci.basic = c(2 * theta.hat - q[2], 2 * theta.hat - q[1])
##
boot.t.ci = function(x, B = 500, R = 100, level = 0.95, statistic) {
  x = as.matrix(x)
  n = nrow(x)
  stat = numeric(B)
  se = numeric(B)
  
  boot.se = function(dat, R, statistic) {
    m = nrow(dat)
    th = replicate(R, {
      ind = sample(1:m, size = m, replace = TRUE)
      statistic(dat[ind, , drop = FALSE])
    })
    sd(th)
  }
  
  for (b in 1:B) {
    ind = sample(1:n, size = n, replace = TRUE)
    xb = x[ind, , drop = FALSE]
    stat[b] = statistic(xb)
    se[b] = boot.se(xb, R = R, statistic = statistic)
  }
  
  stat0 = statistic(x)
  se0 = sd(stat)
  t.stats = (stat - stat0) / se
  alpha = 1 - level
  q = quantile(t.stats, c(alpha / 2, 1 - alpha / 2), type = 1)
  ci = rev(stat0 - q * se0)
  return(ci)
}

## 6.R中的数值求解
### 6-1 Burent二分法
bisection=function(b0, b1, eps=.Machine$double.eps^0.25, iter.max=1000)
{
  f=function(y, a, n) 
  {
    y^2+2*a*y/(n-1)+a^2-n+2
  }
  
  r=seq(b0, b1, length=3)
  y=c(f(r[1], a, n), f(r[2], a, n), f(r[3], a, n))
  
  if (y[1]*y[3]>0)
    stop("f does not have opposite sign at endpoints")
  
  it=0
  while(it<iter.max & abs(y[2])>eps) 
  {
    it=it+1
    
    if (y[1]*y[2]<0) 
    {
      r[3]=r[2]
      y[3]=y[2]
    } 
    else 
    {
      r[1]=r[2]
      y[1]=y[2]
    }
    
    r[2]=(r[1]+r[3])/2
    y[2]=f(r[2], a, n)
    cat(it, c(r[1], r[2], r[3], y[1], y[2], y[3]),"\n")
  }
  return(list(root=r[2], f.root=y[2], iter=it))
}
## 7.MCMC算法
### 7-1生成Rayileh分布的概率密度函数
f = function(x,sigma)
{
  stopifnot(sigma>0)
  if(any(x<0)) return(0)
  return(x/sigma^2*exp(-x^2/(2*sigma^2)))
}
sigma = 2
set.seed(999)
m = 10000
x = rep(0,m)
u = runif(m)
x[1] = rnorm(1)
for(i in 2:m)
{
  xt = x[i-1]
  y = rnorm(1,mean = xt,sd = 1)
  num = f(y,sigma)*dnorm(xt, mean = y)
  den = f(xt,sigma)*dnorm(y, mean = xt)
  alpha = min(1,num / den)
  if(u[i] <= alpha)
  {
    x[i] = y
  }
  else
  {
    x[i] = xt
  }
}
#从马尔科夫链到真实分布
index=(0.2*m+1):m                             
y=x[index]   

a=seq(from=0.005, to=0.995, by=0.01)
QR=sigma*sqrt(-2*log(1-a))  
QM=quantile(y, a)
print(cbind(QR, QM))

jpeg("fig1.jpeg", height=800, width=800, quality = 100)
hist(y, breaks="scott", main="", xlab="", freq=FALSE)
lines(QR, f(QR, sigma=2))
dev.off()

jpeg("fig2.jpeg", height=800, width=800, quality = 100)
qqplot(QR, QM, main="", xlab="Rayleigh Quantiles", ylab="Sample Quantiles")
lines(QR, QR)
dev.off()

### 7-2,使用指数分布来作为提议分布
set.seed(999)
m = 10000
x = rep(0,m)
u = runif(m)
x[1] = rgamma(1,shape = 1)
for(i in 2:m)
{
  xt = x[i-1]
  y = rgamma(1,shape = xt,rate = 1)
  num = f(y,sigma)*dgamma(xt, shape = y,rate = 1)
  den = f(xt,sigma)*dgamma(y, shape = xt,rate = 1)
  alpha = min(1,num / den)
  if(u[i] <= alpha)
  {
    x[i] = y
  }
  else
  {
    x[i] = xt
  }
}
#从马尔科夫链到真实分布
index=(0.2*m+1):m                             
y=x[index]   

a=seq(from=0.005, to=0.995, by=0.01)
QR=sigma*sqrt(-2*log(1-a))  
QM=quantile(y, a)
print(cbind(QR, QM))

jpeg("fig1.jpeg", height=800, width=800, quality = 100)
hist(y, breaks="scott", main="", xlab="", freq=FALSE)
lines(QR, f(QR, sigma=2))
dev.off()

jpeg("fig2.jpeg", height=800, width=800, quality = 100)
qqplot(QR, QM, main="", xlab="Rayleigh Quantiles", ylab="Sample Quantiles")
lines(QR, QR)
dev.off()

###7-3Cauchy distribution
g = function(x)
{
  return (1/(pi*(1+x^2)))
}
set.seed(999)
m=10000
b=10
x=rep(0, m)
x[1]=rnorm(1, mean=0, sd=b)
k=0
#metropolis
b = 2
accepted = 0
for (i in 2:m) {
  cand = rnorm(1, mean = x[i - 1], sd = b)
  alpha = min(1, g(cand) / g(x[i - 1]))
  
  if (runif(1) <= alpha) {
    x[i] = cand
    accepted = accepted + 1
  } else {
    x[i] = x[i - 1]
  }
}

#independence
u=runif(m)
for (i in 2:m) 
{
  xt=x[i-1]
  y=rnorm(1, mean=xt, sd=b)
  num=g(y)
  den=g(xt)
  
  if (u[i]<=num/den) 
  {
    x[i]=y
  }
  else 
  {
    x[i]=xt
    k=k+1     
  }
}
print(k)
print(k/m)

index=(0.4*m+1):m                             
y=x[index]   

a=seq(from=0.005, to=0.995, by=0.01)
QR=qcauchy(a) 
QM=quantile(y, a)
print(cbind(QR, QM))

jpeg("fig9.jpeg", height=800, width=800, quality = 100)
hist(y, breaks="scott", main="", xlab="", freq=FALSE)
lines(QR, dcauchy(QR))
dev.off()

jpeg("fig10.jpeg", height=800, width=800, quality = 100)
qqplot(QR, QM, main="", xlab="Rayleigh Quantiles", ylab="Sample Quantiles")
lines(QR, QR)
dev.off()

