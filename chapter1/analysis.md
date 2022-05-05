##### 1. Visualization code for Fig. 1e 
```R
library(UpSetR)
a <- read.table("hub-node.txt",header = T,sep = "\t",check.names = F) ##hub-node.txt in data folder
upset(a, queries = list(list(query=intersects, params="Co-expression",color="#CC5700", active=T),list(query=intersects, params="Co-translation",color="#3464A8", active=T),list(query=intersects, params="Interactome",color="#349824", active=T),list(query=intersects, params=list("Co-expression","Co-translation"),color="#EA9F00", active=T),list(query=intersects, params=list("Co-expression","Interactome"),color="#FC9E95", active=T),list(query=intersects, params=list("Co-translation","Interactome"),color="#72303E", active=T),list(query=intersects, params=list("Co-expression","Co-translation","Interactome"),color="#FF85FF", active=T)))
```
