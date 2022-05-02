library(WGCNA)
datExpr=read.table("ribo-log-rep2.txt",sep="\t",row.names=1,header=T,check.names=F)
datExpr = t(datExpr)
beta1=21
ADJ= adjacency(datExpr,power=beta1)
vis=exportNetworkToCytoscape(ADJ,edgeFile="ribo-edge-rep2-0.05.txt",threshold = 0.05)
vis=exportNetworkToCytoscape(ADJ,edgeFile="ribo-edge-rep2-0.01.txt",threshold = 0.01)
