#首先生成一个序列，从0.1开始
x = seq(0.1,2.5,length = 10)
#其次生成一个对应的分布
cdf_norm = function(x,n){
  #生成[0,x]的均匀分布
  u = runif(n,min = 0, max = x)
  #其次生成一系列的服从正态分布的点
  norm_distribution = 1/(sqrt(2*pi))*exp(-1/2*u^2)
  #取均值作为Monte-Carlo积分，还要加上负无穷到0的部分
  cdf = mean(norm_distribution)*x+1/2
  cdf
}
cdf_norm_estimate = sapply(x, cdf_norm,n=1000)
cdf_norm_true = pnorm(x)
print(round(rbind(x,cdf_norm_estimate,cdf_norm_true),3))


