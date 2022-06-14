##### Statistics and visual code for Fig. 3b and Extended Data Fig. 14
step1:  
`awk -F '\t' '{if ($2==1) print $0}' 00sbicolor_maize-omics.txt |cut -d " " -f 8-10 >1.txt` ##Obtain information of chromosome1  
step2:  
`perl slindingwindow.pl 10 100 >chr1.txt` ##slindingwindow.pl Section3/code and 00sbicolor_maize-omics Section3/data  
step3: 
```R
##figure by R, ##chr1.txt was in data folder
a <- read.table("chr1.txt",header = T,sep = "\t")
a$omics <- factor(a$omics, levels = c("Co-expression","Co-translation","Interactome"))
ggplot(a,aes(x=id,y=per,color=type))+
	geom_point(size=0.5)+
	geom_smooth(formula = y ~ x,method="loess",size=1.5)+
	scale_color_manual(values=c("#E7B800", "#2E9FDF"))+
	labs(x="Gene order along Sorghum bicolor chr1",y="Proportion of dominant subgenome in a bin")+
	facet_grid(.~omics,as.table=F)+
	theme_bw()+theme(legend.position = "none")
```
