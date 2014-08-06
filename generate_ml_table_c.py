
import utils

import users_DB_graph_c
import cluster_analysis_c
from base_c import base_c
from random import randint

import csv
import os




class generate_ml_table_c(base_c):
    
    def __init__(self , graph , cluster_analysis = None , isGraphEncoded = False , stringsHash = None , usersDB = None , dataFilePath = None):
        
        self.LogPrint("Init all machine learning table creator components ....")
        self.m_graph = graph
        if usersDB==None and dataFilePath != None:
            self.LogPrint("no user DB ,will create user DB ")
            self.m_userDB = users_DB_graph_c.user_DB_graph_c(dataFilePath,graph)
            #need to create the users DB.... without taking all values 
        else:
            self.m_userDB = usersDB
        self.m_userList = self.m_userDB.GetUsersGraph()
        self.m_user2subject = self.m_userDB.GetCopyUser2SubjectsDic().copy()
        self.m_user2subjectItem = self.m_user2subject.items()
       
        self.m_fakeUsers2Subject = {}
        
        if isGraphEncoded and stringsHash==None :
            self.LogPrint("Error can't work without object for encoded numbers... ")
            return
        self.m_isGraphEncoded = isGraphEncoded
        if isGraphEncoded and stringsHash != None:
            self.m_stringHash = stringsHash
            print "working in codede mode"
        
        if len(self.m_userList)==0:
            self.LogPrint("no user list from UserDB...can't proceed...")
            #return 
        
       
        if cluster_analysis==None:
            self.m_cluser_analysis = cluster_analysis_c.cluster_analysis_c(graph,None,self.m_userDB,1)
        else:
            self.m_cluser_analysis = cluster_analysis
            
        self.m_clusterGroups = self.m_cluser_analysis.GetClusterGroups().items()
        
        self.__TABLE_FILE_PATH = utils.DEF_RESULT_DIR + "/machine_learning_tbl.csv"
        #print "init path =%s" % self.__TABLE_FILE_PATH
        self.m_clusters_items = self.m_cluser_analysis.GetClusterGroups().items()
        self.m_table={0:"user",
                      1:"subject",
                      2:"number of subject per user",
                      3:"number of users per subject (real user subjects) ",
                      4:"fake(0) or real(1)"
                      }
        
        
        self.m_numGroups = len(self.m_clusters_items)
        
        for i in range(0,self.m_numGroups):
            self.m_table[i+len(self.m_table)]="subject in cluster %d" % self.m_clusters_items[i][0] 
        for i in range(0,self.m_numGroups):
            self.m_table[i+len(self.m_table)+self.m_numGroups] = "user in cluster %d " % self.m_clusters_items[i][0] 
        self.m_groupSubjectList={}
                
        self.__init_GroupBlongToUsers() 
        self.LogPrint("done Init!!!")
           
            
    
    
    def AddFalseSubjectUsers(self,enforceCoefficient=1):
        self.LogPrint("adding fake subjects... ")
        num_users = self.m_userDB.GetNumOfDBUsers()
        
        usersKeys= self.m_user2subject.keys()
        for user,subjects in self.m_userDB.GetUsers2SubjectDic().iteritems():
            lenSubject = len(subjects)
            addSunbject =int (lenSubject* enforceCoefficient)
            #print "addSunbject = %d real subject =%d"% (addSunbject,len(subjects)) 
            userIndex = randint(0,num_users-1)
            selectedUserSubjectsKey = usersKeys[userIndex]
            selectedUserSubjects = self.m_user2subject[selectedUserSubjectsKey]
            ranUsrSubj=  len(selectedUserSubjects)
            if ranUsrSubj > 1 and addSunbject > 1: 
                for i in range(addSunbject):
                    subjectIndex= randint(0,ranUsrSubj-1)
                    selectSubject =selectedUserSubjects[subjectIndex]
                    #print "selectSubject = %s" % selectSubject 
                    if not selectSubject in subjects:
                        self.m_user2subject[user].append( selectSubject )
                        if not self.m_fakeUsers2Subject.has_key(user):
                            self.m_fakeUsers2Subject[user]=[]
                        self.m_fakeUsers2Subject[user].append(selectSubject )
                            
                        #print "ok %s"% selectSubject
                    else:
                        i-=1
                        #print "need to do something ...i=%d" % i                   
             
        self.LogPrint("finish adding fake subject rate =%0.2f"%enforceCoefficient)        
            #print "users =%s have %d subject " % (user,lenSubject)
    
            
    def __getEncodedValue(self,strVal):
        #print "strVal=%s"% strVal
        varHash=int(strVal)
        if not self.m_stringHash.has_key(varHash):
            self.LogPrint("failed to find value string  %d in the encoded dictionary" % varHash)
            return None
        return self.m_stringHash[varHash]
    
    
    
    def __getSubjectCluster(self,subject):
        if len(self.m_groupSubjectList)==0:
            self.LogPrint("ERROR self.m_groupSubjectList is empty")
            return None
        for groupName , subjects in self.m_groupSubjectList.items():
            if subject in subjects:
                return groupName
        
        return -1
            
    
    def __init_GroupBlongToUsers(self):
        if self.m_userDB == None or self.m_cluser_analysis == None :
            self.LogPrint("missing userDb or clustering ... will return ...")
            return
        self.m_userInGroup={}
        
        for group in self.m_clusterGroups:
            
            groupsubjectList_clean = utils.translateNodeList2SubList(group[1])
            if self.m_isGraphEncoded:
                groupsubjectList = self.__getEncodeGroupSubjectList(groupsubjectList_clean)
            else:
                groupsubjectList = groupsubjectList_clean 
				#group[0]=name
            self.m_groupSubjectList[group[0]]= groupsubjectList 
            for user,subjects in self.m_user2subjectItem : 
                foundInGroup=False
                for subject in subjects:
                    if subject in groupsubjectList: 
                        #print "subject =%s " %subject 
                        if not self.m_userInGroup.has_key(user):
                            self.m_userInGroup[user]=[]
                        self.m_userInGroup[user].append(group[0])
                        foundInGroup = True    
                if foundInGroup :
                    continue
                        
      
    def __getEncodeGroupSubjectList(self,groupSubjectList):
        groupSubjects =[]
        for subjectinGroup in groupSubjectList:
            #print  "going to print %s" % subjectinGroup 
            #print "and now it's %s"% self.__getEncodedValue(subjectinGroup)
            #break ## for debug need to remove !!! - check if it's number or str 
            groupSubjects.append(self.__getEncodedValue(subjectinGroup))
        return groupSubjects
    
    def __StartFile(self,fileHandle=None):
        
        if fileHandle==None:
            return None
        
        #if os.path.exists(filePath):
        #    os.remove(filePath)
        
        
            
        #self.m_csvFile = open(filePath,"wb")
        writer = csv.writer(fileHandle,delimiter=",",quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        #print "opening file %s"% filePath
        #self.m_writer.writerow(self.m_table.values())
        return writer
        
    #not coded on the fly is supported 
    def GenerateMachineLearingTestTable(self,testDataFilePath,filePath):
        
        if os.path.exists(filePath):
            os.remove(filePath)
        
        csv_H = open(filePath,"wb")
        writer = self.__StartFile(csv_H)
        writer.writerow(self.m_table.values())
        print "test Set file is=%s"% testDataFilePath
        
        if not os.path.exists(testDataFilePath):
            self.LogPrint("ERROR :missing test set data graph...")
            return
        
        testuserDb = users_DB_graph_c.user_DB_graph_c(testDataFilePath,self.m_graph)
        testUser2SubDic= testuserDb.GetUsers2SubjectDic().copy()
        trainUser2SubDic = self.m_user2subject
        skipSubjects =0
        totalSubject=0
        outsideSubject=[]
        for user,subjects in testUser2SubDic.items():
            #running on each user
            for subject in subjects :
                totalSubject+=1
                rowlist=[]
                rowlist.append(user)
                rowlist.append(subject)
                rowlist.append(len(subjects))
                if not user in trainUser2SubDic.keys():
                    self.LogPrint("Error the user%s in not in the train set graph , please check data "% user)
                    continue
                usersFromSubList = self.m_userDB.GetUsersFromSubject(subject)
                if usersFromSubList==None:
                    self.LogPrint("subjet not exist...will skip this row ")
                    skipSubjects+=1
                    outsideSubject.append(subject)
                    continue
                rowlist.append(len( usersFromSubList))
                rowlist.append(1) #the testing column
                for subjectList in self.m_groupSubjectList.values():
                                            
                        if subject in subjectList:
                            existIn =1
                            #print "found %s in group %s index list = %d r" %(subStr,groupName,indexGroup)
                        else:
                            existIn = 0
                        rowlist.append(existIn)
                #add to column if user exist in at clusterX 
                for group in self.m_clusterGroups:
                    groupName = group[0]
                    
                    if self.m_userInGroup.has_key(user):
                        if groupName in  self.m_userInGroup[user]:
                            rowlist.append(1)
                        else:
                            rowlist.append(0)
                    else:
                        rowlist.append(0)
                writer.writerow(rowlist)
                
        
        csv_H.close()
        self.LogPrint("done creating machine learning table total subject that didn't found at trainSet:%d total subjects=%d"% (skipSubjects,totalSubject))
            
        
    
    def GenerateMahineLearingTable(self,filePath):
        
        if self.m_userDB == None:
            self.LogPring("m_userDB is empty ... can't continue will return ")
            return None
        users2Subjects=self.m_user2subject #for performance we can replace 
        if os.path.exists(filePath):
            os.remove(filePath)
        
        csv_H = open(filePath,"wb")
        
        self.m_writer= self.__StartFile(csv_H)
        self.m_writer.writerow(self.m_table.values())
        #for user,subjects in self.m_user2subjectItem:
        userGraphList = self.m_userDB.GetUsersGraph()
        for user in userGraphList:
            subjects = users2Subjects[user]
            haveSubjectInGroup=[]
            for i in range(0, self.m_numGroups):
                haveSubjectInGroup.append(False)
            for subject in subjects:
                rowList=[]
                #for in case we what to coded our data on the fly  
                usrStr = user
                if usrStr != None:
                    if self.m_isGraphEncoded:
                        rowList.append(utils.EncodeString(usrStr))
                    else:
                        rowList.append(usrStr)
                else:
                    self.LogPrint("no user ... will continue")
                    continue
                #subStr = self.__getEncodedValue(subject) if self.m_isGraphEncoded else subject
                subStr = subject
                if subStr == None :
                    self.LogPrint("problem with some subject... (is None)")
                else:
                    if self.m_isGraphEncoded:
                        rowList.append(utils.EncodeString(subStr))
                    else:
                        rowList.append(subStr) 
                    sublen= len(subjects)
                    rowList.append(sublen)
                    usersFromSub = self.m_userDB.GetUsersFromSubject(subStr)
                    if usersFromSub == None :
                        self.LogPrint("no user found for %s subject" % subStr)
                        lenUser=0
                    else:
                        lenUser=len(usersFromSub)
                    rowList.append(lenUser)
                    #fake or not 
                    if self.m_fakeUsers2Subject.has_key(user):
                        if subject in self.m_fakeUsers2Subject[user]:
                            rowList.append(0)
                        else:
                            rowList.append(1)
                    
                    else:
                        rowList.append(0)                    
                    
                    #print  self.m_groupSubjectList
                    for subjectList in self.m_groupSubjectList.values():
                                            
                        if subStr in subjectList:
                            existIn =1
                            #print "found %s in group %s index list = %d r" %(subStr,groupName,indexGroup)
                        else:
                            existIn = 0
                        rowList.append(existIn)
                #add to column if user exist in at clusterX 
                for group in self.m_clusterGroups:
                    groupName = group[0]
                    
                    if self.m_userInGroup.has_key(user):
                        if groupName in  self.m_userInGroup[user]:
                            rowList.append(1)
                        else:
                            rowList.append(0)
                    else:
                        rowList.append(0)
                                            
                #print "row is =", rowList
                #print "==================================================================================================="
                self.m_writer.writerow(rowList)
                
            # for i in range(0,self.m_numGroups):
                #print "index=%d"%i
                #toInser=1 if haveSubjectInGroup[i] else 0
                #rowList.append(toInser)
            
            
        csv_H.close()
        self.LogPrint("!done create machine learing table is done - closing file %s"%filePath)                    
                        
                
                    
                    
                    
                     
            
            
               
            
            
                
            
             
        
        
        
        
            
            
        
        
    
    