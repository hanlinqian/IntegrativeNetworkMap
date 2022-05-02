library(WGCNA)
datExpr=read.table("totalrna-log-rep1.txt",sep="\t",row.names=1,header=T,check.names=F)
datExpr = t(datExpr)
beta1=18
ADJ= adjacency(datExpr,power=beta1)
vis=exportNetworkToCytoscape(ADJ,edgeFile="totalrna-edge-rep1.txt",threshold = 0.1)
