use strict;
use warnings;
my $sab; my $dab; my @arr;
open IN,"<id.txt";
while (my $str=<IN>){
	chomp $str;
	my $in="$ARGV[0]-$str.txt";
	open SUBIN,"<$in";
	while (my $substr=<SUBIN>){
		chomp $substr;
		@arr=split /\t/,$substr;
		if ($arr[2] eq "na"){
			$arr[2]=0;
		}
		if ($arr[3] eq "na"){
			$arr[3]=0;
		}
		print "$arr[0]\t$arr[1]\t";
		if (($arr[2]>0 && $arr[3]) > 0 && ($arr[2]+$arr[3]) >= 5){
			$sab=$arr[4]/&min($arr[2],$arr[3]);
			$dab=(abs($arr[2]-$arr[3]))/&max($arr[2],$arr[3]);
			print "$dab\t$sab\t";
			if ($dab >= 0 && $dab < 0.5){
				if ($sab >= 0 && $sab < 0.5){
					print "III\t";
				}elsif ($sab >= 0.5 && $sab <= 1){
					print "I\t";
				}
			}elsif ($dab >= 0.5 && $dab <= 1){
				if ($sab >= 0 && $sab < 0.5){
					print "IV\t";
				}elsif ($sab >= 0.5 && $sab <= 1){
					print "II\t";
				}
			}
		}elsif (($arr[2]==0 && $arr[3] >= 10) || ($arr[2]>=10 && $arr[3] == 0)){
			print "1\t0\tV\t";
		}
		print "$str\n";
	}
	close SUBIN;
}
close IN;
sub min(){
	$a=$_[0];
	$b=$_[1];
	if ($a <= $b){
		return $a;
	}else{
		return $b;
	}
}
sub max(){
	$a=$_[0];
	$b=$_[1];
	if ($a >= $b){
		return $a;
	}else{
		return $b;
	}
}