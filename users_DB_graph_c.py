'''

@author: oz
'''
import os
from base_c import base_c
import csv
import re
import utils
from UserList import UserList


class user_DB_graph_c(base_c):

   
    def __init(self):
               
        if not os.path.exists( self.m_data_file_path):
            self.LogPrint("csv data file(%s) not found ... will return -1" % self.m_data_file_path)
            return -1
       
  
    def __init__(self,graph=None,dataBaseCSVFilePath):
        self.m_data_file_path=dataBaseCSVFilePath
        self.m_graph=graph
        self.m_is_loaded=False
        self._REGEX_SUBJECT="[\w\d?!_&:\-/)(\".<>='+]+,"
        self.m_sub2UserDic={} #subject  are the keys
        self.m_user2subDic={} #users    are the keys
        self.__init() 
        self.LoadDics()
       
        
        
        
    def __AddToSub2User(self,subject,user):
        if not subject in self.m_sub2UserDic:
            userlist=[]
            self.m_sub2UserDic[subject] =userlist
        self.m_sub2UserDic[subject].append(user)
        
        
        
    def LoadDics(self):
        if not os.path.exists( self.m_data_file_path):
            self.LogPrint("csv data file(%s) not found ... will return -1" % self.m_data_file_path)
            return -1
        ifile  = open(self.m_data_file_path, "rb")
        reader = csv.reader(ifile)
        user=""
        for row in reader:
            column = 0
            for col in row:
                if column==0:
                    user = col
                    #print "user=%s"%user
                    if not user=="":
                        if not user in self.m_user2subDic:
                            subjectList=[]
                            self.m_user2subDic[user]=subjectList
                else:
                   
                    if not user=="":
                        subj = col
                        if subj==None or subj=="":
                            continue
                        #print "subject=%s"%subj
                        self.m_user2subDic[user].append(subj)
                        if not subj in self.m_sub2UserDic:
                            usersList =[]
                            self.m_sub2UserDic[subj]=usersList
                        self.m_sub2UserDic[subj].append(user)
                column+=1
                
        ifile.close()                
        self.m_is_loaded=True
                    
        
    def FindRawSubjects(self,subject1,subject2,update=False):
        ret=False
        print "subject1=%s ,subject2=%s"%(subject1,subject2)
        if subject1 == None or subject2 == None or subject1 == subject2:
            return ret
        with open(self.m_data_file_path, 'r') as inF:
            for line in inF:
                cleanLine= utils.clean_string(line)
                #print "Line=%s\n"%line
                #if subject1 in line and subject2 in cleanLine:
                if not cleanLine.find(subject1) == -1 and not cleanLine.find(subject2) ==-1:
                    matchObj= re.match(self._REGEX_SUBJECT, line, flags=0)
                    if matchObj:
                        user = matchObj.group()
                        #print user
                        if not user == "":
                            #print "found user %s for subject %s and subject %s update dics.." %(user,subject1,subject2)
                            ret=True
                            if update:
                                if not user in self.m_user2subDic:
                                    subjectsList=[]
                                    self.m_user2subDic[user]=subjectsList
                                self.m_user2subDic[user].append(subject1)
                                self.m_user2subDic[user].append(subject2)
                                self.__AddToSub2User(subject1, user)
                                self.__AddToSub2User(subject2, user)
        return ret                
   
    def GetUsersGraph(self):
        if self.m_graph==None:
            self.LogPrint("Error:no graph is loaded for get users!!!")
            return None
        edges = self.m_graph.edges()
        usersList=[]
        for edge in edges:
            sub1 = utils.GetNodeName(edge[0],self.m_graph)
            sub2 = utils.GetNodeName(edge[1],self.m_graph)
            if sub1==None or sub2==None or sub1==sub2:
                continue
            if sub1 in self.m_sub2UserDic:
                #
                for user in self.m_sub2UserDic[sub1]:
                    if sub2 in self.m_sub2UserDic:
                        if user in self.m_sub2UserDic[sub2]:
                            if not user in usersList:
                                usersList.append(user)
                                break
        return usersList
    
   
    def GetNumUsersGraph(self):
        
        return len(self.GetUsersGraph())
                        
    def GetCopyUser2SubjectsDic(self):
        return self.m_user2subDic.copy()
        
    def GetCopySubjecst2UsersDir(self):
        return self.m_sub2UserDic.copy()    
        
    def IsSubjectInUser(self,user,subject):
        if subject in self.m_sub2UserDic :
            if user in self.m_sub2UserDic[subject]:
                return True
        return False
    
    def IsUserHadSubject(self,user,subject):
        if user in self.m_user2subDic:
            if subject in self.m_user2subDic[user]:
                return True
        return False
            
    def GetUsersFromSubject(self,subject):
        if subject in self.m_sub2UserDic:
            return self.m_sub2UserDic[subject] 
        return None
    
    def GetSubjectsFromUser(self,user):
        if user in self.m_user2subDic:
            return self.m_user2subDic[user]
        return None
    
    def IsLoaded(self):
        return self.m_is_loaded
    
    def GetSubject2UsersDic(self):
        return self.m_sub2UserDic
    
    def GetUsers2SubjectDic(self):
        return self.m_user2subDic
                
    def GetNumOfDBUsers(self):
        return len(self.m_user2subDic)