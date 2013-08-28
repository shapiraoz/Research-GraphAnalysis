
import argparse
import graph_statistics
import cluser_analysis
from graph_statistics import LoadGraph



parser = argparse.ArgumentParser(description='graph analysis ')
parser.add_argument("-g",'--graphPath' ,type=file,help='graph file in graphml format')
parser.add_argument("-s",'--statistics',action="store_true",help='run statistics  analysis')
parser.add_argument("-c",'--cluster',action="store_true",help='run clustring analysis')

icom ={}

def tests(graph):
    for node in graph.nodes():
        deg =graph.degree(node)
        if deg > 1:
            print deg

#******************main*******************

args =parser.parse_args()
if args.graphPath.name == None:
    print "no graph file have been entered ... will exit!!"
else:
    graph = LoadGraph(args.graphPath.name)
    graph_statistics.Init(graph)
    if args.statistics :
        graph_statistics.DegreeAnayltor(graph)
        graph_statistics.EdgesAnayltor(graph)
        graph_statistics.NodeDegreeCorrelation(graph)
    if args.cluster:
        partition = cluser_analysis.InitClusterAnalysis(graph)
        cluser_analysis.ShowResultCluster()         
        #cluser_analysis.GenerateDendorgram(graph)
        #print len(cluser_analysis.dendorgram)
       
    


