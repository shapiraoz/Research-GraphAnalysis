import os
import csv
import networkx as nx
import logging



nodeNameList={}
RESULT_DIR ="results"
log_file ="%s/graph_analysis.log"% RESULT_DIR 
startedLog=False
IsNodeNameListInit=False


########################################################################
# String util functions
def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def clean_string(str):
    str_clean = str.lower()
    str_clean = str_clean.strip()
    str_clean = safe_unicode(str_clean)
    return str_clean
########################################################################



def EnsureDir(d):
    if not os.path.exists(d):
        os.mkdir(d)

def FillNodeName(graph):
    global nodeNameList
    global IsNodeNameListInit
    nodeNameList = nx.get_node_attributes(graph, 'name')
    print  "index_name have been init with " ,len(nodeNameList)
    IsNodeNameListInit =True
    #print nodeNameList  


    
def LOG(strMsg):
    EnsureDir(RESULT_DIR)
    if not os.path.exists(log_file):
        StartLog() 
    logging.debug(strMsg)
    
def StartLog():
    global startedLog
    print "starting log file..."
    logging.basicConfig(filename=log_file,level=logging.DEBUG)
    startedLog=True


def Init(graph):
    FillNodeName(graph)


def GetNodeNameList():
    return nodeNameList

def GetNodeName(index,graph):
    global IsNodeNameListInit
    if not IsNodeNameListInit:
        FillNodeName(graph)
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
    
    
