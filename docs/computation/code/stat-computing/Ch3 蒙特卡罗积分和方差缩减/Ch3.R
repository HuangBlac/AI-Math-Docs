#Ch3T1,T3
##T1,MonteCarlo估计积分\int_0^1 exp(-x)dx
###(1)使用均匀分布来进行估计
n = 100
u = runif(n,min = 0,max = 0.5)
x = exp(-u)
theta1 = 0.5*mean(x)
var1 = var(x)/n
###(2)使用指数分布来进行估计
u_exp = rexp(n)
theta2 = mean(u_exp<0.5)
var2 = (1-theta2)*(theta2)/n
###(3)比较两个估计量的方差
var1
var2

##T3,构造对偶变量计算Monte-Carlo积分
N = 100
U = runif(N/2)
V = 1 - U 
x= c(exp(-U)/(1+U^2),exp(-V)/(1+V^2))
theta = mean(x)
var = var(x)/N
print(theta)
print(var)

##T4重要抽样法求Monte-Carlo integeration:\int_1^{\infty}\frac{x^2}{\sqrt{2\pi}}exp(-x^2/2)dx
f = function(x) {
  x^2*exp(-x^2/2)/(sqrt(2*pi)) * (x>1)
}

p1 = pnorm(1)                # Φ(1) ≈ 0.8413447
tail_prob = 1 - p1           # 1-Φ(1) ≈ 0.1586553
u = runif(n)
x = qnorm(p1+(1-p1)*u)
fg = f(x)/(exp(-1/2*x^2)/sqrt(2*pi))*tail_prob
X_int = mean(fg)
print(X_int)
