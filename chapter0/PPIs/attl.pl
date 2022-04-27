use strict;
use warnings;
my %hb;my %attls; my %attle; my %bd; my %ad; my %info;
open IN,"<$ARGV[0]";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	if (!exists $hb{$arr[0]}){
		$hb{$arr[0]}=1;
		$info{$arr[0]}{len}=$arr[3];
		$info{$arr[0]}{mis}=$arr[4];
		$info{$arr[0]}{gap}=$arr[5];
		if ($arr[8] < $arr[9]){
			$attls{$arr[0]}=$arr[6];
			$attle{$arr[0]}=$arr[7];
			$bd{$arr[0]}=1;
		}elsif ($arr[8] > $arr[9]){
			$attls{$arr[0]}=$arr[6];
			$attle{$arr[0]}=$arr[7];
			$ad{$arr[0]}=1;
		}
	}else{
		$hb{$arr[0]}++;
	}
}
close IN;
open IN,"<$ARGV[1]";
open OUT1,">$ARGV[2]";
open OUT2,">$ARGV[3]";
while (my $str=<IN>){
	my @name=split / /,$str;
	my @name1=split />/,$name[0];
	if (exists $hb{$name1[1]} && $hb{$name1[1]} eq "1" && $info{$name1[1]}{len} >= 54 && $info{$name1[1]}{len} <= 56 && $info{$name1[1]}{mis} <=1 && $info{$name1[1]}{gap} <=1){
		my $seq=<IN>;
		chomp $seq;
		my $len=length($seq);
		my $a=substr($seq,0,$attls{$name1[1]}-1);
		my $b=substr($seq,$attle{$name1[1]},$len-$attle{$name1[1]});
		if (length($a)>=1 && length($b) >=1){
			print OUT1 "$str";
			print OUT2 "$str";
			my $b_rc=&rev_and_com($b);
			if (exists $bd{$name1[1]}){
				print OUT1 "$a\n";
				print OUT2 "$b_rc\n";
			}elsif (exists $ad{$name1[1]}){
				print OUT2 "$a\n";
				print OUT1 "$b_rc\n";
			}
		}
	}else{
		$str=<IN>;
	}
}
close IN;
close OUT1;
close OUT2;
sub rev_and_com {
	my $s ="";
	my $a ="";
	$s = shift;
	$a = $s;
	$a =~ tr/atcgATCG/tagcTAGC/;
	return reverse($a);
}