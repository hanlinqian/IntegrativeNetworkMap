library(WGCNA)
args<-commandArgs(T)
datExpr=read.table(args[1],sep="\t",row.names=1,header=T,check.names=F)
datExpr = t(datExpr)
beta1=args[2]
ADJ= adjacency(datExpr,power=beta1)
vis=exportNetworkToCytoscape(ADJ,edgeFile=args[3],threshold = 0.1)
