
import utils
from base_c import base_c
import users_DB_graph_c
import pickle
import csv

from random import shuffle
from ctypes import util

class data_set_creator_c( base_c ):
    
    def __init__(self,user_db ):
        self.__DATA_SETS_DIR=utils.DEF_RESULT_DIR + "/dataSets" 
        self.__DATA_SETS_FILE_NAME = "dataSet%d.csv"
        self.__DATA_SETS_FILE_NAME_ENC = "dataSet%dEncoded.csv"
        self.__TEST_SETS_FILE_NAME_ENC="testSet%dEncoded.csv"
        self.__TEST_SETS_FILE_NAME = "testSet%d.csv"
        self.__TEST_SETS_FILE_NAME_ENC ="testSet%dEncoded.csv"
        self.__DATA_SET_FILE_NAME_OBJ = "dataSet.pkl"
        self.__DATA_SET_FILE_NAME_OBJ_ENCODED= "encodeDataSet%d"
        self.__TEST_SET_FILE_NAME_OBJ_ENCODED = "testSet%d"
        self.__TEST_SET_FILE_NAME_OBJ = "testSet.pkl"
        self.__STRING_HASH_FILE_NAME = self.__DATA_SETS_DIR+ "/string_hash.pkl"
        self.m_string_hash={}
        self.m_user_db = user_db
        self.__SPREATE_SIZE=5
        
        self.m_usersDataSets={}
        self.m_usersDataSetsEnc={}
        
        self.m_test_sets={}
        self.m_test_setsEnc={}
        
        self.m_translatorData={}
        self._translatorTest={}
        
        self.m_isReady=False
        self.m_isEncoded=False
        #self.__DATA_SETS_FILES_NAME
        for i in range(0,self.__SPREATE_SIZE):
            self.m_usersDataSets[i]={}   
            self.m_test_sets[i]={}
        utils.EnsureDir(self.__DATA_SETS_DIR)
        
        
    def __SplitList(self,alist, wanted_parts=1):
        length = len(alist)
        return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]    
        
        
        
        
    def create_data_set(self):
        ret=True
        self.LogPrint("start creating data set ...")
        if self.m_user_db == None :
            self.LogPrint("self.m_user_db is None!!! aborting..")
            return False
        if not self.m_user_db.IsLoaded():
            utils.LOG("users data base is not loaded will return false")
            return False
        #everything is ok!!!
        users2SubjectDic=self.m_user_db.GetUsers2SubjectDic()
        
        for user , subjects in users2SubjectDic.iteritems():
            subjectLen=len(subjects)
            if not subjectLen < self.__SPREATE_SIZE:
                #self.LogPrint("skip user %s has less them %d subjects" % (user ,self.__SPREATE_SIZE ))
               
                newSubjectGroups = self.__SplitList(subjects, self.__SPREATE_SIZE)
                for i in range(0,self.__SPREATE_SIZE):
                    for j in range(0,self.__SPREATE_SIZE):
                        for subjectindex in newSubjectGroups[j]:
                            if not i==j:
                                if not self.m_usersDataSets[j].has_key(user):
                                    self.m_usersDataSets[j][user]=[]
                                if not subjectindex in  self.m_usersDataSets[j][user]:
                                    self.m_usersDataSets[j][user].append(subjectindex) 
                            else:
                                if not self.m_test_sets[j].has_key(user):
                                    self.m_test_sets[j][user]=[]
                                if not subjectindex in self.m_test_sets[j][user]:
                                    self.m_test_sets[j][user].append(subjectindex)
                
        self.m_isReady=True
        return ret

    def __SetFilePathToResult(self,fileName):
        return "%s/%s" % (self.__DATA_SETS_DIR,fileName )
        
    def __CreateFilePath(self,filename,index=None):
        
        if  index != None:
            pathFileName = filename % index
           
        else:
            pathFileName = filename
        return self.__SetFilePathToResult(pathFileName)
        
    def __EncodedString(self,str):
        return utils.EncodeString(str)
        
    def __EncodedSet(self,set,dump2fileName):
        encodedSet ={}
        
        for i in range(0,self.__SPREATE_SIZE):
            setDic=set[i].copy().items()
           
            encodedSet[i]={}
            
            for user,subjects in setDic:
                if user != None:
                    encUser = self.__EncodedString(user)
                    if not self.m_string_hash.has_key(encUser):
                        self.m_string_hash[encUser]=user
                    encodedSet[i][encUser]=[]
                                            
                    for subject in subjects:
                        encSubject= self.__EncodedString(subject)
                        if not  self.m_string_hash.has_key(encSubject):
                            self.m_string_hash[encSubject]=subject
                        encodedSet[i][encUser].append(encSubject)
            encodedDataFile =self.__CreateFilePath(dump2fileName, i) 
            encodedDataFile +=".pkl"
            self.LogPrint("saving encoded object data set to file %s" % encodedDataFile)
            utils.DumpObjToFile(encodedSet[i], encodedDataFile)    
        return encodedSet
        
        
    #need to finish
    def EncodedDataSet(self):
        if not self.m_isReady:
            self.LogPrint("can't dump dataSet files... data sets are not ready")
            return
       
        self.m_usersDataSetsEnc = self.__EncodedSet(self.m_usersDataSets,  self.__DATA_SET_FILE_NAME_OBJ_ENCODED)
        self.m_test_setsEnc = self.__EncodedSet(self.m_test_sets,  self.__TEST_SET_FILE_NAME_OBJ_ENCODED)
        '''for i in range(0,self.__SPREATE_SIZE):
            dataSetDic=self.m_usersDataSets[i].copy().items()
            testSetDic=self.m_test_sets[i].copy().item()
            self.m_usersDataSetsEnc[i]={}
            
            for user,subjects in dataSetDic:
                if user != None:
                    encUser = self.__EncodedString(user)
                    if not self.m_string_hash.has_key(encUser):
                        self.m_string_hash[encUser]=user
                    self.m_usersDataSetsEnc[i][encUser]=[]
                                            
                    for subject in subjects:
                        encSubject= self.__EncodedString(subject)
                        if not  self.m_string_hash.has_key(encSubject):
                            self.m_string_hash[encSubject]=subject
                        self.m_usersDataSetsEnc[i][encUser].append(encSubject)
            encodedDataFile =self.__CreateFilePath(self.__DATA_SET_FILE_NAME_OBJ_ENCODED, i) 
            encodedDataFile +=".pkl"
            self.LogPrint("saving encoded object data set to file %s" % encodedDataFile)
            utils.DumpObjToFile(self.m_usersDataSetsEnc[i], encodedDataFile)
         '''
            #self.m_test_setsEnc[i]={}
                    
        self.LogPrint("saving all hash-string to file ")
        
        utils.DumpObjToFile(self.m_string_hash,self.__STRING_HASH_FILE_NAME)
        #print "hash look like:",self.m_string_hash
        
        '''
            encodedDataSetDic ={}
            userCont =0
            for user,subjects in dataSetDic: #need to create shuffle system here...
                
                #print userData
                shuffle(subjects)
                
                encodedDataSetDic[userCont]={}
                enodedSubjectDic={}
                #print "user=", user,"subjects =", subjects
                for interestIndex in len(subjects):
                    enodedSubjectDic[subjects[interestIndex]]=interestIndex
                encodedDataSetDic[user]=enodedSubjectDic
            self.m_usersDataSetsEnc[i]=encodedDataSetDic
            encodedDataFile =self.__CreateFilePath(self.__DATA_SET_FILE_NAME_OBJ_ENCODED, i)
            utils.DumpObjToFile(self.m_usersDataSetsEnc, encodedDataFile)
                           
            self.LogPrint("finish encoded data!! dumping data to %s file "% self.m_usersDataSetsEnc)
        '''
        self.m_isEncoded =True
        
    def __verfiyDicStr(self,dic,keyStr):
        #print "size=", len(self.m_string_hash)
        intKey= int(keyStr)
        #print "key=", intKey
        
        if not self.m_string_hash.has_key(intKey):
            self.LogPrint("Error: someone missing the key %s " % keyStr)
            return False
            str = self.m_string_hash[keyStr]
            if keyStr != self.__EncodedString(str):
                self.LogPrint("Error :hash is not the same like giving hash!!!")                     
                return False
        return True
        
    def VerifyHash(self,testedfilePath):
        ifile = open(testedfilePath,"rb")
        reader = csv.reader(ifile)
        rowCnt =0
        for row in reader:
            if rowCnt==0:
                rowCnt+=1
                continue
            columnCnt = 0
            usrStr=""
            for col in row:
                if columnCnt==0:
                    userHash =int(col)
                    # add this section to function !!!
                    if not self.__verfiyDicStr(self.m_string_hash,userHash):
                        return False
                    
                    usrStr = self.m_string_hash[userHash]
                    user2Subjects = self.m_user_db.GetUsers2SubjectDic()
                    if not user2Subjects.has_key(usrStr):
                        self.LogPrint("Error :user %s didn't found at the userDB..."% usrStr)
                        return False
                else:
                    subjectHash=int(col)
                    if not self.__verfiyDicStr(self.m_string_hash, subjectHash):
                        return False
                    subjectStr = self.m_string_hash[subjectHash] 
                    if not subjectStr in user2Subjects[usrStr]:
                        self.LogPrint("Error :missing subject %s from user %s at the db... "%(subjectStr,usrStr))
                        return False
                                    
                columnCnt+=1
                
        return True            
            
        


    def DumpDataSets(self):
        if not self.m_isReady:
            self.LogPrint("can't dump dataSet files... data sets are not ready")
            return
        self.LogPrint("dumping users data and train set set objects file... ")
        dataObjFilePath = self.__SetFilePathToResult(self.__DATA_SET_FILE_NAME_OBJ)
        utils.DumpObjToFile(self.m_usersDataSets, dataObjFilePath)
        testObjFilePath = self.__SetFilePathToResult(self.__TEST_SET_FILE_NAME_OBJ)
        utils.DumpObjToFile(self.m_test_sets, testObjFilePath)
        self.LogPrint("success to dump data set files!!! path :dataset - %s testset -%s" % (dataObjFilePath,testObjFilePath))
        
        
        for i in range(0,self.__SPREATE_SIZE):

            dataTestName = self.__DATA_SETS_FILE_NAME  % i
            
            testName = self.__TEST_SETS_FILE_NAME % i
            data_file_path = "%s/%s" % (self.__DATA_SETS_DIR,dataTestName)
            data_file_path_enc= "%s/%s" % (self.__DATA_SETS_DIR,self.__DATA_SETS_FILE_NAME_ENC %i)
            
            test_file_path = "%s/%s" % (self.__DATA_SETS_DIR,testName)
            test_file_path_enc ="%s/%s" % (self.__DATA_SETS_DIR,self.__TEST_SETS_FILE_NAME_ENC % i)
            if self.m_isEncoded:
                self.LogPrint("dumping encoded data data Set path =%s ,test Set path =%s" % (data_file_path_enc,test_file_path_enc))
                utils.SaveStatistics2File_DicVal(data_file_path_enc,['user','subject'],self.m_usersDataSetsEnc[i])
                utils.SaveStatistics2File_DicVal(test_file_path_enc,['user','subject'],self.m_test_setsEnc[i])
                self.LogPrint("success to dump encoded data set to %s  ,verifying data..." %data_file_path)
                if not self.VerifyHash(data_file_path_enc):
                    self.LogPrint("verifcation failed!!!")
                    return
                self.LogPrint("success!!")
            
            
            self.LogPrint("dumping data set and test set's files...")
            utils.SaveStatistics2File_DicVal(data_file_path, ['user','subject'],self.m_usersDataSets[i])
            utils.SaveStatistics2File_DicVal(test_file_path,['user','subject'],self.m_test_sets[i])
            
           
   
            