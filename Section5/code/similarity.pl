## usage：perl similarity.pl edge.txt nodeinfo.txt traingene-34pos+34neg.txt 5 10
use strict;
use warnings;
my %degree; my $gene1c; my $gene2c; my $ra;
open IN,"<$ARGV[1]";
my $str=<IN>;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	$degree{$arr[0]}=$arr[3];
}
close IN;
open IN,"<$ARGV[2]";
my @traingene; my $n=0;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	$traingene[$n]=$arr[0];
	$n++;
}
close IN;
open IN,"<$ARGV[1]";
my $x;
$str=<IN>;
for ($x=1; $x<$ARGV[3]; $x++){
	$str=<IN>;
}
while ($str=<IN>){
	if ($x > $ARGV[4]){
		last;
	}
	$x++;
	chomp $str;
	my @arr=split /\t/,$str;
	my $a=$arr[0];
	print "$a";
	for (my $j=0;$j<$n;$j++){
		my $b=$traingene[$j];
		my $CN = &common($a,$b);
		my $RA;
		if ($CN > 0){
			$RA=$ra;
		}else{
			$RA="NA";
		}
		my $TN = $degree{$a}+$degree{$b}-$CN;
		my $PA = $degree{$a}*$degree{$b};
		my $Jaccard=$CN/$TN;
		my $HP=$CN/&min($degree{$a},$degree{$b});
		my $HD=$CN/&max($degree{$a},$degree{$b});
		my $sorensen=2*$CN/($degree{$a}+$degree{$b});
		my $LHNI=$CN/$PA;
		if ($a ne $b){
			print "\t$CN\t$RA\t$TN\t$PA\t$HP\t$HD\t$sorensen";
		}else{
			print "\tNA\tNA\tNA\tNA\tNA\tNA\tNA";
		}
	}
	print "\n";
}
close IN;
sub common(){
	my $a=$_[0];
	my $b=$_[1];
	my %ha; my %hb; my $i=0;
	open SUBIN,"<$ARGV[0]";
	my $substr=<SUBIN>;
	while (my $substr=<SUBIN>){
		chomp $substr;
		my @subarr=split /\t/,$substr;
		if ($subarr[0] eq $a){
			$ha{$subarr[1]}=1;
		}
		if ($subarr[1] eq $a){
			$ha{$subarr[0]}=1;
		}
		if ($subarr[0] eq $b){
			$hb{$subarr[1]}=1;
		}
		if ($subarr[1] eq $b){
			$hb{$subarr[0]}=1;
		}
	}
	close SUBIN;
	$ra=0;
	while (my ($key,$value) =each %ha){
		if (exists $hb{$key}){
			$i++;
			$ra=$ra+(1/$degree{$key});
		}
	}
	return $i;
}
sub max(){
	my $a=$_[0];
	my $b=$_[1];
	if ($a > $b){
		return $a;
	}else{
		return $b;
	}
}
sub min(){
	my $a=$_[0];
	my $b=$_[1];
	if ($a < $b){
		return $a;
	}else{
		return $b;
	}
}