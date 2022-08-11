#### Six different type networks (Slim co-expression network, Co-translation network, Co-expression network with ncRNA, Interactome, Slim-IntegrativeOmics, IntegrativeOmics with ncRNAs) were constructed.  
#### Input files (log-transformed expression matrixs: totalrna-log-rep1.txt, totalrna-log-rep2.txt, ribo-log-rep1.txt, ribo-log-rep2.txt, rnawithnc-exp.txt) for co-expression and co-translation network and input files (edge-proteome-highconf.txt, edge-proteome-lowconf.txt) for Interactome were uploaded into Section0/data. 
#### All final output edge files were stored into NCBI (https://www.ncbi.nlm.nih.gov/geo/) under GEO accession number GSE199932.  
#### Network properties were calculated: node information files (uploaded into Section1/data), module files (uploaded into Section1/data), shortest distance files (in GEO with accession number GSE199932).  
#### Code in this pipeline were uploaded into Section1/code.
### Net1: Slim co-expression network(only containing annotated genes)  
##### step1: calculate soft thresholding  
`module load R/3.6.0;`  
`Rscript softThresholding.r totalrna-log-rep1.txt totalrna-softThresholding-rep1.pdf;`  
`Rscript softThresholding.r totalrna-log-rep2.txt totalrna-softThresholding-rep2.pdf`    
##### step2: sample clustering to detect outliers
`module load R/3.6.0;`  
`Rscript sampletodetectoutliers.r totalrna-log-rep1.txt totalrna-Sampletodetectoutliers-rep1.pdf;`  
`Rscript sampletodetectoutliers.r totalrna-log-rep2.txt totalrna-Sampletodetectoutliers-rep2.pdf`  
##### step3: constrcut co-expression network by WGCNA
`module load R/3.6.0;`  
`Rscript totalrna-edge.r totalrna-log-rep1.txt 18 totalrna-edge-rep1.txt;`  
`Rscript totalrna-edge.r totalrna-log-rep2.txt 12 totalrna-edge-rep2.txt`  
##### step4: obtain overlapped gene-gene pairs as final co-expression network's edges  
`perl network-overlap.pl totalrna-edge-rep1.txt totalrna-edge-rep2.txt >edge-slimcoexpression.txt`   
##### step5: statistics node information
`module load R/3.6.0;`  
`Rscript NetInfo.r edge-slimcoexpression.txt nodeinfo-slimcoexpression.txt sd-slimcoexpression.txt transitivity-slimcoexpression.txt`
##### step6: divide modules
`module load MCL/14-137; mcl edge-slimcoexpression-abc.txt --abc -o module-slimcoexpression.txt`

### Net2: Co-translation network  
##### step1: calculate soft thresholding  
`module load R/3.6.0;`  
`Rscript softThresholding.r ribo-log-rep1.txt ribo-softThresholding-rep1.pdf;` 
`Rscript softThresholding.r ribo-log-rep2.txt ribo-softThresholding-rep2.pdf`  

##### step2: sample clustering to detect outliers
`module load R/3.6.0;`  
`Rscript sampletodetectoutliers.r ribo-log-rep1.txt ribo-Sampletodetectoutliers-rep1.pdf;`  
`Rscript sampletodetectoutliers.r ribo-log-rep2.txt ribo-Sampletodetectoutliers-rep2.pdf`  

##### step3: constrcut co-translation network by WGCNA
`module load R/3.6.0;`  
`Rscript totalrna-edge.r ribo-log-rep1.txt 9 ribo-edge-rep1.txt;`  
`Rscript totalrna-edge.r ribo-log-rep2.txt 21 ribo-edge-rep2.txt` 

##### step4: select overlapped gene pairs as final co-expression network's edges  
`perl network-overlap.pl ribo-edge-rep1.txt ribo-edge-rep2.txt >edge-cotranslation.txt`   
##### step5: statistics node information
`module load R/3.6.0;`  
`Rscript NetInfo.r edge-cotranslation.txt nodeinfo-cotranslation.txt sd-cotranslation.txt transitivity-cotranslation.txt` 
##### step6: divide modules
`module load MCL/14-137; mcl edge-cotranslation-abc.txt --abc -o module-cotranslation.txt`

