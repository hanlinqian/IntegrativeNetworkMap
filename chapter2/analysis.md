##### 1. Code for Fig. 2d-2g
`for i in $(cat id.txt);do perl genecommon.pl edge-slimcoexpression.txt nodeinfo-slimcoexpression.txt Zma.$i.txt >trans-$i.txt; done`  
`for i in $(cat id.txt);do perl genecommon.pl edge-cotranslation.txt nodeinfo-cotranslation.txt Zma.$i.txt >ribo-$i.txt; done`  
`for i in $(cat id.txt);do perl genecommon.pl edge-proteome-highconf.txt nodeinfo-proteome-highconf.txt Zma.$i.txt >ppi-$i.txt; done`  
##id.txt is written to dispersed, proximal, tandem, transposed, and wgd 5 lines; edge files were in XXX, node information was in chapter1/data folder, and genecommon.pl code was in data folder.
