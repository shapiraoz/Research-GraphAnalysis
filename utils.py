import os
import csv
import networkx as nx
import logging

nodeNameList={}
log_file ="graph_analysis.log" 



def FillNodeName(graph):
    global nodeNameList
    nodeNameList = nx.get_node_attributes(graph, 'name')
    print  "index_name have been init with " ,len(nodeNameList)
    #print nodeNameList  


    
def LOG(strMsg):
    logging.debug(strMsg)
    
def StartLog():
    #f_log = open(log_file,'wb')
    #print "starting log file..." 
    logging.basicConfig(filename=log_file,level=logging.DEBUG)
    #msg = "starting run: ",datetime.datetime.now()
    #LOG(msg)    


def Init(graph):
    FillNodeName(graph)


def GetNodeNameList():
    return nodeNameList

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
    
    
