#Ch2 T1
library(VGAM)
##首先计算F(x)=1-(x/b)^a的逆变换
u = runif(1000)
#a=b=2时
x = (u)^{-1/2}*2
#绘图画出样本的密度直方图并叠加𝑃𝑎𝑟𝑒𝑡𝑜(2, 2)的密度来加以比较.
jpeg(width = 400,height = 400, quality = 100)
# 绘制直方图（概率密度）
hist(x, breaks = 50, prob = TRUE, 
     xlim = c(0, 40), ylim = c(0, 0.3),
     xlab = "x", main = "Pareto(2,2) 密度比较", col = "lightblue")

curve(pareto_density(x, 2, 2), add = TRUE, 
      from = 2, to = 40, col = "red", lwd = 2)

dev.off()
