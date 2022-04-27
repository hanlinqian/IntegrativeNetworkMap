use strict;
use warnings;
my %ccs_gene1; my %ccs_gene2;
open IN,"<$ARGV[0]";
my $str=<IN>;
chomp $str;
my @arr=split /\t/,$str;
$ccs_gene1{$arr[0]}=$arr[1];
while ($str=<IN>){
	chomp $str;
	my @arr1=split /\t/,$str;
	if ($arr[0] ne $arr1[0]){
		@arr=@arr1;
		$ccs_gene1{$arr[0]}=$arr[1];
	}
}
close IN;
open IN,"<$ARGV[1]";
$str=<IN>;
chomp $str;
@arr=split /\t/,$str;
if (exists $ccs_gene1{$arr[0]}){
	$ccs_gene2{$arr[0]}=$arr[1];
}
while ($str=<IN>){
	chomp $str;
	my @arr1=split /\t/,$str;
	if ($arr[0] ne $arr1[0] && exists $ccs_gene1{$arr1[0]}){
		@arr=@arr1;
		$ccs_gene2{$arr[0]}=$arr[1];
	}
}
close IN;
while (my ($key,$value) =each %ccs_gene2){
	print "$key\t$ccs_gene1{$key}\t$ccs_gene2{$key}\n";
}