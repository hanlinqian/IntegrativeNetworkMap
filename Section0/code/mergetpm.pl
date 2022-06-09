use strict;
use warnings;
my %hb; my %gene; my $i=0; my @id;
open IN,"<id.txt"; ##all the tissues' name
while (my $str=<IN>){
	chomp $str;
	$id[$i]=$str;
	open IN1,"<hisat+stringtie/$str\_gene_exp.tab";
	my $str1=<IN1>;
	while (my $str1=<IN1>){
		chomp $str1;
		my @arr=split /\t/,$str1;
		my @arr1=split /:/,$arr[0];
		$hb{$arr1[1]}{$str}=$arr[8];
		$gene{$arr1[1]}=1;
	}
	close IN1;
	$i++;
}
close IN;
print "gene";
for (my $n=0;$n<$i;$n++){
	print "\t$id[$n]";
}
print "\n";
while (my ($key,$value)=each %gene){
	print "$key";
	for (my $n=0;$n<$i;$n++){
		if (exists $hb{$key}{$id[$n]}){
			print "\t$hb{$key}{$id[$n]}";
		}else{
			print "\t0";
		}
	}
	print "\n";
}