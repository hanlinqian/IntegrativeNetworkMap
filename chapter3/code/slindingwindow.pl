#usage:perl slindingwindow.pl 10 100
#usage:perl slindingwindow.pl windowsize stepsize
use strict;
my $str;
my %hb;
my $n; my $x; my $i; my $a;
`wc -l 1.txt > a.txt`;
open IN,"<a.txt";
$a=<IN>;
chomp $a;
close IN;
`rm a.txt`;
print "id\tper\ttype\tomics\n";
for ($n=1;$n<=$a;$n=$n+$ARGV[0]){
	$hb{1}=0; $hb{0}=0; $hb{-1}=0;
	open IN,"<1.txt";
	for ($x=1;$x<$n;$x++){
		$str=<IN>;
	}
	for ($i=1;$i<=$ARGV[1];$i++){
		$str=<IN>;
		chomp $str;
		my @arr=split /\t/,$str;
		$hb{$arr[0]}++;
	}
	my $str1=sprintf "%.2f",($hb{1}/($hb{1}+$hb{0}+$hb{-1}));
	my $str2=sprintf "%.2f",($hb{-1}/($hb{1}+$hb{0}+$hb{-1}));
	print "$n\t$str1\tMaize1\tCo-expression\n";
	print "$n\t$str2\tMaize2\tCo-expression\n";
	close IN;
}
for ($n=1;$n<=$a;$n=$n+$ARGV[0]){
	$hb{1}=0; $hb{0}=0; $hb{-1}=0;
	open IN,"<1.txt";
	for ($x=1;$x<$n;$x++){
		$str=<IN>;
	}
	for ($i=1;$i<=$ARGV[1];$i++){
		$str=<IN>;
		chomp $str;
		my @arr=split /\t/,$str;
		$hb{$arr[1]}++;
	}
	my $str1=sprintf "%.2f",($hb{1}/($hb{1}+$hb{0}+$hb{-1}));
	my $str2=sprintf "%.2f",($hb{-1}/($hb{1}+$hb{0}+$hb{-1}));
	print "$n\t$str1\tMaize1\tCo-translation\n";
	print "$n\t$str2\tMaize2\tCo-translation\n";
	close IN;
}
for ($n=1;$n<=$a;$n=$n+$ARGV[0]){
	$hb{1}=0; $hb{0}=0; $hb{-1}=0;
	open IN,"<1.txt";
	for ($x=1;$x<$n;$x++){
		$str=<IN>;
	}
	for ($i=1;$i<=$ARGV[1];$i++){
		$str=<IN>;
		chomp $str;
		my @arr=split /\t/,$str;
		$hb{$arr[2]}++;
	}
	my $str1=sprintf "%.2f",($hb{1}/($hb{1}+$hb{0}+$hb{-1}));
	my $str2=sprintf "%.2f",($hb{-1}/($hb{1}+$hb{0}+$hb{-1}));
	print "$n\t$str1\tMaize1\tInteractome\n";
	print "$n\t$str2\tMaize2\tInteractome\n";
	close IN;
}
`rm 1.txt`
