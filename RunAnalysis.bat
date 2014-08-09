@echo off

echo running full analysis.
echo parms : %*

if "%1"=="" (
	set dataPath=results\dataSets
else (
	set dataPath=%1
)
)

echo running according to path : %dataPath%
set graphSuffix=csvpinterest_clean.graphml

set wight=5
set app=main.py

for /L %%i IN (0,1,4) DO (
	echo create machine learing table
	python %app% -u %dataPath%/dataSet%i%.csv -s -g %dataPath%/dataSet%i%.%graphSuffix% -c -w %wight% -m %dataPath%/machine_train_tbl%i%.csv -f -mt %dataPath%/machine_test_tbl%i%.csv -ut %dataPath%/testSet%i%.csv > %dataPath%/stat_analysis_%i%.log
	
	python %app% -a %dataPath%/machine_train_tbl%i%.csv -p %dataPath%/machine_test_tbl%i%.csv > %dataPath%/result_analysis_%i%.log
	
)