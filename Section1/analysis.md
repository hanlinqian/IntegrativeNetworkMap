##### 1. Visual code for Fig. 1e 
```R
##R
library(UpSetR)
a <- read.table("hub-node.txt",header = T,sep = "\t",check.names = F) ##hub-node.txt was in Section1/data
upset(a, queries = list(list(query=intersects, params="Co-expression",color="#CC5700", active=T),list(query=intersects, params="Co-translation",color="#3464A8", active=T),list(query=intersects, params="Interactome",color="#349824", active=T),list(query=intersects, params=list("Co-expression","Co-translation"),color="#EA9F00", active=T),list(query=intersects, params=list("Co-expression","Interactome"),color="#FC9E95", active=T),list(query=intersects, params=list("Co-translation","Interactome"),color="#72303E", active=T),list(query=intersects, params=list("Co-expression","Co-translation","Interactome"),color="#FF85FF", active=T)))
```
##### 2. Visual code for Extended Data Fig. 2b
```R
##R
library(ComplexHeatmap)
a <- read.table("heatmap-mrna.txt",header = T,sep = "\t",check.names = F,row.names = 1) ##heatmap-mrna.txt in data folder
Heatmap(a,cluster_rows = T,cluster_columns = T,show_column_names = F,show_row_names = F)
```
##### 3. Visual code for Extended Data Fig. 2c
```R
##R
library(ggplot2)
a <- read.table("ribo-tisnum.txt",header = T) ##ribo-tisnum.txt was in Section1/data
ggplot(a,aes(x=ribonum))+geom_density()+theme_bw()+labs(x="Number of tissues with expressed elements")
```
##### 4. Code for Extended Data Fig. 5
```R
library(ggplot2)
lib = read.table("lib1.txt",sep="\t",header=T) ##lib1.txt was in Section1/data
mmModel = nls(PPIs~Vm*Screens/(K+Screens),data=lib,start=list(Vm=30000, K=30))
summary(mmModel) ##estimated maximum
## figure
lib["Fitted"] = fitted(mmModel,c(1:10))
ggplot(lib,aes(x = Screens,y = PPIs))+geom_point()+geom_errorbar(aes(ymin = PPIs-sd, ymax = PPIs+sd))+geom_line(aes(x=Screens,y=Fitted))+labs(x="Number of Screens of Lib1", y="Cumulative number of PPIs")+theme_classic()
```
##### 5. Code for Extended Data Fig. 7a,7b
```R
library(ggplot2)
data <- read.table("test-corexp.txt",header = T,sep = "\t") ##test-corexp.txt was in Section1/data
ggplot(data, aes(x=rep1, y=rep2))+
	stat_density_2d(aes(fill = ..density..), geom = "raster", contour = FALSE)+
	scale_fill_gradient2(low = 'gray', high = 'red', midpoint = 0.08,limits=c(0,0.2))+
	scale_x_continuous(limits = c(0, 9), expand = c(0, 0))+
	scale_y_continuous(limits = c(0, 9), expand = c(0, 0))+
	theme(legend.position='none')
cor(data$rep1,data$rep2) ##calculate correlation
```
