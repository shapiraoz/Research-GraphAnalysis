
import community
import csv
import os
from utils import SaveStatistics2File
import utils
import networkx



dendorgram = None

CSV_COMMUNITIES_SIZE_FILE="communitiesSize.csv"
CSV_COMMUNITIES_MEMBERS_IDS="communitiesMemberIDS.csv"
CSV_COMMUNITIES_MEMBERS="communitiesMember.csv"
CSV_GROUP_SUM = "groups_statistics.csv"

SIGNIFICAT_WEIGHT = 1

comSize={}
comsizeClean={}
comMem={}
comMemClean={}
comMemNames={}
comDegAvg={}
comWeight={}
partition = None

def LogPrint(strMsg):
    utils.LOG(strMsg)
    print strMsg

def InitClusterAnalysis(graph):
    global comMemClean
    global comMemNames
    global comsizeClean
    global partition
    print "starting best partition algorithm (will take a while)...."
    partition = community.best_partition(graph)
    modularity = community.modularity(partition, graph)
    LogPrint("the modularity is %f"%modularity)
    if partition !=None:
        for node in partition.iteritems():
            if comSize.has_key(node[1]):
                comSize[node[1]]= comSize[node[1]]+1
                comMem[node[1]].append(node[0])
            else:
                comSize[node[1]]=1
                comMem[node[1]]=[]
    for cSize in comSize.iteritems():
        if cSize[1] >1:
            print "cSize[1]=",cSize[1]
            comsizeClean[cSize[0]] =cSize[1]
            if len(comMem[cSize[0]])==1:
                print "way this value is only one member...",comMem[cSize[0]]
            comMemClean[cSize[0]] = comMem[cSize[0]]
    
    for memberIDs in comMemClean.iteritems():
        comMemNames[memberIDs[0]]=[]
        for member in memberIDs[1]:
            comMemNames[memberIDs[0]].append(utils.GetNodeName(member,graph))  
           
def ShowResultCluster():
    strmsg = "summary results for communities with more them one member :\n number of communities : %d" % len(comSize)
    LogPrint( strmsg)
    LogPrint( "saving data in %s file...." % CSV_COMMUNITIES_SIZE_FILE)
    SaveStatistics2File(CSV_COMMUNITIES_SIZE_FILE, ['community number ','member size'], comsizeClean)
    LogPrint( "done")
    LogPrint( "saving data ids on members in %s file...."%  CSV_COMMUNITIES_MEMBERS_IDS)
    SaveStatistics2File(CSV_COMMUNITIES_MEMBERS_IDS , ['community number','members ids'], comMemClean)
    LogPrint( "done" )   
    LogPrint( "saving data on members in %s file...")
    SaveStatistics2File(CSV_COMMUNITIES_MEMBERS,['community number','members'],comMemNames) 
    
    
# performance    
def AddGroupsWeight(groupId,edgeGroupList):
    global comWeight
    weightList =[]
    for item in edgeGroupList:
        weightList.append(item[1])
    comWeight[groupId]=weightList     

def MinMaxList2(edge2weightList): 
    minList = min(edge2weightList,key=lambda item:item[1])   
    maxList = max(edge2weightList,key=lambda item:item[1])
    #sumList = sum(edge2weightList,key=lambda item:item[1])
    #avg = sumList/len(edge2weightList)
    return minList[1],maxList[1]
    
def AvgMinMaxList(list):
    sum =0
    for item in list:
        sum=sum+item
    avg = sum/len(list)
    minList = min(list)
    maxlist = max(list)
    return avg,minList,maxlist    
    
    
def GetEdgeNodeName(edge2weightList,graph,index):    
    name1a = utils.GetNodeName(edge2weightList[index][0][0],graph)
    name1b = utils.GetNodeName(edge2weightList[index][0][1],graph)
    returnStr = "%s__2__%s"%(name1a,name1b)
    return returnStr
    #return   
      
def ReturnNameWeight(index,edge2weightList,graph):
    name=None
    weight=0
    if index > 0:
        name= GetEdgeNodeName(edge2weightList,graph,index)
        weight=edge2weightList[index][1]
    return name,weight 
      
