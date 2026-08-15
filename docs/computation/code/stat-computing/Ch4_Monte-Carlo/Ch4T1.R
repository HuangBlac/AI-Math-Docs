#Ch4 T1
## X1,X2,\cdots,Xn是n个Cauchy分布，使用X_{[k]}截断均值的均方误差
###(1)生成Cauchy分布
n = 20
X = rcauchy(n,0,1)
print(X)
###(2)生成截尾分布的均方误差
##考虑生成1000个样本
m = 1000
trimmed.mse=function(m, n, k) 
{
  tmean=rep(0, m)
  for (j in 1:m) 
  {
    x=sort(rcauchy(n, 0, 1))
    tmean[j]=mean(x[(k+1):(n-k)])
  }
  mse_cauchy = mean(tmean)  
  return (mse_cauchy)
}
### k =1,2,...,9的均方误差
n = 20
K=n/2-1
mse=rep(0, n/2-1)
for (k in 1:9)
{
 mse[k] = trimmed.mse(m,n,k) 
}
mse

##(3)说明截断误差先
