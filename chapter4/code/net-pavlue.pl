##usage: perl net-pavlue.pl genenumber iterationnumber geneid.txt
##usage: perl net-pavlue.pl 62 1000 62kernel.txt
use strict;
use warnings;
my $knwongenenum=$ARGV[0];
my $iteratenum=$ARGV[1];
my $inputfile=$ARGV[2];
open IN,"<edge-slimio-lowconf.txt";
my %edge; my $num=0; my %node; my @allgene; my @weight;
my $str=<IN>;
while ($str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $str1="$arr[0]$arr[1]";
	$edge{$str1}=$arr[6];
	if (!exists $node{$arr[0]}){
		$node{$arr[0]}=1;
		$allgene[$num]=$arr[0];
		$num++;
	}
	if (!exists $node{$arr[1]}){
		$node{$arr[1]}=1;
		$allgene[$num]=$arr[1];
		$num++;
	}
}
close IN;
my $n=0;
for (my $i=0;$i<$iteratenum;$i++){
	my @testarr=();
	for ($n=0;$n<$knwongenenum;$n++){
		$testarr[$n]=int(rand($num));
	}
	$weight[$i]=&weightsum(@testarr);
}
open IN,"<$inputfile";
my @truearr; $n=0;
while ($str=<IN>){
	chomp $str;
	$truearr[$n]=$str;
	$n++;
}
close IN;
my $trueweight=&weightsum(@truearr);
$n=0;
foreach my $item(@weight){
	if ($item > $trueweight){
		$n++;
	}
}
my $rate=sprintf "%.6f",($n/$iteratenum);
print "Pvalue: $rate\n";
sub weightsum(){
	my @id=@_;
	my $sum=0;
	for (my $x=0;$x<$knwongenenum;$x++){
		for (my $y=$x+1;$y<$knwongenenum;$y++){
			my $str1="$id[$x]$id[$y]";
			my $str2="$id[$y]$id[$x]";
			if (exists $edge{$str1}){
				$sum=$sum+$edge{$str1};
			}elsif (exists $edge{$str2}){
				$sum=$sum+$edge{$str2};
			}
		}
	}
	return $sum;
}
