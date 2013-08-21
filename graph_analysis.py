'''
'''


import networkx as nx
import sys
import os
import csv
import datetime
import logging

#if __name__ == '__main__':
    

weightDist = {}
degreeDist = {}
subject2Degree={}

CSV_SUB_2_DEGREE = "subject2degrees.csv"
CSV_DEGREE_DIS = "degree2distribution.csv"
CSV_DEGREE_WEIGHT_CORR = "degreeWeightCorrlation.csv"
CSV_WEIGHT_FREQUENT = "weightsFrequent.csv"

log_file ="graph_analysis.log" 

nodeNameList={}
   
args_size=0  
graph_path = ""

NODE_INDEX=0
NODE_DETAILES_INDEX=1
    
   
def test2( graph  ):
   print graph.edges()[0][0]
   #print graph[graph.edges()[0][0]][graph.edges()[0][1]]['weight'] 
   #for edge in  graph.edges_iter():
   #    print graph[edge[0]][edge[1]]['weight']
   
def test(grpah,index):
    print nx.info(grpah, index)
    

    
def LOG(strMsg):
    logging.debug(strMsg)
    
def StartLog():
    #f_log = open(log_file,'wb')
    #print "starting log file..." 
    logging.basicConfig(filename=log_file,level=logging.DEBUG)
    #msg = "starting run: ",datetime.datetime.now()
    #LOG(msg)    

      
    
def FillNodeName(graph):
    global nodeNameList
    nodeNameList = nx.get_node_attributes(graph, 'name')
    print  "index_name have been init with " ,len(nodeNameList)
    #print nodeNameList  


def Init(graph):
    StartLog()
    FillNodeName(graph)
    
    
#def closeLog():
#    if empty_nodes > 0:
#        msg = "number of empty nodes are:",empty_nodes
#        LOG(msg)
#    if f_log:
#        f_log.close() 
        
def LoadGraph(path):
    if not os.path.exists(path):
        print "file %s not exist will exit!!!" % path
        return
    graph = nx.read_graphml(path)
    print "graph is loaded from path %s" % path 
    return graph

def printLine():
    print "========================================================================"


def GetNodeName(index,graph):
    if index != None:
        #print index
        if nodeNameList.has_key(index):
            return nodeNameList.get(index) 
    return None

def SaveStatistics2File(filePath ,header, dictionary):
    if os.path.exists(filePath):
        os.remove(filePath)
    csvFile = open(filePath,"wb")
    writer = csv.writer(csvFile,delimiter=",",quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header)
    for k,v in dictionary.items():
        writer.writerow([k,v])
    csvFile.close()
  
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
    for node in nodeNameList.iteritems():
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
    
        
            
        #if deg !=0 :
        #    print "node",node,"have degree" , deg
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
    count =0.0
    printLine()
    #print "node list:"
    #print nodeNameList
    print "analyzing weight distribution..." 
    #allWeights =  nx.get_edge_attributes(graph,"weight").items()
    
    countWeight =0 # len (allWeights)
    #old_num =0
    minWeight = graph[graph.edges()[0][0]][graph.edges()[0][1]]['weight'] 
    for edge in   graph.edges_iter():
        weight = graph[edge[0]][edge[1]]['weight']
        #count=count+1
        #num_num= round((count/countWeight)*100)
        #if num_num!=old_num:
        #   old_num=num_num
        #   if num_num %10 == 0:
        #      sys.stdout.write(".")
        if weight in weightDist :
            weightDist[weight]  = weightDist[weight]+1 
        else:
            weightDist[weight] = 1   
        name1= GetNodeName(edge[0],graph)
        name2= GetNodeName(edge[1],graph)
        if  name1!= None and name2 != None and name1 != name2:
            #print "ok"
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
    #print "the srongest link is", maxWeight , " between ",nx.get_node_attributes(graph, "name")[weight[0][0]] ," to " ,nx.get_node_attributes(graph, "name")[weight[0][1]]    #need to fix this!!!     
    print "the srongest link is", maxWeight , "between",GetNodeName(maxIndex[0],graph) ,"to" ,GetNodeName(maxIndex[1],graph) 
    print "the minimal weight is",minWeight
    allweights  = weightDist.keys()
    allweights.sort()
    SaveStatistics2File(CSV_WEIGHT_FREQUENT,['edge weight','frequent'],weightDist)
    index =(len(allweights)/2)
    print index 
    #print allweights
    #print "countWieght = %d" % countWeight
    print "the median is : %d " % allweights[index]  
    #sorted(allWeights)
    
def  NodeDegreeCorrelation(graph):
    if len(nodeNameList)==0:
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
      
 
#******************main*************************
if len(sys.argv) > 1 :
    graph_path = sys.argv[1] 

print "loading graph...graphPath=%s" % graph_path
graph = LoadGraph(graph_path)
#test2(graph)
Init(graph)

DegreeAnayltor(graph)
NodeDegreeCorrelation(graph)
EdgesAnayltor(graph)
#
#test(graph,'i.1222180848')


#node_anayltor(graph)