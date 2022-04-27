step1: quality control and remove adapter  
`module load cutadapt/1.9.1;

cutadapt -q 20,20 -o 00cutadapt/YYY.fq.gz /public/home/lqhan/B73_interactome_buce/W211108053-smallRNASeq/fq/XXX.fq.gz
cutadapt -a AGTCGGAGGCCAAGCGGTCTTAGGAA -o 00cutadapt/YYY-rmada.fq.gz --discard-untrimmed -e 0.05 -O 14 --no-indels 00cutadapt/YYY.fq.gz; 
cutadapt -a "A{10}" --no-trim --untrimmed-o 00cutadapt/YYY-rmada-rmpolya.fq.gz -m 15 -e 0 -O 10 --no-indels --max-n 0.1 00cutadapt/YYY-rmada.fq.gz`
