use strict;
use warnings;
my $in=$ARGV[0];
my $out=$ARGV[1];
my %hb;
open IN,"<$in";
while (my $str=<IN>){
	chomp $str;
	$hb{$str}=1;
}
close IN;
my %node;
open IN,"<edge-slimio-lowconf.txt";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	if (exists $hb{$arr[0]} || exists $hb{$arr[1]}){
		$node{$arr[0]}=1;
		$node{$arr[1]}=1;
	}
}
close IN;
open IN,"<edge-slimio-lowconf.txt";
open OUT,">$out";
print OUT "source\ttarget\tweight\n";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	if (exists $node{$arr[0]} && exists $node{$arr[1]}){
		print OUT "$arr[0]\t$arr[1]\t$arr[6]\n";
	}
}
close IN;