
import community
import csv
import os
from utils import SaveStatistics2File
import utils
import networkx
import time
import classifier_c

class cluster_analysis_c :
    
    def __LogPrint(self,strMsg):
        utils.LOG(strMsg)
        print strMsg
    
    def __init__(self,graph,classifier = None):
        
        self.SUBGRAPH_MEMBERS_CRITERIA =500
        self.SUBGRAPH_EDGE_CRITERIA =75
        self.m_graph = graph
        self.m_comSize={}
        self.m_comsizeClean={}
        self.m_comMem={}
        self.m_comMemClean={}
        self.m_comMemNames={}
        self.m_comDegAvg={}
        self.m_comWeight={}
        self.m_partition = None
        self.__m_dendorgram =None
        self.__CSV_COMMUNITIES_SIZE_FILE="%s/communitiesSize_%s.csv" % (utils.RESULT_DIR,self.m_graph.name)
        self.__CSV_COMMUNITIES_MEMBERS_IDS="%s/communitiesMemberIDS_%s.csv"%(utils.RESULT_DIR, self.m_graph.name)
        self.__CSV_COMMUNITIES_MEMBERS="%s/communitiesMember_%s.csv"% (utils.RESULT_DIR,self.m_graph.name)
        self.__CSV_GROUP_SUM = "%s/groups_statistics_%s.csv"% (utils.RESULT_DIR,self.m_graph.name)
        self.m_classifier=classifier
        self.__InitClusterAnalysis()
       
    
    def SetClassifier(self,classifier):
        self.m_classifier=classifier
    
    def __InitClusterAnalysis(self):
              
        print "starting best m_partition algorithm (will take a while)...."
        if self.m_classifier==None:
            classifier = classifier_c.classifier_c(self.m_graph)
            self.m_partition = classifier.run_classifier(classifier_c.classifier_type_e.e_bestPractice)  #community.best_partition(self.m_graph)
            modularity = community.modularity(self.m_partition,self.m_graph)
            self.__LogPrint("the modularity is %f"%modularity)
        else:
            self.m_partition=self.m_classifier.classifey()
        if self.m_partition==None:
            self.__LogPrint("partition is NULL...will not create cluster, exit")
            return
        #__LogPrint(self,"the modularity is %f"%modularity)
        else:
            for node in self.m_partition.iteritems():
                if self.m_comSize.has_key(node[1]):
                    self.m_comSize[node[1]]= self.m_comSize[node[1]]+1
                    self.m_comMem[node[1]].append(node[0])
                else:
                    self.m_comSize[node[1]]=1
                    self.m_comMem[node[1]]=[]
        for cSize in self.m_comSize.iteritems():
            if cSize[1] >1:
                self.__LogPrint("cSize[1]=%d"%cSize[1])
                self.m_comsizeClean[cSize[0]] =cSize[1]
                if len(self.m_comMem[cSize[0]])==1:
                    self.__LogPrint( "have value is only one member...%d")
                self.m_comMemClean[cSize[0]] = self.m_comMem[cSize[0]]
        
        for memberIDs in self.m_comMemClean.iteritems():
            self.m_comMemNames[memberIDs[0]]=[]
            for member in memberIDs[1]:
                self.m_comMemNames[memberIDs[0]].append(utils.GetNodeName(member,self.m_graph))  
               
    def ShowResultCluster(self):
        strmsg = "summary results for communities with more them one member :\n number of communities : %d" % len(self.m_comSize)
        self.__LogPrint( strmsg)
        self.__LogPrint( "saving data in %s file...." % self.__CSV_COMMUNITIES_SIZE_FILE)
        SaveStatistics2File(self.__CSV_COMMUNITIES_SIZE_FILE, ['community number ','member size'],self.m_comsizeClean)
        self.__LogPrint( "done")
        self.__LogPrint( "saving data ids on members in %s file...."%  self.__CSV_COMMUNITIES_MEMBERS_IDS)
        SaveStatistics2File(self.__CSV_COMMUNITIES_MEMBERS_IDS , ['community number','members ids'],self.m_comMemClean)
        self.__LogPrint( "done" )   
        self.__LogPrint( "saving data on members in %s file...")
        SaveStatistics2File(self.__CSV_COMMUNITIES_MEMBERS,['community number','members'],self.m_comMemNames) 
        
        
    # performance    
    def __AddGroupsWeight(self,groupId,edgeGroupList):
        weightList =[]
        for item in edgeGroupList:
            weightList.append(item[1])
        self.m_comWeight[groupId]=weightList     
    
    def __MinMaxList2(self,edge2weightList): 
        minList = min(edge2weightList,key=lambda item:item[1])   
        maxList = max(edge2weightList,key=lambda item:item[1])
        #sumList = sum(edge2weightList,key=lambda item:item[1])
        #avg = sumList/len(edge2weightList)
        return minList[1],maxList[1]
        
    def __AvgMinMaxList(self,list):
        sum =0
        for item in list:
            sum=sum+item
        avg = sum/len(list)
        minList = min(list)
        maxlist = max(list)
        return avg,minList,maxlist    
        
        
    def __GetEdgeNodeName(self,edge2weightList,graph,index):    
        name1a = utils.GetNodeName(edge2weightList[index][0][0],graph)
        name1b = utils.GetNodeName(edge2weightList[index][0][1],graph)
        returnStr = "%s__2__%s"%(name1a,name1b)
        return returnStr
        #return   
          
    def __ReturnNameWeight(self,index,edge2weightList,graph):
        name=None
        weight=0
        if index > 0:
            name= self.__GetEdgeNodeName(edge2weightList,graph,index)
            weight=edge2weightList[index][1]
        return name,weight 
          
    def __StrongestEdgesItems(self,edge2weightList,graph):
        #last = len(edge2weightList)
        foundList = self.__FindStrongestEdgesItems(edge2weightList,3,graph)
        name1 ,weight1 = foundList[0]
        name2, weight2 = foundList[1]
        name3, weight3 = foundList[2]
        #name1 ,weight1 = ReturnNameWeight(last-1, edge2weightList, graph)
        #name2 ,weight2 = ReturnNameWeight(last-2,edge2weightList, graph)
        #name3 ,weight3 = ReturnNameWeight(last-3 ,edge2weightList, graph)
        return name1,weight1,name2,weight2,name3,weight3
        
    def __FindStrongestEdgesItems(self,edge2weightList,numItem,graph):
        nameWeightList=[]
        last =len(edge2weightList)
        for i in range(1,numItem+1):
            nameWeightList.insert(i, self.__ReturnNameWeight(last-i,edge2weightList,graph))
        return nameWeightList
        
    def __FindEdges2(self,nodeList,graph): 
        edgeList =[]
        foundNode=[]
        sum=0
        print "start findEdge..."
        edges =  graph.edges()
        for node in nodeList:
            for nodeNeb in graph.neighbors(node):
                if nodeNeb in nodeList:
                    name1 = utils.GetNodeName(nodeNeb,graph)
                    name2 = utils.GetNodeName(node,graph)
                    if name1!=None and name2!=name1 and name2!=None and  (not node in foundNode and not nodeNeb in foundNode) :
                        item1 =(str(node),str(nodeNeb))
                        item2 = (str(nodeNeb),str(node))
                        item=None
                        if item1 in edges:
                            weight=graph[node][nodeNeb]['weight']
                            item =[item1,weight]
                        else:
                            if item2 in edges:
                                weight =graph[nodeNeb][node]['weight']
                                item = [item2,weight]
                        if item!=None:
                            sum = sum +weight
                            edgeList.append(item)
                            foundNode.append(nodeNeb)
                            foundNode.append(node)
                        else:
                            print "not working!!!!!"
        edgeList.sort(key=lambda item:item[1])
        #print edgeList
        return edgeList,sum
       
    def __FindEdges(self,nodeList,graph):
        
        edgeList =[] #sort list
        
        for edge in graph.edges_iter():
            name1 = utils.GetNodeName(edge[0],graph)
            name2 = utils.GetNodeName(edge[1],graph)
            if name1 == None or name2 == None or name1 == name2:
                continue
            weight = graph[edge[0]][edge[1]]['weight']
            if edge[0] in nodeList and edge[1] in nodeList and weight > 1 : 
                item=[edge,weight]
                edgeList.append(item)
                
        edgeList.sort(key=lambda item:item[1])
        #print edgeList
        return edgeList    
        
    def __GetWeightEdge(self,edge2weightList):
        weightList=[]
        for edge in edge2weightList:
            weight = edge[1]
            if (weight!= None):
                weightList.append(weight)
        return weightList
        
    def RunClusterStatistics(self):
        self.__LogPrint("Run Cluster Statistics...saving data on %s file" % self.__CSV_GROUP_SUM)
        self.__LogPrint("=======================================================================")
        if os.path.exists(self.__CSV_GROUP_SUM):
            os.remove(self.__CSV_GROUP_SUM)
        
        csvFile = open(self.__CSV_GROUP_SUM,"wb")
        writer = csv.writer(csvFile,delimiter=",",quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['group number','number of subjects','number of edges', 'minimum Degree','Average Degree','maximum Degree','minimum weight','Average weight','maximum weight', 'the strongest edge','weight first','second edge','weight second','third edge','weight third'])
        if self.m_comMemClean==None or len(self.m_comMemClean)==0:
            self.__LogPrint( "error cluster was not init !!!" )
            return  
        self.__LogPrint( "size of m_comMemClean= %d "% len(self.m_comMemClean))
        for group in self.m_comMemClean.iteritems():
            maxDeg =0
            minDeg =10000000
            maxWeight = -1
            minWeight = -1
            numMembers = len(group[1])
            self.__LogPrint("statistics for group %s:"%group[0])
            sumGroup=0
            for node in group[1]:
                deg = self.m_graph.degree(node)
                if maxDeg < deg:
                    maxDeg = deg
                if minDeg > deg:
                    minDeg =deg
                sumGroup=sumGroup+deg
            avgDeg =  sumGroup/numMembers
            self.m_comDegAvg[group[0]]= avgDeg 
            msg =" the avg degree of the group %s is %d" % (group[0]  , avgDeg)
            self.__LogPrint(msg)
            edgeList,sumEdgesWieghtList = self.__FindEdges2(group[1],self.m_graph)
            #edgeList = FindEdges(group[1],graph)
            edgeListLen = len(edgeList)
            if (edgeListLen > self.SUBGRAPH_EDGE_CRITERIA and numMembers > self.SUBGRAPH_MEMBERS_CRITERIA):
                subGraph= networkx.subgraph(self.m_graph, group[1])
                
                subGraph.name="%s.%d"%(self.m_graph.name, group[0])
                ca=cluster_analysis_c(subGraph)
                ca.RunClusterStatistics()
                ca.ShowResultCluster()
                self.__LogPrint("create new subGraph and run the analysis graph name:%s"%subGraph.name)
                
            if (edgeListLen == 0):
                self.__LogPrint("group don't have edges....")
            else:
                avgWeight =sumEdgesWieghtList/edgeListLen 
                self.__LogPrint ("number edges=%d" % edgeListLen)
                #WeightList = GetWeightEdge(edgeList)
                #avgWeight,minWeight,maxWeight = AvgMinMaxList(WeightList)
                minWeight,maxWeight = self.__MinMaxList2(edgeList)
                self.__LogPrint("avg weight is %f" % avgWeight  )
                name1,weight1,name2,weight2,name3,weight3 = self.__StrongestEdgesItems(edgeList,self.m_graph)
                self.__LogPrint( "names for insert :%s,%s,%s"% (name1,name2,name3))
                
                writer.writerow([group[0],numMembers,edgeListLen,minDeg,avgDeg,maxDeg,minWeight,avgWeight,maxWeight,name1,weight1,name2,weight2,name3,weight3])
        self.__LogPrint("Done!!!")
        csvFile.close()
        self.__LogPrint("close %s file "% self.__CSV_GROUP_SUM )
        
            
    def RunBestPartitionIndex(self):
        print "m_partition len before: %d"%len(self.m_partition)
        partition = community.best_partition(self.m_graph, self.m_partition)
        print "m_partition len after %d"% len(self.m_partition)
        return partition 
            
            
    def __GenerateDendorgram(self):
        global dendorgram
        dendorgram = community.generate_dendogram(self.m_graph)
        
    
    def GetDendorgram(self):
        return dendorgram

   