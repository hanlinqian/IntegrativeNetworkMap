##### 1. Statistics for Fig. 2b
`perl module.pl module-slimcoexpression.txt module-cotranslation.txt module-proteome-highconf.txt`  
##module.pl was in code folder. Five files of duplicate genes(Zma.$i.txt) and a random pair file, para_random.txt were in data folder. Three module files from three omics were in chapter1/data folder.
##### 2. Statistics for Fig. 2c
`perl duplicate-SD.pl sd-slimcoexpression.txt sd-cotranslation.txt sd-PPIs-highconf.txt`  
##Three shortest distance files from three omics were in XXX.
##### 3. Statistics for Fig. 2d-2g
`for i in $(cat id.txt);do perl genecommon.pl edge-slimcoexpression.txt nodeinfo-slimcoexpression.txt Zma.$i.txt >trans-$i.txt;  done`  
`for i in $(cat id.txt);do perl genecommon.pl edge-cotranslation.txt nodeinfo-cotranslation.txt Zma.$i.txt >ribo-$i.txt; done`   
`for i in $(cat id.txt);do perl genecommon.pl edge-proteome-highconf.txt nodeinfo-proteome-highconf.txt Zma.$i.txt >ppi-$i.txt; done`  
`perl dabsab.pl trans >trans-type.txt`  
`perl dabsab.pl ribo >ribo-type.txt`  
`perl dabsab.pl ppi >ppi-type.txt`   
##edge files were in XXX, node information was in chapter1/data folder, genecommon.pl and dabsab.pl were in code folder and id.txt were in data folder.  
##### 4. Visual code for Fig. 2g and Extended Data Fig. 13
```R
library(ggalluvial)
library(ggplot2)
a <- read.table("wgd-change.txt",header=T,sep="\t") ##wgd-change.txt in data folder
ggplot(a,aes(axis1=trans,axis2=ribo,axis3=ppi))+
  geom_alluvium(aes(fill = trans))+
  geom_stratum()+
  geom_text(stat = "stratum",aes(label = after_stat(stratum)))+
  scale_x_continuous(breaks = 1:3, labels = c("Co-expression", "Co-translation", "Interactome"))+
  theme_bw()+theme(legend.position="none")
```
