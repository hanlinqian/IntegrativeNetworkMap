####Raw data see , and the final file was named "edge-proteome-lowconf.txt" (in the same directory), the processing flow is as follows:  
step1: bamtofq  
`module load SMRTLink/9.0.0.92188; ccs test.subreads.bam test.fastq.gz ‐‐report‐file test_report.txt ‐‐min‐length 50 ‐‐max‐length 100000 ‐j 20`

step2: fqtofa  
`seqkit fq2fa test.fastq.gz ‐w 0 >test.fa`

step3: Distinguish sequences from AD and BD vector according to ATTL sequence  
`module load BLAST+/2.6.0;  blastn ‐db attl_blastindex/attl_db ‐query test.fa.fa ‐out testattlblast.txt ‐evalue 1.0e‐4 ‐outfmt 6;  perl attl.pl test‐attlblast.txt test.fa BD‐test.fa AD‐test.fa`

step4: Sequences were mapped to CDS region  
`module load BLAST+/2.6.0; makeblastdb ‐in Zea_mays.B73_RefGen_v4.cds.all.fa ‐dbtype nucl ‐parse_seqids ‐out blast‐v4.cds.all.fa;`  
`blastn ‐db blast‐v4.cds.all.fa ‐query BD‐test.fa ‐out BD‐test2cdsblast.txt ‐evalue 1.0e‐4 ‐outfmt 6 ‐num_alignments 1;`  
`blastn ‐db blast‐v4.cds.all.fa ‐query AD‐test.fa ‐out AD‐test2cdsblast.txt ‐evalue 1.0e‐4 ‐outfmt 6 ‐num_alignments 1`

step5: Obtain BD-AD Interactions  
`perl ccs-bd-ad.pl BD‐test2cds‐blast.txt AD‐test2cds‐blast.txt >ccs‐genepairtest.txt`

step6: Obtain unique undirected gene pairs  
`perl genepair-uniq.pl ccs‐genepair‐test.txt > uniqgenepair‐test.txt`
