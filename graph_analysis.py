'''
'''


import networkx as nx
import sys
import os
import csv

#if __name__ == '__main__':
    

weightDist = {}
degreeDist = {}
subject2Degree={}

args_size=0  
graph_path = ""


    
def load_graph(path):
    if not os.path.exists(path):
        print "file %s not exist will exit!!!" % path
        return
    graph = nx.read_graphml(path)
    print "graph is loaded form path %s" % path 
    return graph



def SaveStatistics2File(filePath ,header, dictionary):
    if os.path.exists(filePath):
        os.remove(filePath)
    csvFile = open(filePath,"wb")
    writer = csv.writer(csvFile,delimiter=",",quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header)
    for k,v in dictionary.items():
        writer.writerow([k,v])
    csvFile.close()
  
        

def degree_anayltor(graph):
    maxDegree=0
    nodeIndex =None
    degreeDistCsvFilePath ="degreesDistribution.csv"
    degreesFile = "degrees.csv"
    print "analyze degree..."
    for node in nx.get_node_attributes(graph, 'name').iteritems():
        deg = graph.degree(node[0])
        name = node[1]
        if name != None:
            subject2Degree[name]=deg
            if deg > maxDegree:
                maxDegree = deg
                nodeIndex = node[0]
            if deg in degreeDist :
                degreeDist[deg] = degreeDist[deg] + 1
            else:
                degreeDist[deg] = 1 
        #if deg !=0 :
        #    print "node",node,"have degree" , deg
    print "saving degree distribution in ", degreeDistCsvFilePath ," file "
    SaveStatistics2File(degreeDistCsvFilePath,['degree','num'] , degreeDist)
    print "saving subject degree cvs ...."
    SaveStatistics2File(degreesFile, ['subject','degree'], subject2Degree)
    print "the node with the largest degree is ", getNodeName(nodeIndex,graph) , "with degree of " , maxDegree
   
   
   
def getNodeName(index,graph):
    if index != None:
        return nx.get_node_attributes(graph, 'name').get(index) 
    #   for node in graph.nodes_iter(data = True):
    #       if str(node[0]) == index and 'name' in node[1]:
    #           return node[1]['name']
    return None
    
            
   
def test(grpah,index):
    for n in  nx.get_node_attributes(grpah, 'name').iteritems():
        print  "n[0]=",n[0] , "n[1]=",n[1]
        

def edges_anayltor(graph):
    maxWeight = 0
    sumEdge =0
    maxIndex =None
    count =0.0
    print "analyzing edges..." 
    allWeights =  nx.get_edge_attributes(graph,"weight").items()
    countWeight = len (allWeights)
    old_num =0
    for weight in  allWeights:
        if weight[1] in weightDist :
            weightDist[weight[1]]  = weightDist[weight[1]]+1 
        else:
            weightDist[weight[1]] = 1   
        sumEdge = sumEdge + weight[1]
        if weight[1] >  maxWeight and weight[0][0] != weight[0][1] and getNodeName(weight[0][0],graph)!= None and getNodeName(weight[0][1],graph) != None:
            maxWeight = weight[1]
            maxIndex = weight[0] 
        count=count+1
        
        num_num= round((count/countWeight)*100)
        if num_num!=old_num:
            old_num=num_num
            if num_num %10 == 0:
                sys.stdout.write("==")
            
           
    avgWeight = sumEdge/countWeight
    print "   done!!"
    print  "the avg of the weight is" ,avgWeight  #, " the sumEdge is " , sumEdge
    #print "the srongest link is", maxWeight , " between ",nx.get_node_attributes(graph, "name")[weight[0][0]] ," to " ,nx.get_node_attributes(graph, "name")[weight[0][1]]    #need to fix this!!!     
    print "the srongest link is", maxWeight , " between ",getNodeName(maxIndex[0],graph) ," to " ,getNodeName(maxIndex[1],graph) 
    allWeights.sort()
    SaveStatistics2File("edges.csv",['edge weight','nums'],weightDist)
    #print allWeights
    #print "countWieght = %d" % countWeight
    print "the mid is : %d " % allWeights[(countWeight/2)][1]  
    #sorted(allWeights)
    
    
      
 
#******************main*************************
if len(sys.argv) > 1 :
    graph_path = sys.argv[1] 
    
print "loading graph... graphPath=%s" % graph_path

graph = load_graph(graph_path)
#test(graph,'i.1222180848')
degree_anayltor(graph)
edges_anayltor(graph)
#node_anayltor(graph)