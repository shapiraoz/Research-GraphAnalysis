
import utils
import base_c
import users_DB_graph_c
import cluster_analysis_c


class generate_mac_table_c(base_c):
    
    def __init__(self,graph,cluster_analysis=None,isGraphEncoded=False,stringsHash=None,usersDB=None,dataFilePath=None):
        
        if usersDB==None and dataFilePath != None:
            self.LogPrint("no user DB ,will create user DB ")
            self.m_userDB = users_DB_graph_c.user_DB_graph_c(graph,dataFilePath)
            #need to create the users DB.... without taking all values 
        else:
            self.m_userDB = usersDB
        self.m_userList = self.m_userDB.GetUsersGraph()
        if len(self.m_userList)==0:
            self.LogPrint("no user list from UserDB...can't proceed...")
            return 
        if isGraphEncoded and stringsHash==None :
            self.LogPrint("Error can't work without object for encoded numbers... ")
            return
        if isGraphEncoded and stringsHash != None:
            self.m_isGraphEncoded = isGraphEncoded
            self.m_stringHash = stringsHash
       
        if cluster_analysis==None:
            self.m_cluser_analysis = cluster_analysis_c.cluster_analysis_c(graph,None,self.m_userDB,1)
        else:
            self.m_cluser_analysis = cluster_analysis
       
    def __getEncodedValue(self,strVal):
        varHash=int(strVal)
        if not self.m_stringHash.has_key(varHash):
            self.LogPrint("failed to find value string  %d in the encoded dictionary" % varHash)
            return None
        return self.m_stringHash[varHash]
            
    
    def GenerateMahineLearingTable(self):
        
        if self.m_userDB == None:
            self.LogPring("m_userDB is empty ... can't continue will return ")
            return None
        users2Subjects=self.m_userDB.GetCopyUser2SubjectsDic() #for performance we can replace 
        for user,subjects in users2Subjects:
            rowList=[]
            usrStr = self.__getEncodedValue(user) if self.m_isGraphEncoded else user
            if usrStr != None:
                rowList.append(usrStr)
            else:
                self.LogPrint("no user ... will continue")
                continue
            for subject in subjects:
                subStr = self.__getEncodedValue(subject) if self.m_isGraphEncoded else subject
                if subStr == None :
                    self.LogPrint("problem with some subject... (is None)")
                else:
                    rowList.append(subStr)
                     
            
            
               
            
            
                
            
             
        
        
        
        
            
            
        
        
    
    