#### The clean data obtained after preliminary processing of the original data by SOAPnuke and FastUniq software was submitted to GSA(https://ngdc.cncb.ac.cn/gsa/, accession number: CRA006221). Final output expression file (21tis-circ.tpm) and annotation file (circ.gff3) were uploaded into section0/data.
##### step1: build genome index  
`module load Bowtie/1.2.2; bowtie-build Zea_mays.AGPv4.dna.toplevel.fa bowtie-1.2.2-index/Zea_mays.AGPv4.dna.toplevel`

##### step2: map to genome by TopHat
`module load Tophat/2.1.1; module load Python/2.7.15; module load Bowtie/1.1.2-foss-2016b;`  
`mkdir 01CIRCexplorer2/$i;cd 01CIRCexplorer2/$i;`  
`tophat2 -o fusion-$i -p 10 --fusion-search --keep-fasta-order --bowtie1 --no-coverage-search Zea_mays.AGPv4.dna.toplevel uniq-$i-1.fq.gz uniq-$i-2.fq.gz;`

##### step3: identify circRNA and calculate read count by CIRCexplorer2  
`module load SAMtools/1.9; samtools index -b tophat-fusion/fusion-$i/accepted_hits.bam ##build bam index`  
`CIRCexplorer2 parse --pe -t TopHat-Fusion fusion-$i/accepted_hits.bam > CIRCexplorer2_parse-$i.log;`  
`CIRCexplorer2 annotate -r b734.40/4.40.gpd -g Zea_mays.AGPv4.dna.toplevel.fa -b back_spliced_junction.bed -o circularRNA_known-$i.txt; ##start position of bed file is 0 while gff3 file is 1`

##### step4: merge all the tissues' read count to one file  
`perl mergetpm.pl > 21+21circrna.tpm`  ##mergetpm.pl refers to Section0/code/mergetpm.pl with slight modifications

##### step5: transfer read count to TPM(CPM)  
According to the formula of CPM, CPM= A/mapped reads*1000000 (A is the read count mapped to a gene).
