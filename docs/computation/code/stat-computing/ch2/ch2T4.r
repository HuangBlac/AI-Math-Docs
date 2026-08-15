#T4
#(1)生成n个随机变量，服从对数正态分布
logNorm = function(n,mu,sigma)
{
  x = rnorm(n,mu,sigma)
  y = exp(x)
  y
}

#(2)n=1000，mu = 0, sigma = 1
n = 1000
mu = 0
sigma = 1
y = logNorm(n,mu,sigma)
#(3)画出样本的直方图并叠加对数正态分布的密度函数曲线(提示: 可使用R中\dlnorm"函数).
jpeg(width = 400,height = 400, quality = 100)
# 绘制直方图（概率密度）
hist(y, breaks = 50, prob = TRUE, 
     xlim = c(0, 20), ylim = c(0, 0.7),
     xlab = "y", main = "使用变换法得到的抽样", col = "lightblue")
curve(dlnorm(x),col = "red", add = TRUE, lwd = 2)
dev.off()
