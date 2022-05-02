library(WGCNA)
args<-commandArgs(T)
powers1=c(seq(1,10,by=1),seq(12,30,by=2))
datExpr=read.table(args[1],sep="\t",row.names=1,header=T,check.names=F)
datExpr = t(datExpr)
sft <- pickSoftThreshold(datExpr, 
                        powerVector = powers1, 
                        verbose = 5,
                        networkType = "unsigned"
                        )
softPower = sft$powerEstimate
ADJ= adjacency(datExpr,power=softPower)
vis=exportNetworkToCytoscape(ADJ,edgeFile=args[2],threshold = 0.1)