step1: quality control and remove adapter  
`module load cutadapt/1.9.1;`  
`cutadapt -q 20,20 -o out.fq.gz input.fq.gz;  cutadapt -a AGTCGGAGGCCAAGCGGTCTTAGGAA -o out-rmada.fq.gz --discard-untrimmed -e 0.05 -O 14 --no-indels out.fq.gz;`  
`cutadapt -a "A{10}" --no-trim --untrimmed-o out-rmada-rmpolya.fq.gz -m 15 -e 0 -O 10 --no-indels --max-n 0.1 out-rmada.fq.gz`  
  
step2: filter sequences not in the 18-26nt  
`seqkit seq out.fq.gz -m 18 -M 26 -g -o trim18-26/out.fq.gz;`  
`seqkit fq2fa trim18-26/out.fq.gz -w 0 >01trim18-26/out.fa`
  
step3: Compress into uniq sequence  
`perl uniq.pl 01trim18-26/out.fa >01trim18-26/uniq-out.fa`  
```perl
#This is uniq.pl;
use strict;
use warnings;
my %hb;
open IN,"<$ARGV[0]";
while (my $str1=<IN>){
	chomp $str1;
	my $str2=<IN>;
	chomp $str2;
	if (!exists $hb{$str2}){
		$hb{$str2}=1
	}else{
		$hb{$str2}++;
	}
}
close IN;
my $i=1;
while (my ($key,$value) =each %hb){
	print ">$ARGV[1]-s$i-$value\n";
	print "$key\n";
	$i++;
}
```

step4: remove which mapping to rRNA, tRNA, snRNA, snoRNA sequences and then mapping to genome file  
`module load Bowtie/1.2.2; module load SAMtools/1.7; bowtie -f -a -v 0 -p 1 --un 02rm-nc/rmnc-out.fa bowtie-index/zmnc-idsimple 01trim18-26/uniq-out.fa 02rm-nc/out.bwt 2>02rm-nc/out.log; rm 02rm-nc/out.bwt; bowtie -a -m 1 -f -S -v 0 -p 1 --al 03togenome/align-togenome-out.fa bowtie-1.2.2-index/Zea_mays.AGPv4.dna.toplevel 02rm-nc/rmnc-out.fa 2> 03togenome/out.log | samtools view -@ 1 -b -S -h | samtools sort -@ 1 -o 03togenome/uniq-sort-out.bam`

step5: merge all the bams  
`module load SAMtools/1.7; samtools merge -@ 10 03mergeuniq.bam 03togenome/uniq-sort-out1.bam 03togenome/uniq-sort-out2.bam 03togenome/uniq-sort-out3.bam ...`

step6: bamtobed  
`module load BEDTools/2.27; bedtools bamtobed -cigar -i 03mergeuniq.bam > 03mergeuniq.bed`

step7: Remove low coverage sites (<6x)  
`perl coverage.pl 03mergeuniq.bed >03mergeuniq-6x.bed`  
```perl
#this is coverage.pl;
use strict;
use warnings;
my %hb;
open IN,"<$ARGV[0]";
my $str=<IN>;
my @arr=split /\t/,$str;
my $prechr=$arr[0];
my $pres=$arr[1];
my $pree=$arr[2];
my @arr1=split /-/,$arr[3];
my $num=$arr1[2];
while ($str=<IN>){
	chomp $str;
	@arr=split /\t/,$str;
	@arr1=split /-/,$arr[3];
	if ($arr[0] eq $prechr){
		if ($arr[1] <= $pree){
			$num=$num+$arr1[2];
			if ($arr[2] > $pree){
				$pree=$arr[2];
			}
		}else{
			if ($num >= 6){
				print "$prechr\t$pres\t$pree\t$num\n";
			}
			$pres=$arr[1];
			$pree=$arr[2];
			$num=$arr1[2];
		}
	}else{
		$prechr=$arr[0];
		$pres=$arr[1];
		$pree=$arr[2];
		$num=$arr1[2];
	}
}
close IN;
```

step8: merge adjacent bed to cluster  
`bedtools merge -d 300 -i 03mergeuniq-6x.bed > 03mergeuniq-6x-gap300.bed`  

step9: calculate read counts in each cluster  
`bedtools intersect -a 03mergeuniq.bed -b 03mergeuniq-6x-gap300.bed -wb >cluster-tissues-read.txt;`  
`bedtools intersect -a 03mergeuniq.bed -b 03mergeuniq-6x.bed -wb >highcoverage.bed;`
`perl count.pl >cluster-readcount.txt`  
```perl
#this is count.pl;
use strict;
use warnings;
my %hb; my %node;
open IN,"<highcoverage.bed";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	$node{$arr[3]}=1;
}
close IN;
open IN,"<cluster-tissues-read.txt";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my @arr1=split /-/,$arr[3];
	if (exists $node{$arr[3]}){
		if (!exists $hb{$arr[10]}{$arr1[0]}){
			$hb{$arr[10]}{$arr1[0]}=$arr1[2];
		}else{
			$hb{$arr[10]}{$arr1[0]}=$hb{$arr[10]}{$arr1[0]}+$arr1[2];
		}
	}
}
close IN;
print "gene";
for (my $i=1;$i<=54;$i++){
	print "\tt$i";
}
print "\n";
for (my $c=1;$c<=340479;$c++){
	print "cluster$c";
	my $gene="cluster$c";
	for (my $i=1;$i<=54;$i++){
		my $tissues="t$i";
		if (exists $hb{$gene}{$tissues}){
			print "\t$hb{$gene}{$tissues}";
		}else{
			print "\t0";
		}
	}
	print "\n";
}
```  
  
step10: transfer read counts to TPM
```perl
use strict;
use warnings;
my %hb; my %node;
open IN,"<03mergeuniq-54tissues-6x-gap300.bed";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $len=$arr[2]-$arr[1]+1;
	$hb{$arr[3]}=$len;
}
close IN;
open IN,"<$ARGV[0]";
my $str=<IN>;
print "$str";
chomp $str;
my @id=split /\t/,$str;
while ($str=<IN>){
	%node=();
	chomp $str;
	my @arr=split /\t/,$str;
	my $sum=0; my $n=1;
	while ($id[$n]){
		$node{$n}=$arr[$n]/$hb{$id[$n]};
		$sum=$sum+$node{$n};
		$n++;
	}
	$n=1;
	print "$arr[0]";
	while ($id[$n]){
		my $tpm=$node{$n}/$sum*100000;
		$tpm=sprintf "%.2f",$tpm;
		print "\t$tpm";
		$n++;
	}
	print "\n";
}
close IN;
```
