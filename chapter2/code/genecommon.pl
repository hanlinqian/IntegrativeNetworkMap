## usage：perl genecommon.pl edge.txt nodeinfo.txt Zma.wgd.txt
use strict;
use warnings;
my %degree; my $gene1c; my $gene2c;
open IN,"<$ARGV[1]";
my $str=<IN>;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	$degree{$arr[0]}=$arr[3];
}
close IN;
open IN,"<$ARGV[2]";
$str=<IN>;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $overlap = &common($arr[0],$arr[1]);
	print "$arr[0]\t$arr[1]\t";
	if (exists $degree{$arr[0]}){
		print "$degree{$arr[0]}\t";
		$gene1c=$overlap/$degree{$arr[0]};
	}else{
		print "na\t";
		$gene1c="na";
	}
	if (exists $degree{$arr[1]}){
		print "$degree{$arr[1]}\t";
		$gene2c=$overlap/$degree{$arr[1]};
	}else{
		print "na\t";
		$gene2c="na";
	}
	print "$overlap\t$gene1c\t$gene2c\n";
	
}
close IN;
sub common(){
	my $a=$_[0];
	my $b=$_[1];
	my %ha; my %hb; my $i=0;
	open SUBIN,"<$ARGV[0]";
	my $substr=<SUBIN>;
	while ($substr=<SUBIN>){
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
	while (my ($key,$value) =each %ha){
		if (exists $hb{$key}){
			$i++;
		}
	}
	return $i;
}