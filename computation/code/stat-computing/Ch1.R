library(vcd)
Anthritis
?Anthritis
##
table1=table(Arthritis$Improved)
table1

table2=table(Arthritis$Improved, Arthritis$Treatment)
table2

jpeg("mytreat1.jpeg", height=400, width=1000, quality = 100)
opar=par(mfrow=c(1,2))
barplot(table2, main="Stacked Barplot", xlab="Treatment", ylab = "Frequency", 
        col=c("coral1", "orange", "yellow"), legend=rownames(table2))
par(opar)
dev.off()

jpeg("mytreat1.jpeg",height = 400, width=1000, quality = 100)
opar=par(mfrow=c(1,2))
barplot(table2, main="Grouped Barplot", xlab="Treatment", ylab = "Frequency", 
        col=c("blue1", "dodgerblue", "skyblue1"), legend=rownames(table2), beside=T)
par(opar)
dev.off()
