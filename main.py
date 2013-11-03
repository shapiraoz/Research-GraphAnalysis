
import argparse
import graph_statistics
#import cluser_analysis
import cluster_analysis_c
import sys
from graph_statistics import LoadGraph
import graphCleaner
import utils
import classifier_c

def init():
    utils.EnsureDir(utils.RESULT_DIR);



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
       
    graph_statistics.Init(workGraph) 
    if args.statistics :
        graph_statistics.DegreeAnayltor(workGraph)
        graph_statistics.EdgesAnayltor(workGraph)
        graph_statistics.NodeDegreeCorrelation(workGraph)
    if args.cluster:
        copyGraph=workGraph.copy()
        classifier_best = classifier_c.classifier_c(workGraph,"best_practice",classifier_c.classifier_type_e.e_bestPractice)
       
        cluster_best_analysis = cluster_analysis_c.cluster_analysis_c(workGraph,classifier_best)
        cluster_best_analysis.RunClusterStatistics()
        cluster_best_analysis.ShowResultCluster()
        
        classifier_networkX = classifier_c.classifier_c(copyGraph,"networkx",classifier_c.classifier_type_e.e_networkx)
        cluster_best_analysisNetworkx = cluster_analysis_c.cluster_analysis_c(copyGraph,classifier_networkX)
        cluster_best_analysisNetworkx.RunClusterStatistics()
        cluster_best_analysisNetworkx.ShowResultCluster()
            
        
    
        #partition = cluser_analysis.InitClusterAnalysis(graph)
        #cluser_analysis.ShowResultCluster()         
        #cluser_analysis.RunClusterStatistics(graph)
        #cluser_analysis.RunBestPartitionIndex(graph)
        #cluser_analysis.GenerateDendorgram(graph)
        #print len(cluser_analysis.dendorgram)
       
    


