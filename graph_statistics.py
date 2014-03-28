
import networkx as nx
import os
import csv
import logging
from utils import SaveStatistics2File  
from utils import GetNodeName

import utils


weightDist = {}
degreeDist = {}
subject2Degree={}

CSV_SUB_2_DEGREE = "%s/subject2degrees.csv" % utils.DEF_RESULT_DIR
CSV_DEGREE_DIS = "%s/degree2distribution.csv" % utils.DEF_RESULT_DIR
CSV_DEGREE_WEIGHT_CORR = "%s/degreeWeightCorrlation.csv"% utils.DEF_RESULT_DIR
CSV_WEIGHT_FREQUENT = "%s/weightsFrequent.csv"% utils.DEF_RESULT_DIR



   
args_size=0  
graph_path = ""

NODE_INDEX=0
NODE_DETAILES_INDEX=1
    
    
def LOG(strMsg):
    utils.LOG(strMsg)
    
def StartLog():
    utils.StartLog()
      

def FillNodeName(graph):
    utils.FillNodeName(graph)
    #print nodeNameList  

def Init(graph):
    StartLog()
    FillNodeName(graph)
        
def LoadGraph(path):
    if not os.path.exists(path):
        print "file %s not exist will exit!!!" % path
        return
    graph = nx.read_graphml(path)
    print "graph is loaded from path %s" % path 
    nodes_len=len(graph.nodes())
    edges_len=len(graph.edges())
    LOG("graph loaded with number of nodes=%d"%nodes_len)
    LOG("graph loaded with number of edges=%d"%edges_len)
    return graph


def printLine():
    print "========================================================================"

  
def DegreeAnayltor(graph):
    empty_nodes=0
    zeroDegree =0
    maxDegree=0
    minDegree=1000000
    maxIndex = None
    minIndex = None 
    avgDeg =0
    sumDeg =0
    count=0
    printLine()
    print "analyze node degree distribution ..."
    for node in utils.GetNodeNameList().iteritems():
        deg = graph.degree(node[NODE_INDEX])
        name = node[1]
        if deg > 0 and name:
            sumDeg = sumDeg+deg
            count = count+1
            subject2Degree[name]=deg
            if deg > maxDegree:
                maxDegree = deg
                maxIndex = node[0]
            if deg < minDegree:
                minDegree = deg
                minIndex = node[0] 
            if deg in degreeDist :
                degreeDist[deg] = degreeDist[deg] + 1
            else:
                degreeDist[deg] = 1 
        else :
            if not name:
                empty_nodes = empty_nodes+1
            else :
                zeroDegree=zeroDegree+1  
    msg="there is %d nodes with 0 degree" % zeroDegree
    LOG(msg)
    msg= "there is %d empty nodes" % empty_nodes
    LOG(msg)     
    avgDeg=sumDeg/count
    print "saving degree distribution in", CSV_DEGREE_DIS ,"file "
    SaveStatistics2File(CSV_DEGREE_DIS,['degree','num'] , degreeDist)
    print "saving subject to degree in %s file" % CSV_SUB_2_DEGREE
    SaveStatistics2File(CSV_SUB_2_DEGREE, ['subject','degree'], subject2Degree)
    print "the node with the maxmum degree is", GetNodeName(maxIndex,graph) , "with degree of" , maxDegree
    print "the node with the minimum degree is  " ,GetNodeName(minIndex,graph) , "with " ,minDegree," degree "
    print "the average degree in the graph is %d" % avgDeg
   
    
def EdgesAnayltor(graph):
    maxWeight = 0
    sumWeight = 0
    maxIndex =None
    printLine()
    print "analyzing weight distribution..." 
     
    countWeight =0 # len (allWeights)
    minWeight = graph[graph.edges()[0][0]][graph.edges()[0][1]]['weight'] 
    for edge in   graph.edges_iter():
        weight = graph[edge[0]][edge[1]]['weight']
                
        name1= GetNodeName(edge[0],graph)
        name2= GetNodeName(edge[1],graph)
        if  name1!= None and name2 != None and name1 != name2:
            if weight in weightDist :
                weightDist[weight]  = weightDist[weight]+1 
            else:
                weightDist[weight] = 1  
            sumWeight = sumWeight + weight
            countWeight = countWeight+1
            if weight >  maxWeight :
                maxWeight = weight
                maxIndex = edge
            if minWeight  > weight:
                minWeight = weight
                 
    avgWeight = sumWeight/countWeight
    print "...done!!"
    print  "the avg of the weight is" ,avgWeight  #, " the sumWeight is " , sumWeight
    print "the srongest link is", maxWeight , "between",GetNodeName(maxIndex[0],graph) ,"to" ,GetNodeName(maxIndex[1],graph) 
    print "the minimal weight is",minWeight
    allweights  = weightDist.keys()
    allweights.sort()
    SaveStatistics2File(CSV_WEIGHT_FREQUENT,['edge weight','frequent'],weightDist)
    index =(len(allweights)/2)
    print index 
    print "the median is : %d " % allweights[index]  
    
        
def  NodeDegreeCorrelation(graph):
    if len(utils.GetNodeNameList())==0:
        FillNodeName(graph)
    printLine()
    genCount = 0.0
    missCorrel = 0.0;
    print "analyze the correlation between weight average to degree... "
    if os.path.exists(CSV_DEGREE_WEIGHT_CORR):
        os.remove(CSV_DEGREE_WEIGHT_CORR)
    csvFile = open(CSV_DEGREE_WEIGHT_CORR,"wb")
    writer = csv.writer(csvFile,delimiter=",",quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['name','degree','avg weight'])
    for node in nx.get_node_attributes(graph, 'name').iteritems():
        genCount = genCount+1
        nodeID = node[0]
        nodeDeg = graph.degree(nodeID)
        if nodeDeg!=0 and node[1]:
            neighbors = graph.neighbors(nodeID)
            neighborSize = len(neighbors)
            weightSum=0
            for neighborID in neighbors:
                weightSum = weightSum + graph[nodeID][neighborID]['weight']
            nodeWeightAvg = weightSum/neighborSize     
            #print "the node",node[1] ,"have degree" ,nodeDeg , "the avg  Weight is", nodeWeightAvg
            writer.writerow([node[1],nodeDeg,nodeWeightAvg])
            #degreeCorrelation[nodeDeg]=nodeDeg
        else:
            missCorrel = missCorrel+1    
    csvFile.close()       
    persent = (missCorrel/genCount)*100
    msg ="there is " ,missCorrel,"genCount = ",genCount," missing information item that are ", persent ,"of total";
    LOG(msg)        
    print msg
    print "done saving correlation between degree to node average weight ,please check %s file" % CSV_DEGREE_WEIGHT_CORR
    
