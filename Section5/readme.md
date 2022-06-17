This section is about predicting genes of flowering time by machine learning.

#### 1. Computation of node similarity in a network
`perl similarity.pl edge-proteome-highconf.txt nodeinfo-proteome-highconf.txt traingene-34pos+34neg.txt 5 8 >out.txt`  
##similarity.pl was in Section5/code;  
##edge-proteome-highconf.txt was in Section0/data;  
##nodeinfo-proteome-highconf.txt was in Section1/data;  
##traingene-34pos+34neg.txt was in Section5/data;  
##5 and 8 means genes in 5-8 rows of nodeinfo-proteome-highconf.txt.   
   
This code was used to calculate similarity with 68 train genes in the network, including:  
(1) Common Neighbours Similarity (CN);  
(2) Resource Allocation Similarity (RA);  
(3) Total Neighbours Similarity (TN);  
(4) Preferential Attachment (PA);  
(5) Hub Promoted Similarity (HP);  
(6) Hub Depressed Similarity (HD);  
(7) Sorensen-Dice Similarity (sorensen). 

#### 2. Model evaluation (AUC and F1 values) of five classical machine learning algorithms (LogisticRegression, BaggingClassifier, XGBClassifier, SVM and Neural Network) for Interactome. 
Trainning_results_for_sd_feature.py was in Section5/code.

#### 3. Model evaluation (AUC and F1 values) of five classical machine learning algorithms (LogisticRegression, BaggingClassifier, XGBClassifier, SVM and Neural Network) for Intergrative omics which containg expression of transcriptome and translatome, nodeinformation and shortest distance attributes of Interactome.
Training_results_for_different_features.py was in Section5/code.

#### 4. Result prediction and feature importance calculation
predresult.py was in Section5/code.

#### 5. Code for ROC-AUC figure and PR-curve
Draw_picture.py was in Section5/code.

#### 6. Input data
The input files train.xlsx and test.xlsx involved in the machine learning calculation were uploaded into Section5/data.
