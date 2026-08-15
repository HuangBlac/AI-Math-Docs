getwd()
# 创建x的变量，为x进行赋值
x
x = 1:100
print(x)
# 使用x.txt
write.table(x,"x.txt")
rm(x)
x = read.table("x.txt")
sink("x.txt")
write(x)
sink()
data = read.csv("2015city.csv")
a = rep(1:5,times = 5)
b = rep(1:5,each = 5)
