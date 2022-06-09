```perl
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
