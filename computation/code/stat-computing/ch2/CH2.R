X=rnorm(100000)
Y=rnorm(100000)

Z=c()
system.time({
  for(i in 1:100000)
  {
    Z=c(Z, X[i]+Y[i]) 
  }
})


Z=rep(0, 100000)
system.time({
  for(i in 1:100000)
  {
    Z[i]=X[i]+Y[i]
  }
})


system.time({
  Z=X+Y
})


