##### 1. Computation of node similarity in a network
`perl similarity.pl edge-proteome-highconf.txt nodeinfo-proteome-highconf.txt traingene-34pos+34neg.txt 5 8 >out.txt`  
##similarity.pl was in code folder, edge-proteome-highconf.txt was in OMIX(https://ngdc.cncb.ac.cn/omix/) which accession number was OMIX001131, nodeinfo-proteome-highconf.txt was in chapter1/data folder and traingene-34pos+34neg.txt was in data folder. 5 and 8 means genes in rows 5-8 of nodeinfo-proteome-highconf.txt. 
This code was used to calculate similarity with 68 train genes in the network, including: 
1) Common Neighbours Similarity (CN);  
2) Resource Allocation Similarity (RA);  
3) Total Neighbours Similarity (TN);  
4) Preferential Attachment (PA);  
5) Hub Promoted Similarity (HP);  
6) Hub Depressed Similarity (HD);  
7) Sorensen-Dice Similarity (sorensen).

##### 2. Five classical Machine Learning Model Evaluation of Interactome  
Refer to code Trainning_results_for_sd_feature.py in code folder.

##### 3. Five classical Machine Learning Model Evaluation of Intergrative omics which containg expression, nodeinformation and shortest distance attributes
Refer to code Training_results_for_different_features.py in code folder.

##### 4. Prediction by Machine Learning and feature evaluation
Refer to code predresult.py in code folder.
