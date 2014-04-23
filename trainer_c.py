


import numpy as np
import pandas as pd
import random
import utils
import base_c

 
columnNames = [] # need to add all columes ...



 
 
#df = pd.read_csv('cadata.txt',skiprows=27, sep='\s+',names=columnNames)

class trainer_c(base_c):
    
    
    def InitcolumnNames(self,trainTableFile):
        columnNames =[]
        
        return columnNames
    
    def __init__(self,trainTableFile):
        if not utils.PathExist(trainTableFile):
            self.LogPrint("missing machine learning table file will exist...")
            return -1
        self.m_tainFile = trainTableFile
        
        self.m_columnNames=self.InitcolumnNames(self.m_tainFile)
        self.m_machinePandasMatrix = pd.read_csv(trainTableFile,skiprows=1, sep=',',names=self.m_columnNames)
        
        
            