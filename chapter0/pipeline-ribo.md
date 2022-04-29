#### Clean data was submitted to GSA(https://ngdc.cncb.ac.cn/gsa/), and accession number was CRA006221. Final average expression file translatome.tpm was in the data directory. The processing pipeline is as follows:  
##### step1: mapping to the genome  
`module load hisat2/2.1.0; module load SAMtools/1.7;`  
`hisat2 -x B73_v4_index --dta -p 8 -U clean_data/$i\.clean.fq.gz | samtools sort -@ 8 -o hisat+stringtie/samtools_$i\_sort.bam`   
`samtools view -@ 8 -b -q 50 hisat+stringtie/samtools_$i\_sort.bam > hisat+stringtie/samtools_$i\_sort_uq.bam;`  

##### step3: calculate gene expression  
`module load StringTie/1.3.0-foss-2016b;`
`stringtie hisat+stringtie/samtools_$i\_sort_uq.bam -p 10 -G cds-AGPv4.40.gtf -e -A hisat+stringtie/$i\_gene_exp.tab; rm hisat+stringtie/samtools_$i\_sort.bam`  

##### step4: merge all the tissues' expression to one file  
`perl mergetpm.pl > 21+21ribo.tpm`  
##The code refers to mergetpm.pl in the code folder, and slightly modified according to the array location.
