import numpy as np
import pandas as pd
import random
import utils
from base_c import base_c
import csv
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.ensemble import GradientBoostingRegressor
from atk import Util

PRDICT_COL='fake(0) or real(1)'
class trainer_c(base_c):
    
    def InitcolumnNames(self,trainTableFile,x_trianerFile="x_train.pkl",y_trainerFile="y_train.pkl"):
        columnNames =[]
        ifile  = open(trainTableFile, "rb")
        reader = csv.reader(ifile)
        rowNum = 0
        for row in reader:
            if rowNum > 0 :
                break
            for col in row :
                columnNames.append(col)
            rowNum=+1
        
        self.LogPrint("success import table headers num of column =%d" % len(columnNames))
        return columnNames
    
    def __init__(self,trainTableFile):
        if not utils.PathExist(trainTableFile):
            self.LogPrint("missing machine learning table file will exist...")
            return -1
        self.m_tainFile = trainTableFile
        
        self.m_columnNames=self.InitcolumnNames(self.m_tainFile)
        self.m_machinePandasMatrix = pd.read_csv(trainTableFile,dtype={'user': np.int,'subject':np.int},skiprows=2, sep=',',names=self.m_columnNames,encoding='utf8',infer_datetime_format=False)   #,na_filter=False)
        self.m_clf = None
        self.m_X = self.m_machinePandasMatrix[self.m_machinePandasMatrix.columns-[PRDICT_COL]]
        self.m_params =  {'n_estimators': 500, 'max_depth': 6,'learning_rate': 0.1, 'loss': 'huber','alpha':0.95}
        self.m_trainFilePath = trainTableFile
        self.m_testSetFilePath = None
        
        
        
    def BuildClassifer(self,predictCol=PRDICT_COL):
        
        self.m_Y = self.m_machinePandasMatrix[predictCol]
        self.LogPrint ("building classifer...")         
        self.m_clf = GradientBoostingRegressor(**self.m_params).fit(self.m_X, self.m_Y)           
        if not self.m_clf == None:
            self.LogPrint("success to learn and create classifier")
            self.LogPrint("saving x_trains...")
            classiferFilePath = "classifer_obj.pkl"
            utils.DumpObjToFile(self.m_clf ,classiferFilePath)
            if not utils.PathExist(classiferFilePath):
                print "failed to save classifer..."
            else:
                print "classifer saved successfully " 
                                                                                                
    def RunPredict(self,testSetFile):
        if not utils.PathExist(testSetFile):
            self.LogPrint("missing machine learning table file for testset...")
            return None
        self.m_testSetFilePath = testSetFile
        testSetCln = self.InitcolumnNames(testSetFile)
        testPdCsv = pd.read_csv(testSetFile,dtype={'user': np.int,'subject':np.int},skiprows=2, sep=',',names=self.m_columnNames,encoding='utf8',infer_datetime_format=False)#,na_filter=False)
        testSetVal =  testPdCsv.drop([PRDICT_COL],axis=1)# testPdCsv[testPdCsv.columns - [PRDICT_COL]]
        
        #print testSetVal
        predictRes = self.__Predict(testSetVal)
        self.__build_prediction_files(testPdCsv,predictRes)
        
        #print predictRes
    
        
    
        self.LogPrint("predication size = %d ,wile the size of testSet is %d " % ( len( predictRes),len(testSetVal)))
        
        mse= mean_squared_error(testPdCsv[PRDICT_COL],predictRes) #need to fix 
        r2 =r2_score(testPdCsv[PRDICT_COL],predictRes)
        
        print "predict results "
        print "mse=",mse
        print  "r2=",r2  
        
        return predictRes
              
       
    def __build_prediction_files(self,testMatrix,resultColum):
        
        
        #self.LogPrint("building prediction file acording to %s and %s" % ( self.m_trainFilePath,self.m_testSetFilePath) )
        
        #print resultColum
        numberRow = len(resultColum)
        #print "numberRow =%s len of all matrix =%s " % (numberRow, len(testMatrix))
        hFile = open(self.m_testSetFilePath+"_predict.csv","wb")
        writer= csv.writer(hFile,delimiter=",",quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['user','subject','real','prediction'])
        
        self.LogPrint("writing prediction table..")
        for i in range(0,numberRow):
            user  = testMatrix.ix[i][0]
            subject = testMatrix.ix[i][1]
            real = testMatrix.ix[i][4]
            predicit = resultColum[i]
            
            #print "user=%s , subject = %s ,fake=%s" %(user,subject,fake_q)
            writer.writerow([user,subject,real,predicit])
        hFile.close()
        self.LogPrint("done!")
        
        
           
        
        #for x in self.m_machinePandasMatrix.ix[0]:
        #    print "value...  " ,x  
        
        
        
             
        
                
       
    def __Predict(self, testSet):
        if self.m_clf == None :
            self.LogPrint("trainer was not init...will exit");
            return -1
        
        ret =  self.m_clf.predict(testSet); 
        return ret
          
     
        
    def Analysis(self):   
        self.LogPrint("running analysis...")
        

    def LoadClassifer(self,clsObjFilePath):
        if not utils.PathExist(clsObjFilePath):
            self.LogPrint("no trainer classiifer found will exit")
            return -1
        cls =  utils.LoadObjFromFile(clsObjFilePath);
        if  not cls==None:
            self.m_clf = cls
            self.LogPrint("trainer load classifer!!!")



