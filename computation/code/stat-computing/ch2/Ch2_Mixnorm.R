p = 0.8
n = 1000
mu1 = c(1:3)
mu2 = rep(0,3)
sigma1 = matrix(data = c(1,0,0,1),nrow= 2,ncol = 2)
sigma2 = matrix(data = c(2,0.5,0.5,2),nrow = 2,ncol = 2)
rmvn.eigen = function(n, mu, Sigma) 
{
  # generate n random vectors from MVN(mu, Sigma) by spectral decomposition
  d = length(mu)                                 ## dimension
  ev = eigen(Sigma, symmetric = TRUE)            ## spectral decomposition
  lambda = ev$values                            
  V = ev$vectors                                
  R = V %*% diag(sqrt(lambda)) %*% t(V)
  
  Z = matrix(rnorm(n*d), nrow = n, ncol = d)
  X = Z %*% R + matrix(mu, n, d, byrow = TRUE)
  X
}
mixnorm = function(mu1,sigma1,mu2,sigma2,n,p)
{
  m = length((mu1))
  x1 = rmvn.eigen(n*p,mu1,sigma1)
  x2 = rmvn.eigen(n*(1-p),mu2,sigma2)
  x = rbind(x1,x2)
  return(x)
}
y = mixnorm(mu1,sigma1,mu2,sigma2,n,p)
mu = apply(y, 2, mean)
Sigma = cov(y)
mu
p=0.8
n = 1000
mu = c(0,5)
sigma = 1
my_mixnorm = function(n,p,mu,sigma)
{
  x1 = rnorm(n * p+1,mu[1],sigma)
  x2 = rnorm(n * (1-p),mu[2],sigma)
  return(c(x1,x2))
}
data = my_mixnorm(n,p,mu,sigma)
mean(data)
var(data)
mu_alpha_mc= function(n,m,p,mu,mu0,sigma,alpha)
{
  alpha_hat = rep(0,m)
  for(i in 1:m)
  {
    x = my_mixnorm(n,p,mu,sigma)
    left = mean(x)+sd(x)/sqrt(n)*qnorm(alpha/2)
    right = mean(x)+sd(x)/sqrt(n)*qnorm(1-alpha/2)
    if(mu0>left && mu0<right)
    {
      alpha_hat[i] = 1
    }
  }
  return (mean(alpha_hat))
}
mu_alpha_mc(n,m,p = 0.99,mu,mu0 = 0,sigma,alpha = 0.05)
