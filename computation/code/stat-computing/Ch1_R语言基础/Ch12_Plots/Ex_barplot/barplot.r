######## barplot  ####
library(vcd)
Arthritis

table1=table(Arthritis$Improved)
table1

jpeg("treat1.jpeg", height=760, width=800, quality = 100)
opar=par(mfrow=c(2,2))
barplot(table1, xlab="Improvement", ylab = "Frequency")
barplot(table1, xlab="Improvement", ylab = "Frequency", col=2:4)
barplot(table1, xlab="Improvement", ylab = "Frequency", col=3:5, horiz = T)
par(opar)
dev.off()

table2=table(Arthritis$Improved, Arthritis$Treatment)
table2

jpeg("treat2.jpeg", height=400, width=1000, quality = 100)
opar=par(mfrow=c(1,2))
barplot(table2, main="Stacked Barplot", xlab="Treatment", ylab = "Frequency", 
        col=c("red", "blue", "green"), legend=rownames(table2))
barplot(table2, main="Grouped Barplot", xlab="Treatment", ylab = "Frequency", 
        col=c("red", "blue", "green"), legend=rownames(table2), beside=T)
par(opar)
dev.off()

jpeg("treat3.jpeg", height=400, width=1000, quality = 100)
opar=par(mfrow=c(1,2))
barplot(table2, main="Stacked Barplot", xlab="Treatment", ylab = "Frequency", 
        col=c("coral1", "orange", "yellow"), legend=rownames(table2))
barplot(table2, main="Grouped Barplot", xlab="Treatment", ylab = "Frequency", 
        col=c("blue1", "dodgerblue", "skyblue1"), legend=rownames(table2), beside=T)
par(opar)
dev.off()

