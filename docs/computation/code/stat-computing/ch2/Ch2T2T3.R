n = 1000

X1 = function(n)
{
  k = 1
  X1 = numeric(n)
  while(k <= n){
    u = runif(1)
    if(u<0.1){
      X1[k] = 0
    }
    else if(0.1<=u && u<0.3){
      X1[k] = 1
    }
    else if(u>=0.3 && u < 0.5){
      X1[k] = 2
    }
    else if(u>=0.5 && u < 0.7 ){
      X1[k] = 3
    }
    else{
      X1[k] = 4
    }
    k = k + 1
  }
  return (X1)
}
X1(n/2)

X2 = sample(0:4, n, replace = TRUE, prob = c(0.1, 0.2, 0.2, 0.2, 0.3))


#(3)构造一个频数表, 比较理论概率和经验概率
freq_table1 <- table(X1)
print(freq_table1/1000)
freq_table2 = table(X2)
print(freq_table2/1000)a


#T3 beta分布的ar接受拒绝法构造样本

X_beta <- function(num_beta, alpha, beta) {
  if(alpha <= 1 || beta <= 1){
    stop("该函数只适用于 alpha>1, beta>1")
  }
  
  x_beta <- numeric(num_beta)
  k <- 1
  
  mode <- (alpha - 1) / (alpha + beta - 2)
  M <- dbeta(mode, alpha, beta)
  
  while(k <= num_beta){
    y <- runif(1)
    u <- runif(1)
    #y,u<f(y)/cg(y),其中选取c让这个式子总小于等于1，f为目标分布,g为测试分布，对于有限的情况往往选取均匀分布
    if(u <= dbeta(y, alpha, beta)/M){
      x_beta[k] <- y
      k <- k + 1
    }
  }
  
  return(x_beta)
}
#生成1000个服从(3,2)beta分布的样本点
alpha = 3
beta = 2
num_beta = 2000

x = X_beta(num_beta,alpha,beta)
y = rbeta(num_beta,alpha,beta)
t = mean(x)-mean(y)
#画出直方图
jpeg(width = 400,height = 400, quality = 100)
# 绘制直方图（概率密度）
hist(X_beta, breaks = 50, prob = TRUE, 
     xlim = c(0, 2), ylim = c(0, 3),
     xlab = "x", main = "beta分布的概率密度", col = "lightblue")
dev.off()


