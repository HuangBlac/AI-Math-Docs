#Ch5T1
library(bootstrap)
x = law$GPA
y = law$LSAT
rho = function(x,y)
{
  rho = mean(x*y)-mean(x)*mean(y)
  sigmax = sqrt(mean(x^2)-mean(x)^2)
  sigmay = sqrt(mean(y^2)-mean(y)^2)
  return(rho/(sigmax*sigmay))
}

B = 2000
n = length(x)
theta.hat = rho(x,y)
theta.b = numeric(B)

for (b in 1:B) {
  ind = sample(1:n, size = n, replace = TRUE)
  xb = x[ind]
  yb = y[ind]
  theta.b[b] = rho(xb,yb)
}

rho.b = mean(theta.b)
rho.b
se.hat = sd(theta.b)

n = length(x)
theta.jack = numeric(n)
for (i in 1:n) {
  theta.jack[i] = rho(x[-i],y[-i])
}

bias.jack = (n - 1) * (mean(theta.jack) - theta.hat)
se.jack = ((n - 1) / sqrt(n)) * sd(theta.jack)
bias.jack
se.jack