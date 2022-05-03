use strict;
use warnings;
my %hb; my %node; my %node1;
open IN,"<$ARGV[0]";
my $str=<IN>; 
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	$node{$arr[0]}=1;
	$node{$arr[1]}=1;
}
close IN;
open IN,"<$ARGV[1]";
$str=<IN>; 
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	if (exists $node{$arr[0]}){
		$node1{$arr[0]}=1;
	}
	if (exists $node{$arr[1]}){
		$node1{$arr[1]}=1;
	}
}
close IN;
open IN,"<$ARGV[0]";
$str=<IN>; 
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	if (exists $node1{$arr[0]} && exists $node1{$arr[1]}){
		my $str1="$arr[0]$arr[1]";
		$hb{$str1}=1;
	}
}
close IN;
open IN,"<$ARGV[1]";
$str=<IN>;
print "$str";
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	if (exists $node1{$arr[0]} && exists $node1{$arr[1]}){
		my $str1="$arr[0]$arr[1]";
		my $str2="$arr[1]$arr[0]";
		if (exists $hb{$str1} || exists $hb{$str2}){
			print "$str\n";
		}
	}
}
close IN;