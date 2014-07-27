#!/bin/bash

echo running full analysis. 
dataPath=results/dataSets #TestTrainSet
graphSuffix=csv.graphml # csvpinterest_clean.graphml  
wight=3
app=main.py

for i in {0..1};
do
	echo create machine learing table 
	#python $app -u $dataPath/dataSet$i.csv -g $dataPath/dataSet$i.$graphSuffix -c -w $wight -t machine_train_tbl$i.csv -f 
	#python $app -u $dataPath/testSet$i.csv -g $dataPath/testSet$i.$graphSuffix -c -w $wight -t machine_test_tbl$i.csv 
	python $app -a $dataPath/machine_train_tbl$i.csv -p $dataPath/machine_test_tbl$i.csv
	
	#python parse_to_graph.py -d $dataPath/dataSet$i.csv 
	#python parse_to_graph.py -d $dataPath/testSet$i.csv
	
	

done 



