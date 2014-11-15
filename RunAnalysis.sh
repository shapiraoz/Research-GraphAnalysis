#!/bin/bash



#usage: main.py [-h] [-g GRAPHPATH] [-s] [-c] [-w WEIGHT] [-d] [-u USERDB]
            #               [-m MACHINETABLE] [-ut TESTSET_USERDB]
            #               [-mt TESTSET_MACHINETABLE] [-e] [-a ANALYSIS] [-f] [-p PREDICT]

#graph analysis

#optional arguments:
#  -h, --help            show this help message and exit
#  -g GRAPHPATH, --graphPath GRAPHPATH
                        #                        graph file in graphml format
#  -s, --statistics      run statistics analysis
#  -c, --cluster         run clustring analysis
#  -w WEIGHT, --weight WEIGHT
                        #                        set minimum weight for cleaning the graph
#  -d, --dataset         create data set train set from all data
#  -u USERDB, --userDB USERDB
                        #                        load users file data (csv format
#  -m MACHINETABLE, --machineTable MACHINETABLE
                        #                        create machine learning table input filePath
#  -ut TESTSET_USERDB, --testSet_userDb TESTSET_USERDB
                        #                        test userdb for creating test set
#  -mt TESTSET_MACHINETABLE, --testSet_MachineTable TESTSET_MACHINETABLE
                    	#                   	creating testSet machine learning table (by given
                        #                        testData Set) will be only only after machine learning
                        #                        creation
#  -e, --encoded         graph is encoded
#  -a ANALYSIS, --analysis ANALYSIS
                        #                        train set machine learning talbe
#  -f, --addFake         add fake to the machine learning table
#  -p PREDICT, --predict PREDICT



echo running full analysis. 
echo params: $1

if [ -z $1 ]; then
	
	dataPath=results/dataSets 
else
	dataPath=$1
fi

echo running according to path : $dataPath

graphSuffix=csvpinterest_clean.graphml # csvpinterest_clean.graphml  
wight=5
app=main.py




for i in {1..1};
do
	#echo create machine learing table 
	#python $app -u $dataPath/dataSet$i.csv -s -g $dataPath/dataSet$i.$graphSuffix -c -w $wight -m $dataPath/machine_train_tbl$i.csv -f -mt $dataPath/machine_test_tbl$i.csv -ut $dataPath/testSet$i.csv > $dataPath/stat_analysis_$i.log 
	# cp -r -f results $dataPath/results$i 
	#python $app -u $dataPath/testSet$i.csv -g $dataPath/testSet$i.$graphSuffix -c -w $wight -t machine_test_tbl$i.csv 
	echo train classifiers...
        python $app -a $dataPath/machine_train_tbl$i.csv -p $dataPath/machine_test_tbl$i.csv  #> $dataPath/result_analysis_$i.log 
	cp -f classifer_obj.pkl $dataPath/classifer_obj$i.pkl
	#python parse_to_graph.py -d $dataPath/dataSet$i.csv 
	#python parse_to_graph.py -d $dataPath/testSet$i.csv

done 