def StrongestEdgesItems(edge2weightList,graph):
    #last = len(edge2weightList)
    foundList = FindStrongestEdgesItems(edge2weightList,3,graph)
    name1 ,weight1 = foundList[0]
    name2, weight2 = foundList[1]
    name3, weight3 = foundList[2]
    #name1 ,weight1 = ReturnNameWeight(last-1, edge2weightList, graph)
    #name2 ,weight2 = ReturnNameWeight(last-2,edge2weightList, graph)
    #name3 ,weight3 = ReturnNameWeight(last-3 ,edge2weightList, graph)
    return name1,weight1,name2,weight2,name3,weight3
    
def FindStrongestEdgesItems(edge2weightList,numItem,graph):
    nameWeightList=[]
    last =len(edge2weightList)
    for i in range(1,numItem+1):
        nameWeightList.insert(i, ReturnNameWeight(last-i,edge2weightList,graph))
    return nameWeightList
    
def FindEdges2(nodeList,graph): 
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
   
def FindEdges(nodeList,graph):
    
    edgeList =[] #sort list
    
    for edge in graph.edges_iter():
        name1 = utils.GetNodeName(edge[0],graph)
        name2 = utils.GetNodeName(edge[1],graph)
        if name1 == None or name2 == None or name1 == name2:
            continue
        weight = graph[edge[0]][edge[1]]['weight']
        if edge[0] in nodeList and edge[1] in nodeList and weight > SIGNIFICAT_WEIGHT : 
            item=[edge,weight]
            edgeList.append(item)
            
    edgeList.sort(key=lambda item:item[1])
    #print edgeList
    return edgeList    
    
def GetWeightEdge(edge2weightList):
    weightList=[]
    for edge in edge2weightList:
        weight = edge[1]
        if (weight!= None):
            weightList.append(weight)
    return weightList
    
def RunClusterStatistics(graph):
    global comDegAvg
    
    LogPrint("Run Cluster Statistics...")
    LogPrint("=======================================================================")
    if os.path.exists(CSV_GROUP_SUM):
        os.remove(CSV_GROUP_SUM)
    csvFile = open(CSV_GROUP_SUM,"wb")
    writer = csv.writer(csvFile,delimiter=",",quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['group number','number of subjects','number of edges', 'minimum Degree','Average Degree','maximum Degree','minimum weight','Average weight','maximum weight', 'the strongest edge','weight first','second edge','weight second','third edge','weight third'])
    if comMemClean==None or len(comMemClean)==0:
        LogPrint( "error cluster was not init !!!" )
        return  
    LogPrint( "size of comMemClean= %d "% len(comMemClean))
    for group in comMemClean.iteritems():
        maxDeg =0
        minDeg =10000000
        maxWeight = -1
        minWeight = -1
        numMembers = len(group[1])
        LogPrint("statistics for group %s:"%group[0])
        sumGroup=0
        for node in group[1]:
            deg = graph.degree(node)
            if maxDeg < deg:
                maxDeg = deg
            if minDeg > deg:
                minDeg =deg
            sumGroup=sumGroup+deg
        avgDeg =  sumGroup/numMembers
        comDegAvg[group[0]]= avgDeg 
        msg =" the avg degree of the group %s is %d" % (group[0]  , avgDeg)
        LogPrint(msg)
        edgeList,sumEdgesWieghtList = FindEdges2(group[1],graph)
        #edgeList = FindEdges(group[1],graph)
        edgeListLen = len(edgeList)
        if (edgeListLen == 0):
            LogPrint("group don't have edges....")
        else:
            avgWeight =sumEdgesWieghtList/edgeListLen 
            LogPrint ("number edges=%d" % edgeListLen)
            WeightList = GetWeightEdge(edgeList)
            #avgWeight,minWeight,maxWeight = AvgMinMaxList(WeightList)
            minWeight,maxWeight = MinMaxList2(edgeList)
            LogPrint("avg weight is %f" % avgWeight  )
            name1,weight1,name2,weight2,name3,weight3 = StrongestEdgesItems(edgeList, graph)
            LogPrint( "names for insert :%s,%s,%s"% (name1,name2,name3))
            
            writer.writerow([group[0],numMembers,edgeListLen,minDeg,avgDeg,maxDeg,minWeight,avgWeight,maxWeight,name1,weight1,name2,weight2,name3,weight3])
    LogPrint("Done!!!")
    csvFile.close()
        
def RunBestPartitionIndex(graph):
    global partition
    print "partition len before: %d"%len(partition)
    partition = community.best_partition(graph, partition)
    print "partition len after %d"% len(partition)
    
        
        
def GenerateDendorgram(graph):
    global dendorgram
    dendorgram = community.generate_dendogram(graph)
    

def GetDendorgram():
    return dendorgram

   