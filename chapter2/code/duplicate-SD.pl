##usge: perl duplicate-SD.pl sd-slimcoexpression.txt sd-cotranslation.txt sd-PPIs-highconf.txt
use strict;
use warnings;
my %dispersed; my %proximal; my %tandem; my %transposed; my %wgd; my %random;
open IN,"<Zma.dispersed.txt";
my $str=<IN>;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $str1="$arr[0]$arr[1]";
	$dispersed{$str1}=1;
}
close IN;
open IN,"<Zma.proximal.txt";
$str=<IN>;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $str1="$arr[0]$arr[1]";
	$proximal{$str1}=1;
}
close IN;
open IN,"<Zma.tandem.txt";
$str=<IN>;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $str1="$arr[0]$arr[1]";
	$tandem{$str1}=1;
}
close IN;
open IN,"<Zma.transposed.txt";
$str=<IN>;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $str1="$arr[0]$arr[1]";
	$transposed{$str1}=1;
}
close IN;
open IN,"<Zma.wgd.txt";
$str=<IN>;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $str1="$arr[0]$arr[1]";
	$wgd{$str1}=1;
}
close IN;
open IN,"<para_random.txt";
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $str1="$arr[0]$arr[1]";
	$random{$str1}=1;
}
close IN;
print "id1\tid2\tdistance\ttype\tomics\n";
open IN,"<$ARGV[0]";
$str=<IN>;
my @id=split /\t/,$str;
my $n=1;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $i=$n+1;
	while ($id[$i]){
		my $str1="$arr[0]$id[$i]";
		my $str2="$id[$i]$arr[0]";
		if ((exists $dispersed{$str1} || exists $dispersed{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tDispersed\tCo-expression\n";
		}
		if ((exists $proximal{$str1} || exists $proximal{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tProximal\tCo-expression\n";
		}
		if ((exists $tandem{$str1} || exists $tandem{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tTandem\tCo-expression\n";
		}
		if ((exists $transposed{$str1} || exists $transposed{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tTransposed\tCo-expression\n";
		}
		if ((exists $wgd{$str1} || exists $wgd{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tWGD\tCo-expression\n";
		}
		if ((exists $random{$str1} || exists $random{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tRandom\tCo-expression\n";
		}
		$i++;
	}
	$n++;
}
close IN;
open IN,"<$ARGV[1]";
$str=<IN>;
@id=split /\t/,$str;
$n=1;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $i=$n+1;
	while ($id[$i]){
		my $str1="$arr[0]$id[$i]";
		my $str2="$id[$i]$arr[0]";
		if ((exists $dispersed{$str1} || exists $dispersed{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tDispersed\tCo-translation\n";
		}
		if ((exists $proximal{$str1} || exists $proximal{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tProximal\tCo-translation\n";
		}
		if ((exists $tandem{$str1} || exists $tandem{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tTandem\tCo-translation\n";
		}
		if ((exists $transposed{$str1} || exists $transposed{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tTransposed\tCo-translation\n";
		}
		if ((exists $wgd{$str1} || exists $wgd{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tWGD\tCo-translation\n";
		}
		if ((exists $random{$str1} || exists $random{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tRandom\tCo-translation\n";
		}
		$i++;
	}
	$n++;
}
close IN;
open IN,"<$ARGV[2]";
$str=<IN>;
@id=split /\t/,$str;
$n=1;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $i=$n+1;
	while ($id[$i]){
		my $str1="$arr[0]$id[$i]";
		my $str2="$id[$i]$arr[0]";
		if ((exists $dispersed{$str1} || exists $dispersed{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tDispersed\tInteractome\n";
		}
		if ((exists $proximal{$str1} || exists $proximal{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tProximal\tInteractome\n";
		}
		if ((exists $tandem{$str1} || exists $tandem{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tTandem\tInteractome\n";
		}
		if ((exists $transposed{$str1} || exists $transposed{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tTransposed\tInteractome\n";
		}
		if ((exists $wgd{$str1} || exists $wgd{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tWGD\tInteractome\n";
		}
		if ((exists $random{$str1} || exists $random{$str2}) && $arr[$i] ne "Inf"){
			print "$arr[0]\t$id[$i]\t$arr[$i]\tRandom\tInteractome\n";
		}
		$i++;
	}
	$n++;
}
close IN;