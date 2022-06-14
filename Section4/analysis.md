##### 1. Code for Fig. 4f and Extended Data Fig. 18
###### step1: construct a direct-connected network
`perl net-direct.pl 62kernel.txt out.csv`  
##net-direct.pl was in Section4/code; 62kernel.txt containing 62 kernel genes was in Section4/data; and edge-slimio-lowconf.txt in this code was in OMIX(https://ngdc.cncb.ac.cn/omix/) with accession number OMIX001131.
###### step2:calculate the significant
`perl net-pavlue.pl 62 1000 62kernel.txt`   
##net-pavlue.pl was in Section4/code. 62 is the number of kernel genes and 1000 is the number of random iterations.

##### 2. Code for Extended Data Fig. 17a
`for ((i=1;i<=1000;i++));do perl 45+17test.pl 62kernel.txt ;done`
