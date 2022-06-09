##usage: perl module.pl module-slimcoexpression.txt module-cotranslation.txt module-proteome-highconf.txt
use strict;
use warnings;
print "Type\tOmics\tper\n";
my %trans; my %ribo; my %ppi;
open IN,"<$ARGV[0]";
my $n=1;
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $i=0;
	while ($arr[$i]){
		$trans{$arr[$i]}=$n;
		$i++;
	}
	$n++;
}
close IN;
open IN,"<$ARGV[1]";
$n=1;
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $i=0;
	while ($arr[$i]){
		$ribo{$arr[$i]}=$n;
		$i++;
	}
	$n++;
}
close IN;
open IN,"<$ARGV[2]";
$n=1;
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	my $i=0;
	while ($arr[$i]){
		$ppi{$arr[$i]}=$n;
		$i++;
	}
	$n++;
}
close IN;
my $transa=0; my $transb=0; my $riboa=0; my $ribob=0; my $ppia=0; my $ppib=0;
open IN,"<Zma.tandem.txt";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	if (exists $trans{$arr[0]} && exists $trans{$arr[1]}){
		$transa++;
		if ($trans{$arr[0]} eq $trans{$arr[1]}){
			$transb++;
		}
	}
	if (exists $ribo{$arr[0]} && exists $ribo{$arr[1]}){
		$riboa++;
		if ($ribo{$arr[0]} eq $ribo{$arr[1]}){
			$ribob++;
		}
	}
	if (exists $ppi{$arr[0]} && exists $ppi{$arr[1]}){
		$ppia++;
		if ($ppi{$arr[0]} eq $ppi{$arr[1]}){
			$ppib++;
		}
	}
}
close IN;
my $str1=sprintf "%.1f",($transb/$transa*100);
my $str2=sprintf "%.1f",($ribob/$riboa*100);
my $str3=sprintf "%.1f",($ppib/$ppia*100);
print "Tandem\tCo-expression\t$str1\n";
print "Tandem\tTranslatome\t$str2\n";
print "Tandem\tInteractome\t$str3\n";
$transa=0; $transb=0; $riboa=0; $ribob=0; $ppia=0; $ppib=0;
open IN,"<Zma.proximal.txt";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	if (exists $trans{$arr[0]} && exists $trans{$arr[1]}){
		$transa++;
		if ($trans{$arr[0]} eq $trans{$arr[1]}){
			$transb++;
		}
	}
	if (exists $ribo{$arr[0]} && exists $ribo{$arr[1]}){
		$riboa++;
		if ($ribo{$arr[0]} eq $ribo{$arr[1]}){
			$ribob++;
		}
	}
	if (exists $ppi{$arr[0]} && exists $ppi{$arr[1]}){
		$ppia++;
		if ($ppi{$arr[0]} eq $ppi{$arr[1]}){
			$ppib++;
		}
	}
}
close IN;
$str1=sprintf "%.1f",($transb/$transa*100);
$str2=sprintf "%.1f",($ribob/$riboa*100);
$str3=sprintf "%.1f",($ppib/$ppia*100);
print "Proximal\tCo-expression\t$str1\n";
print "Proximal\tTranslatome\t$str2\n";
print "Proximal\tInteractome\t$str3\n";
$transa=0; $transb=0; $riboa=0; $ribob=0; $ppia=0; $ppib=0;
open IN,"<Zma.wgd.txt";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	if (exists $trans{$arr[0]} && exists $trans{$arr[1]}){
		$transa++;
		if ($trans{$arr[0]} eq $trans{$arr[1]}){
			$transb++;
		}
	}
	if (exists $ribo{$arr[0]} && exists $ribo{$arr[1]}){
		$riboa++;
		if ($ribo{$arr[0]} eq $ribo{$arr[1]}){
			$ribob++;
		}
	}
	if (exists $ppi{$arr[0]} && exists $ppi{$arr[1]}){
		$ppia++;
		if ($ppi{$arr[0]} eq $ppi{$arr[1]}){
			$ppib++;
		}
	}
}
close IN;
$str1=sprintf "%.1f",($transb/$transa*100);
$str2=sprintf "%.1f",($ribob/$riboa*100);
$str3=sprintf "%.1f",($ppib/$ppia*100);
print "WGD\tCo-expression\t$str1\n";
print "WGD\tTranslatome\t$str2\n";
print "WGD\tInteractome\t$str3\n";
$transa=0; $transb=0; $riboa=0; $ribob=0; $ppia=0; $ppib=0;
open IN,"<Zma.transposed.txt";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	if (exists $trans{$arr[0]} && exists $trans{$arr[1]}){
		$transa++;
		if ($trans{$arr[0]} eq $trans{$arr[1]}){
			$transb++;
		}
	}
	if (exists $ribo{$arr[0]} && exists $ribo{$arr[1]}){
		$riboa++;
		if ($ribo{$arr[0]} eq $ribo{$arr[1]}){
			$ribob++;
		}
	}
	if (exists $ppi{$arr[0]} && exists $ppi{$arr[1]}){
		$ppia++;
		if ($ppi{$arr[0]} eq $ppi{$arr[1]}){
			$ppib++;
		}
	}
}
close IN;
$str1=sprintf "%.1f",($transb/$transa*100);
$str2=sprintf "%.1f",($ribob/$riboa*100);
$str3=sprintf "%.1f",($ppib/$ppia*100);
print "Transposed\tCo-expression\t$str1\n";
print "Transposed\tTranslatome\t$str2\n";
print "Transposed\tInteractome\t$str3\n";
$transa=0; $transb=0; $riboa=0; $ribob=0; $ppia=0; $ppib=0;
open IN,"<Zma.dispersed.txt";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	if (exists $trans{$arr[0]} && exists $trans{$arr[1]}){
		$transa++;
		if ($trans{$arr[0]} eq $trans{$arr[1]}){
			$transb++;
		}
	}
	if (exists $ribo{$arr[0]} && exists $ribo{$arr[1]}){
		$riboa++;
		if ($ribo{$arr[0]} eq $ribo{$arr[1]}){
			$ribob++;
		}
	}
	if (exists $ppi{$arr[0]} && exists $ppi{$arr[1]}){
		$ppia++;
		if ($ppi{$arr[0]} eq $ppi{$arr[1]}){
			$ppib++;
		}
	}
}
close IN;
$str1=sprintf "%.1f",($transb/$transa*100);
$str2=sprintf "%.1f",($ribob/$riboa*100);
$str3=sprintf "%.1f",($ppib/$ppia*100);
print "Dispersed\tCo-expression\t$str1\n";
print "Dispersed\tTranslatome\t$str2\n";
print "Dispersed\tInteractome\t$str3\n";
$transa=0; $transb=0; $riboa=0; $ribob=0; $ppia=0; $ppib=0;
open IN,"<para_random.txt";
while (my $str=<IN>){
	chomp $str;
	my @arr=split /\t/,$str;
	if (exists $trans{$arr[0]} && exists $trans{$arr[1]}){
		$transa++;
		if ($trans{$arr[0]} eq $trans{$arr[1]}){
			$transb++;
		}
	}
	if (exists $ribo{$arr[0]} && exists $ribo{$arr[1]}){
		$riboa++;
		if ($ribo{$arr[0]} eq $ribo{$arr[1]}){
			$ribob++;
		}
	}
	if (exists $ppi{$arr[0]} && exists $ppi{$arr[1]}){
		$ppia++;
		if ($ppi{$arr[0]} eq $ppi{$arr[1]}){
			$ppib++;
		}
	}
}
close IN;
$str1=sprintf "%.1f",($transb/$transa*100);
$str2=sprintf "%.1f",(($ribob/$riboa)*100);
$str3=sprintf "%.1f",(($ppib/$ppia)*100);
print "Random\tCo-expression\t$str1\n";
print "Random\tCo-translation\t$str2\n";
print "Random\tInteractome\t$str3\n";
