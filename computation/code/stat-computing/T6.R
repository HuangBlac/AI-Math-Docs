#T6
mu = c(0,1,2)
sigma = matrix(c(1,-0.5,0.5,-0.5,1,-0.5,0.5,-0.5,1),nrow = 3,ncol = 3)
n = 200

##方法一，使用特征值法
rmvn.eigen = function(mu,sigma,n)
{
  d = length(mu)
  ev = eigen(sigma)
  lambda = ev$values
  V = ev$vectors
  R = V %*% diag(sqrt(lambda)) %*% t(V) 
  Z = matrix(rnorm(n*d),nrow = n,ncol = d) 
  X = matrix(mu,n,d, byrow = TRUE)+ Z%*%R
  X
}
X1 = rmvn.eigen(mu,sigma,n)
##方法二，奇异值分解
?svd()
rmvn.svd = function(mu,sigma,n)
{
  d = length(mu)
  svd = svd(sigma)
  lambda = svd$d
  R = svd$u %*% diag(sqrt(lambda)) %*% t(svd$v)
  Z = matrix(rnorm(n*d),nrow = n,ncol = d)
  X = matrix(mu,n,d, byrow = TRUE)+ Z%*%R
  X
}
X2 = rmvn.svd(mu,sigma,n)
?chol

rmvn.Choleski = function(mu, Sigma,n) 
{
  # generate n random vectors from MVN(mu, Sigma) by Choleski
  d = length(mu)
  Q = chol(Sigma)                              
  
  Z = matrix(rnorm(n*d), nrow=n, ncol=d)
  X = Z %*% Q + matrix(mu, n, d, byrow=TRUE)
  X
}
X3 = rmvn.Choleski(mu,sigma,n)
pairs(X1)
pairs(X2)
pairs(X3)
