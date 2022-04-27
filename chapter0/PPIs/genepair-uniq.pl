use strict;
use warnings;
my %hb;
open IN,"<$ARGV[0]";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my @arr1=split /_/,$arr[1];
	my @arr2=split /_/,$arr[2];
	my $str1="$arr1[0]\t$arr2[0]";
	my $str2="$arr2[0]\t$arr1[0]";
	if (!exists $hb{$str1} && !exists $hb{$str2}){
		$hb{$str1}=1;
	}elsif (exists $hb{$str1}){
		$hb{$str1}++;
	}elsif (exists $hb{$str2}){
		$hb{$str2}++;
	}
}
close IN;
while (my ($key,$value) =each %hb){
	print "$key\t$value\n";
}