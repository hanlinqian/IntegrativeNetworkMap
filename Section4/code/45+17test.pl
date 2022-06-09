use strict;
use warnings;
my %hb; my %train; my %test; my %node;
open IN,"<$ARGV[0]";
while (my $str=<IN>){
	chomp $str;
	$hb{$str}=1;
}
close IN;
my $i=1;
while (my ($key,$value) =each %hb){
	if ($i<=45){
		$train{$key}=1;
	}else{
		$test{$key}=1;
	}
	$i++;
}
open IN,"<edge-slimio-lowconf.txt";
my $str=<IN>;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	if (exists $train{$arr[0]} || exists $train{$arr[1]}){
		$node{$arr[0]}=1;
		$node{$arr[1]}=1;
	}
}
close IN;
$i=0;
while (my ($key,$value) =each %node){
	if (exists $test{$key}){
		$i++;
	}
}
my $per=$i/17*100;
print "$per\n";