#
f = function(x)
{
  x^3-2*x-5
}
bisection = function(b0,b1,eps=.Machine$double.eps,max_iter=100)
{
  f = function(x)
  {
    x^3-2*x-5
  }
  r = seq(b0,b1,length = 3)
  y = c(f(r[1]),f(r[2]),f(r[3]))
  
  if(y[1]*y[3]>0)
    stop("f不一定有解")
  
  it = 0
  while(it < max_iter & abs(y[2])>eps)
  {
    it = it+1
    
    if(y[1]*y[2]<0)
    {
      r[3] = r[2]
      y[3] = y[2]
    }
    
    else
    {
      r[1] = r[2]
      y[1] = y[2]
    }
    
    r[2] = (r[1]+r[3])/2
    y[2] = f(r[2])
    cat(it,c(r[1],y[1],r[2],y[2],r[3],y[3]),"\n")
  }
  return (list(root = r[2],f.root = y[2],iter = it)) 
}
x0 = bisection(-50,50)
x0$root
x1 = uniroot(f,c(0,5))
x1$root
x2 = polyroot(c(-5,-2,0,1))
x2

newton = function(b0,max_iter= 1000,eps = .Machine$double.eps^0.25)
{
  it = 0
  f = function(x){
    -x^2+x+1/4
  }
  df = function(x){
    -2*x+1
  }
  b1 = b0
  b0 = b0-1 
  while(it < max_iter & f(b1)>f(b0) )
  {
    b0 = b1
    b1 = b0 - f(b0)/df(b0)
    it = it+1
  }
  return (list(root=b0, iter = it))
}
result1 = newton(5*10^166)
result2 = newton(-5*10^99)
result1
result2

#T2(1)
f = function(x){
  return (-x^2+x+1/4)
}
optimize(f,lower = -5,upper = 5, maximum = TRUE)

#T3
lambda0 = 1.2
m=20000
n=200
obj = function(x,lambda)
{
  return(mean(x)/lambda-1)
}
est=rep(0, m)    a
for (i in 1:m) 
{
  x=rpois(n, lambda=lambda0)
  u=uniroot(obj, lower=.001, upper=10e5, x=x)
  lambda.hat=u$root
  est[i]=lambda.hat
}
ML=mean(est)
print(ML)

