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
