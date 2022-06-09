```perl
use strict;
use warnings;
my %hb; my %node;
open IN,"<$ARGV[0]";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $len=$arr[2]-$arr[1]+1;
	$hb{$arr[3]}=$len;
}
close IN;
open IN,"<$ARGV[1]";
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
