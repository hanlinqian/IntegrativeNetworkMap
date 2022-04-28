#### Raw data was submitted to GSA(https://ngdc.cncb.ac.cn/gsa/), the accession was CRA006221. Final file was named 21+21srna.tpm in the data directory. The processing pipeline is as follows:
##### step1: quality control and remove adapter  
`module load cutadapt/1.9.1;`  
`cutadapt -q 20,20 -o out.fq.gz input.fq.gz;  cutadapt -a AGTCGGAGGCCAAGCGGTCTTAGGAA -o out-rmada.fq.gz --discard-untrimmed -e 0.05 -O 14 --no-indels out.fq.gz;`  
`cutadapt -a "A{10}" --no-trim --untrimmed-o out-rmada-rmpolya.fq.gz -m 15 -e 0 -O 10 --no-indels --max-n 0.1 out-rmada.fq.gz`  
  
##### step2: filter sequences not in the 18-26nt  
`seqkit seq out.fq.gz -m 18 -M 26 -g -o trim18-26/out.fq.gz;`  
`seqkit fq2fa trim18-26/out.fq.gz -w 0 >01trim18-26/out.fa`
  
##### step3: Compress into uniq sequence  
`perl srnauniq.pl 01trim18-26/out.fa >01trim18-26/uniq-out.fa  ##srnauniq.pl is in the code directory`  

##### step4: remove which mapping to rRNA, tRNA, snRNA, snoRNA sequences and then mapping to genome file  
`module load Bowtie/1.2.2; module load SAMtools/1.7; bowtie -f -a -v 0 -p 1 --un 02rm-nc/rmnc-out.fa bowtie-index/zmnc-idsimple 01trim18-26/uniq-out.fa 02rm-nc/out.bwt 2>02rm-nc/out.log; rm 02rm-nc/out.bwt; bowtie -a -m 1 -f -S -v 0 -p 1 --al 03togenome/align-togenome-out.fa bowtie-1.2.2-index/Zea_mays.AGPv4.dna.toplevel 02rm-nc/rmnc-out.fa 2> 03togenome/out.log | samtools view -@ 1 -b -S -h | samtools sort -@ 1 -o 03togenome/uniq-sort-out.bam`

##### step5: merge all the bams  
`module load SAMtools/1.7; samtools merge -@ 10 03mergeuniq.bam 03togenome/uniq-sort-out1.bam 03togenome/uniq-sort-out2.bam 03togenome/uniq-sort-out3.bam ...`

##### step6: bamtobed  
`module load BEDTools/2.27; bedtools bamtobed -cigar -i 03mergeuniq.bam > 03mergeuniq.bed`

##### step7: Remove low coverage sites (<6x)  
`perl srnacoverage.pl 03mergeuniq.bed >03mergeuniq-6x.bed  ##srnacoverage.pl is in the code directory`  

##### step8: merge adjacent bed to cluster  
`bedtools merge -d 300 -i 03mergeuniq-6x.bed > 03mergeuniq-6x-gap300.bed`  

##### step9: calculate read counts in each cluster  
`bedtools intersect -a 03mergeuniq.bed -b 03mergeuniq-6x-gap300.bed -wb >cluster-tissues-read.txt;`  
`bedtools intersect -a 03mergeuniq.bed -b 03mergeuniq-6x.bed -wb >highcoverage.bed;`
`perl srnacount.pl >cluster-readcount.txt  ##srnacount.pl is in the code directory`  
  
##### step10: transfer read counts to TPM
`perl srnatoTPM.pl 03mergeuniq-6x-gap300.bed clusterinfo.txt >21+21srna.tpm  ##srnatoTPM.pl is in the code directory`
