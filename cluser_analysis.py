
import community
import csv
import os
from utils import SaveStatistics2File
import utils



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

def LogPrint(strMsg):
    utils.LOG(strMsg)
    print strMsg

def InitClusterAnalysis(graph):
    global comMemClean
    global comMemNames
    global comsizeClean
    print "starting best partition algorithm (will take a while)...."
    partition = community.best_partition(graph)
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
    print strmsg
    print "saving data in",CSV_COMMUNITIES_SIZE_FILE,"file..."
    SaveStatistics2File(CSV_COMMUNITIES_SIZE_FILE, ['community number ','member size'], comsizeClean)
    print "done"
    print "saving data ids on members in" ,  CSV_COMMUNITIES_MEMBERS_IDS ,"file..."
    SaveStatistics2File(CSV_COMMUNITIES_MEMBERS_IDS , ['community number','members ids'], comMemClean)
    print "done"    
    print "saving data on members in ",CSV_COMMUNITIES_MEMBERS,"files..."
    SaveStatistics2File(CSV_COMMUNITIES_MEMBERS,['community number','members'],comMemNames) 
    
    
    
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
      
def StrongestEdgesItems(edge2weightList,graph):
    name1= GetEdgeNodeName(edge2weightList,graph,0)
    name2= GetEdgeNodeName(edge2weightList,graph,1)
    name3= GetEdgeNodeName(edge2weightList,graph,2)
    return name1,name2,name3
    
def FindEdges(nodeList,graph):
    edgeList =[] #sort list
   
    for edge in graph.edges_iter():
        weight = graph[edge[0]][edge[1]]['weight']
        name1 = utils.GetNodeName(edge[0],graph)
        name2 = utils.GetNodeName(edge[1],graph)
        if edge[0] in nodeList and edge[1] in nodeList and weight > SIGNIFICAT_WEIGHT and name1 != name2: 
            #insert to sort list
            item=[edge,weight]
            if len(edgeList) == 0:
                edgeList.append(item)
                continue
            index=0 
            for runItem in edgeList :
                if runItem[1] < weight :
                    break
                index=index+1
            edgeList.insert(index, item)
                                
            #edgeList[weight]=edge # can be problem if there is the same weight 
    
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
    writer.writerow(['group number','number of subjects', 'minimum Degree','Average Degree','maximum Degree','minimum weight','Average weight','maximum weight', 'the strongest edge','second edge','third edge'])
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
        edgeList = FindEdges(group[1],graph)
        edgeListLen = len(edgeList)
        avgWeight = 0
        if (edgeListLen == 0):
            LogPrint("group don't have edges....")
        else:
            LogPrint ("number edges=%d" % edgeListLen)
            WeightList = GetWeightEdge(edgeList)
            avgWeight,minWeight,maxWeight = AvgMinMaxList(WeightList)
            LogPrint("avg weight is %f" % avgWeight  )
        name1,name2,name3 = StrongestEdgesItems(edgeList, graph)
        LogPrint( "names for insert :%s,%s,%s"% (name1,name2,name3))
        writer.writerow([group[0],numMembers,minDeg,avgDeg,maxDeg,minWeight,avgWeight,maxWeight,name1,name2,name3])
    LogPrint("Done!!!")
    csvFile.close()
        
def GenerateDendorgram(graph):
    global dendorgram
    dendorgram = community.generate_dendogram(graph)

def GetDendorgram():
    return dendorgram

   