### Net3: Co-expression network with ncRNA(not only including mRNA, but also lncRNA, small RNA cluster, circRNA, fusionRNA) 
##### step1: construct network by one step
`module load R/3.6.0; Rscript wgcna-edge.r rnawithnc-exp.txt edge-coexpressionwithncrna.txt`  
##### step2: statistics node information
`module load R/3.6.0; Rscript NetInfo.r edge-coexpressionwithncrna.txt nodeinfo-coexpressionwithncrna.txt sd-coexpressionwithncrna.txt transitivity-coexpressionwithncrna.txt`
##### step3: divide modules
`module load MCL/14-137; mcl edge-coexpressionwithncrna-abc.txt --abc -o module-coexpressionwithncrna.txt`

### Net4: Interactome(high confidence and low confidence)  
##### step1: statistics node information
`module load R/3.6.0; Rscript NetInfo.r edge-proteome-highconf.txt nodeinfo-proteome-highconf.txt sd-PPIs-highconf.txt transitivity-PPIs-highconf.txt`  
`module load R/3.6.0; Rscript NetInfo.r edge-proteome-lowconf.txt nodeinfo-proteome-lowconf.txt sd-PPIs-lowconf.txt transitivity-PPIs-lowconf.txt`  
##### step2: divide modules
`module load MCL/14-137; mcl edge-proteome-highconf-abc.txt --abc -o module-proteome-highconf.txt`  
`module load MCL/14-137; mcl edge-proteome-lowconf-abc.txt --abc -o module-proteome-lowconf.txt`  

### Net5: Slim-IntegrativeOmics(high confidence and low confidence)  
##### step1: statistics node information  
Integrates all gene-gene pairs of each omics, ChIA-PET network, slim co-expression network, co-translation network and interactome (high and low confidences). Final output files (edge-slimio-highconf.txt and edge-slimio-lowconf.txt) were uploaded into GEO with accession number GSE199932.
##### step2: statistics node information
`module load R/3.6.0; Rscript NetInfo.r edge-slimio-highconf.txt nodeinfo-slimio-highconf.txt sd-slimio-highconf.txt transitivity-slimio-highconf.txt`  
`module load R/3.6.0; Rscript NetInfo.r edge-slimio-lowconf.txt nodeinfo-slimio-lowconf.txt sd-slimio-lowconf.txt transitivity-slimio-lowconf.txt`  
##### step3: divide modules
`module load MCL/14-137; mcl edge-slimio-highconf-abc.txt --abc -o module-slimio-highconf.txt`  
`module load MCL/14-137; mcl edge-slimio-lowconf-abc.txt --abc -o module-slimio-lowconf.txt`  

### Net6: IntegrativeOmics with ncRNAs(high confidence and low confidence)  
##### step1: statistics node information  
Integrates all gene-gene pairs of each omics, ChIA-PET network, co-expression network with ncRNA, co-translation network and interactome (high and low confidences). Final output files (edge-iowithncrna-highconf.txt and edge-iowithncrna-lowconf.txt) were uploaded into GEO with accession number GSE199932.
##### step2: statistics node information
`module load R/3.6.0;`  
`Rscript NetInfo.r edge-iowithncrna-highconf.txt nodeinfo-iowithncrna-highconf.txt sd-iowithncrna-highconf.txt transitivity-iowithncrna-highconf.txt`  
`Rscript NetInfo.r edge-iowithncrna-lowconf.txt nodeinfo-iowithncrna-lowconf.txt sd-iowithncrna-lowconf.txt transitivity-iowithncrna-lowconf.txt` 
##### step3: divide modules
`module load MCL/14-137; mcl edge-iowithncrna-highconf-abc.txt --abc -o module-iowithncrna-highconf.txt`  
`module load MCL/14-137; mcl edge-iowithncrna-lowconf-abc.txt --abc -o module-iowithncrna-lowconf.txt`  
