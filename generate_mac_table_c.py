
import utils

import users_DB_graph_c
import cluster_analysis_c
from base_c import base_c
import csv
import os

class generate_mac_table_c(base_c):
    
    def __init__(self , graph , cluster_analysis = None , isGraphEncoded = False , stringsHash = None , usersDB = None , dataFilePath = None):
        
        if usersDB==None and dataFilePath != None:
            self.LogPrint("no user DB ,will create user DB ")
            self.m_userDB = users_DB_graph_c.user_DB_graph_c(dataFilePath,graph)
            #need to create the users DB.... without taking all values 
        else:
            self.m_userDB = usersDB
        self.m_userList = self.m_userDB.GetUsersGraph()
        self.m_user2subjectItem = self.m_userDB.GetCopyUser2SubjectsDic().items()
        
        if isGraphEncoded and stringsHash==None :
            self.LogPrint("Error can't work without object for encoded numbers... ")
            return
        self.m_isGraphEncoded = isGraphEncoded
        if isGraphEncoded and stringsHash != None:
            self.m_stringHash = stringsHash
        
        if len(self.m_userList)==0:
            self.LogPrint("no user list from UserDB...can't proceed...")
            #return 
        
       
        if cluster_analysis==None:
            self.m_cluser_analysis = cluster_analysis_c.cluster_analysis_c(graph,None,self.m_userDB,1)
        else:
            self.m_cluser_analysis = cluster_analysis
            
        self.m_clusterGroups = self.m_cluser_analysis.GetClusterGroups().items()
        
        self.__TABLE_FILE_PATH = utils.RESULT_DIR + "/machine_learning_tbl.csv"
        print "init path =%s" % self.__TABLE_FILE_PATH
        self.m_clusters_items = self.m_cluser_analysis.GetClusterGroups().items()
        self.m_table={0:"user",1:"subject",2:"number of subject per user",3:"number of user per subject "}
        self.m_numGroups = len(self.m_clusters_items)
        
        for i in range(0,self.m_numGroups):
            self.m_table[i+4]="subject in cluster %d" % self.m_clusters_items[i][0]  
        for i in range(0,self.m_numGroups):
            self.m_table[i+4+self.m_numGroups] = "user in cluster %d " % self.m_clusters_items[i][0] 
            
        self.__init_GroupBlongToUsers()    
            
            
    def __getEncodedValue(self,strVal):
        varHash=int(strVal)
        if not self.m_stringHash.has_key(varHash):
            self.LogPrint("failed to find value string  %d in the encoded dictionary" % varHash)
            return None
        return self.m_stringHash[varHash]
    
    def __init_GroupBlongToUsers(self):
        if self.m_userDB == None or self.m_cluser_analysis == None :
            self.LogPrint("missing userDb or clustering ... will return ...")
            return
        self.m_userInGroup={}
        
        for group in self.m_clusterGroups:
            
            groupsubjectList = utils.translateNodeList2SubList(group[1])
            
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
                        
      
    
    
    def __StartFile(self):
        
        if os.path.exists(self.__TABLE_FILE_PATH):
            os.remove(self.__TABLE_FILE_PATH)
            
      
        self.m_csvFile = open(self.__TABLE_FILE_PATH,"wb")
        self.m_writer = csv.writer(self.m_csvFile,delimiter=",",quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        print "opening file %s"% self.__TABLE_FILE_PATH
        #self.m_writer.writerow(self.m_table.values())
        return self.m_writer
        
    
    def GenerateMahineLearingTable(self):
        
        if self.m_userDB == None:
            self.LogPring("m_userDB is empty ... can't continue will return ")
            return None
        users2Subjects=self.m_userDB.GetCopyUser2SubjectsDic() #for performance we can replace 
        self.__StartFile()
        self.m_writer.writerow(self.m_table.values())
        #for user,subjects in self.m_user2subjectItem:
        for user in self.m_userDB.GetUsersGraph():
            subjects = users2Subjects[user]
            haveSubjectInGroup=[]
            for i in range(0, self.m_numGroups):
                haveSubjectInGroup.append(False)
            for subject in subjects:
                rowList=[]
                usrStr = self.__getEncodedValue(user) if self.m_isGraphEncoded else user
                if usrStr != None:
                    rowList.append(usrStr)
                else:
                    self.LogPrint("no user ... will continue")
                    continue
                subStr = self.__getEncodedValue(subject) if self.m_isGraphEncoded else subject
                if subStr == None :
                    self.LogPrint("problem with some subject... (is None)")
                else:
                    rowList.append(subStr) 
                    sublen= len(subjects)
                    rowList.append(sublen)
                    users = self.m_userDB.GetUsersFromSubject(subStr)
                    if users == None :
                        self.LogPring("no user found for %s subject" % subStr)
                        lenUser=0
                    else:
                        lenUser=len(users)
                    rowList.append(lenUser)
                    indexGroup=0
                    for group in self.m_clusterGroups:
                                                 
                        groupName = group[0]
                       
                        groupSubjectsIds = group[1]
                        groupSubjects = utils.translateNodeList2SubList(groupSubjectsIds)
                        #print groupSubjects
                        #print subStr
                        existIn= 1 if subStr in groupSubjects else 0
                        rowList.append(existIn)
                        
                        #if existIn == 1:
                        #   haveSubjectInGroup[indexGroup] = True
                        #indexGroup+=1
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
            
            
        self.m_csvFile.close()                    
                        
                
                    
                    
                    
                     
            
            
               
            
            
                
            
             
        
        
        
        
            
            
        
        
    
    