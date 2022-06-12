#### The input bam files in step1 of this pipeline are from step2 of pipeline-totalrna.md in section0. Final expression file (21tis-lnc.tpm) and annotation file (lncrna.gff3) were uploaded into section0/data. This pipeline is as follows:
##### step1: obtain new annotation sites  
`module load StringTie/1.3.0-foss-2016b; stringtie hisat+rf/samtools_$i\_sort_uq.bam -o GTF/$i\.gtf -p 2 -G Zea_mays.AGPv4.40.gff3 -l $i`

##### step2: merge all the gtf files by Cufflinks
`cuffmerge -p 8 -g Zea_mays.AGPv4.40.gff3 list.txt -o merged-cuffmerge.gtf`  

##### step3: screen new transcript loci with class code "u" and the number of exon exceeds 1  

##### step4: transfer gtf file to fa file  
`gffread -w merged-select.fa -g Zea_mays.AGPv4.dna.toplevel.fa merged-select.gtf`  

##### step5: identify lncRNAs  
`module load Bowtie2/2.4.4; module load BLAST+/2.7.1; module unload Python/3.6.5; module load Python/2.7.15; module load CPC2/beta; perl LncRNA_Finder2.0.pl -i merged-select.fa -k zmnc-idsimple.fa -o newlnc`  

##### step6: calculate expression of lncRNAs  
`module load StringTie/1.3.0-foss-2016b; stringtie hisat+rf/samtools_$i\_sort_uq.bam -p 3 -G alllincrna.gtf -e -A exp/$i_linc_exp.tab`  

##### step7: merge all the tissues' expression to one file
`perl mergetpm.pl > 21+21lncrna.tpm`  
The code refers to mergetpm.pl in the code folder, and slightly modified according to the array location.
