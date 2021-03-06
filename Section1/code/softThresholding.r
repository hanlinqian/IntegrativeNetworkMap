library(WGCNA)
args<-commandArgs(T)
powers1=c(seq(1,10,by=1),seq(12,30,by=2))
datExpr=read.table(args[1],sep="\t",row.names=1,header=T,check.names=F)
datExpr = t(datExpr)
RpowerTable=pickSoftThreshold(datExpr, powerVector=powers1)[[2]]
cex1=0.9
pdf(file=args[2])
par(mfrow=c(1,2))
plot(RpowerTable[,1], -sign(RpowerTable[,3])*RpowerTable[,2],xlab="Soft Threshold (power)",ylab="Scale Free Topology Model Fit,signed R^2",type="n")
text(RpowerTable[,1], -sign(RpowerTable[,3])*RpowerTable[,2], labels=powers1,cex=cex1,col="red")
abline(h=0.85,col="red")
plot(RpowerTable[,1], RpowerTable[,5],xlab="Soft Threshold (power)",ylab="Mean Connectivity", type="n")
text(RpowerTable[,1], RpowerTable[,5], labels=powers1, cex=cex1,col="red")
dev.off()
