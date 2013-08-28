
import community
import csv
import os
from utils import SaveStatistics2File
import utils

dendorgram = None

CSV_COMMUNITIES_SIZE_FILE="communitiesSize.csv"
CSV_COMMUNITIES_MEMBERS_IDS="communitiesMemberIDS.csv"
CSV_COMMUNITIES_MEMBERS="communitiesMember.csv"
comSize={}
comsizeClean={}
comMem={}
comMemClean={}
comMemNames={}


def InitClusterAnalysis(graph):
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
            comsizeClean[cSize[0]] =cSize[1]
            comMemClean[cSize[0]] = comMem[cSize[0]]
    
    for memberIDs in comMemClean.iteritems():
        comMemNames[memberIDs[0]]=[]
        for member in memberIDs[1]:
            comMemNames[memberIDs[0]].append(utils.GetNodeName(member,graph))  
           
def ShowResultCluster():
    print "summary results for communities with more them one member :"
    print "number of communities : ", len(comSize)
    print "saving data in",CSV_COMMUNITIES_SIZE_FILE,"file..."
    SaveStatistics2File(CSV_COMMUNITIES_SIZE_FILE, ['community number ','member size'], comsizeClean)
    print "done"
    print "saving data ids on members in" ,  CSV_COMMUNITIES_MEMBERS_IDS ,"file..."
    SaveStatistics2File(CSV_COMMUNITIES_MEMBERS_IDS , ['community number','members ids'], comMemClean)
    print "done"    
    print "saving data on members in ",CSV_COMMUNITIES_MEMBERS,"files..."
    SaveStatistics2File(CSV_COMMUNITIES_MEMBERS,['community number','members'],comMemNames) 
     
    
   
    
def GenerateDendorgram(graph):
    global dendorgram
    dendorgram = community.generate_dendogram(graph)

def GetDendorgram():
    return dendorgram

   