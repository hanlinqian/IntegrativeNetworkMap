```perl
#This is srnauniq.pl;
use strict;
use warnings;
my %hb;
open IN,"<$ARGV[0]";
while (my $str1=<IN>){
	chomp $str1;
	my $str2=<IN>;
	chomp $str2;
	if (!exists $hb{$str2}){
		$hb{$str2}=1
	}else{
		$hb{$str2}++;
	}
}
close IN;
my $i=1;
while (my ($key,$value) =each %hb){
	print ">$ARGV[1]-s$i-$value\n";
	print "$key\n";
	$i++;
}
```
