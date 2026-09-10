state_df=as.data.frame(state.x77)
lm.st  <- lm(Murder~Population+Illiteracy+Income+Frost,data = state_df)
print(lm.st)
summary(lm.st)
?qqplot
?jpeg
residual_murder_lm = residuals(lm.st) 
jpeg(filename = "qqnorm.jpg",width = 400, height = 480, quality = 100)
qqnorm(residual_murder_lm,main = "残差Q-Q正态图")
qqline(residual_murder_lm)
dev.off()
