##### 1. Statistics for Fig. 2d-2g
`for i in $(cat id.txt);do perl genecommon.pl edge-slimcoexpression.txt nodeinfo-slimcoexpression.txt Zma.$i.txt >trans-$i.txt; perl genecommon.pl edge-cotranslation.txt nodeinfo-cotranslation.txt Zma.$i.txt >ribo-$i.txt; perl genecommon.pl edge-proteome-highconf.txt nodeinfo-proteome-highconf.txt Zma.$i.txt >ppi-$i.txt; done`  
`perl dabsab.pl trans >trans-type.txt; perl dabsab.pl ribo >ribo-type.txt; perl dabsab.pl ppi >ppi-type.txt;`  
##edge files were in XXX, node information was in chapter1/data folder, genecommon.pl code was in data folder; and five files of duplicate genes(Zma.$i.txt) and id.txt were in duplicategenes folder.  
##### 2. Visual code for Fig. 2g and Extended Data Fig. 13
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
