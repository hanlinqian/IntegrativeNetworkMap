#### Raw data was submitted to GSA(https://ngdc.cncb.ac.cn/gsa/), the accession was CRA006221. Final file was named 31+31totalrna.tpm in the data directory. The processing pipeline is as follows:
##### step1: quality control and remove adapter  
`module load SOAPnuke/2.1.6;`  
`SOAPnuke filter -J -T 3 -n 0.1 -q 0.5 -l 12 -1 totalrna/raw-1.fq.gz -2 totalrna/raw-2.fq.gz  -f AAGTCGGAGGCCAAGCGGTCTTAGGAAGACAA  -r AAGTCGGATCGTAGCCATGTCGTTCTGTGAGCCAAGGAGTTG  -o 01SOAPnuke/out -C clean-out_1.fq.gz -D clean-out_2.fq.gz;`    
  
##### step2: mapping to the genome  
`module load hisat2/2.1.0; module load SAMtools/1.7;`  
`hisat2 -x hisat_index/B73_v4_index --dta -p 5 --rna-strandness RF -1 01SOAPnuke/out/clean-out_1.fq.gz -2 01SOAPnuke/out/clean-out_2.fq.gz --known-splicesite-infile hisat_index/B73_splicesites.txt | samtools sort -@ 5 -o hisat+rf/samtools_out_sort.bam;`   
`samtools view -@ 5 -b -q 50 hisat+rf/samtools_out_sort.bam > hisat+rf/samtools_out_sort_uq.bam;`  

##### step3: calculate gene expression  
`module load StringTie/1.3.0-foss-2016b;`
`stringtie hisat+rf/samtools_out_sort_uq.bam -p 5 -G Zea_mays.AGPv4.40.gtf -e -A hisat+rf/out_gene_exp.tab; rm hisat+rf/samtools_out_sort.bam`  

##### step4: merge all the tissues' expression  
`perl mergetpm.pl > 31+31totalrna.tpm  ##mergetpm.pl is in the code directory`
