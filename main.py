
import argparse
import graph_statistics
#import cluser_analysis
import cluster_analysis_c
import sys
from graph_statistics import LoadGraph
import graphCleaner
import utils
import classifier_c
import users_DB_graph_c
import networkx as nx
import os

def init():
    utils.EnsureDir(utils.RESULT_DIR)
    if os.path.exists(utils.log_file): 
        os.remove(utils.log_file)
        utils.StartLog()



parser = argparse.ArgumentParser(description='graph analysis ')
parser.add_argument("-g",'--graphPath' ,type=file,help='graph file in graphml format')
parser.add_argument("-s",'--statistics',action="store_true",help='run statistics  analysis')
parser.add_argument("-c",'--cluster',action="store_true",help='run clustring analysis')
parser.add_argument("-w",'--weight',type=int,default=1,help="set minimum weight for cleaning the graph")
icom ={}

def tests(graph):
    for node in graph.nodes():
        deg =graph.degree(node)
        if deg > 1:
            print deg


#******************main*******************

args =parser.parse_args()
if not len(sys.argv) > 1:
    print "no arguments has insert"
    parser.print_help(None)
    sys.exit(1)
    
if args.graphPath.name == None:
    print "no graph file have been entered ... will exit!!"
else:
    init()
    print "load graph (can take a while)..."
    graph = LoadGraph(args.graphPath.name)
    graph.name= "m"
   
    print "cleaning the graph...."
    #gc = graphCleaner.graph_cleaner_c(graph)
    #cleanGraph=gc.CleanGraph()#need to check!!!
    workGraph = graph
    if args.weight>1:
        print "going to clean graph... minimun weight is set to %d"% args.weight
        gc = graphCleaner.graph_cleaner_c(graph,args.weight)
        workGraph = gc.CleanGraph()
        nodes_len=len(workGraph.nodes())
        edges_len=len(workGraph.edges())   
        utils.LOG("clean graph(min weight %d) is with :\n %d nodes\n %d edges "%(args.weight,nodes_len,edges_len))
    
    graph_statistics.Init(workGraph)
    print "checking for data on users ..."
    users_db= users_DB_graph_c.user_DB_graph_c(workGraph,"data_50K.csv") 
     
    print "number of users in data file is %d"%users_db.GetNumOfDBUsers()
    num_of_users_in_graph =users_db.GetNumUsersGraph()
    msg = "number of user in that graph %d"%num_of_users_in_graph
    print msg
    utils.LOG(msg)
    if args.statistics :
        graph_statistics.DegreeAnayltor(workGraph)
        graph_statistics.EdgesAnayltor(workGraph)
        graph_statistics.NodeDegreeCorrelation(workGraph)
    if args.cluster:
        copyGraph=workGraph.copy()
        classifier_best = classifier_c.classifier_c(workGraph,"best_practice",classifier_c.classifier_type_e.e_bestPractice)
       
        cluster_best_analysis = cluster_analysis_c.cluster_analysis_c(workGraph,classifier_best,users_db)
        cluster_best_analysis.RunClusterStatistics()
        cluster_best_analysis.ShowResultCluster()
        
        #classifier_networkX = classifier_c.classifier_c(copyGraph,"networkx",classifier_c.classifier_type_e.e_networkx)
        #cluster_best_analysisNetworkx = cluster_analysis_c.cluster_analysis_c(copyGraph,classifier_networkX)
        #cluster_best_analysisNetworkx.RunClusterStatistics()
        #cluster_best_analysisNetworkx.ShowResultCluster()
            
        
    
        #partition = cluser_analysis.InitClusterAnalysis(graph)
        #cluser_analysis.ShowResultCluster()         
        #cluser_analysis.RunClusterStatistics(graph)
        #cluser_analysis.RunBestPartitionIndex(graph)
        #cluser_analysis.GenerateDendorgram(graph)
        #print len(cluser_analysis.dendorgram)
       
    


