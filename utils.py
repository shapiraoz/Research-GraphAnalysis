import os
import csv
import networkx as nx
import logging
import pickle
import mmap
import hashlib



nodeNameList={}
DEF_RESULT_DIR ="results"
log_file ="%s/graph_analysis.log"% DEF_RESULT_DIR 
startedLog=False
IsNodeNameListInit=False
DEF_USER_DB_FILE="data_50K.csv"
DEF_STRING_HASH="string_hash.pkl"

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

def PathExist(path):
    return os.path.exists(path)

def FillNodeName(graph):
    global nodeNameList
    global IsNodeNameListInit
    nodeNameList = nx.get_node_attributes(graph, 'name')
    print  "index_name have been init with " ,len(nodeNameList)
    IsNodeNameListInit =True
    #print nodeNameList  


    
def LOG(strMsg):
    EnsureDir(DEF_RESULT_DIR)
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


def LoadFileString2Mem(filePath):
    if os.path.exists(filePath):
        size = os.stat(filePath).st_size
        f = open(filePath)
        data = mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ) 
        return data
    return None

def DumpObjToFile(obj,filePath):
    if os.path.exists(filePath):
        os.remove(filePath)
    handel = open(filePath,'wb')
    pickle.dump(obj, handel)
    handel.close()
     
def LoadObjFromFile(filePath):
    if not os.path.exists(filePath):
        print "file %s is not exist can't load file..." % filePath
        return None
    handle = open(filePath,'rb')
    return pickle.load(handle)

def GetNodeNameList():
    return nodeNameList

def GetNodeName(index,graph=None):
    global IsNodeNameListInit
    if not IsNodeNameListInit and graph !=None:
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
    
def translateNodeList2SubList(nodeList):
    global IsNodeNameListInit
    if not IsNodeNameListInit:
        return None
    SubList =[]
    for nodeId in nodeList:
        subName=GetNodeName(nodeId)
        if subName != None and not subName in SubList:
            SubList.append(subName)
    return SubList
    
    
def SaveStatistics2File_DicVal(filePath ,header, dictionary):# repcate manuly...
    if os.path.exists(filePath):
        os.remove(filePath)
    csvFile = open(filePath,"wb")
    writer = csv.writer(csvFile,delimiter=",",quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header)
    
    for k,v in dictionary.items():
        list=[]
        list.append(k)
        for item in v:
            if isinstance(item ,basestring):
                list.append(item.lstrip('\n\r\"').replace('"',''))
            else:
                list.append(item)
    #print "new line\n%s"% list
        writer.writerow(list)
    csvFile.close()
    
    
def EncodeString(str):
    return int (hashlib.md5(str).hexdigest(),16)
    
    