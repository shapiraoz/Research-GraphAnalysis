########################################################################
# imports
import csv
import networkx as nx
import random
import cPickle as pickle
import collections
import utils
import argparse

########################################################################
users_count = 0
unique_interests_count = 0
users_degrees_distribution = {}

# index strings and generate unique node id, returns node id
nodes_index = {}
nodes_index_inverse = {}

def gen_node(name, node_type, graph):
	global unique_interests_count
	node_id = 0
	clean_str = utils.clean_string(name)
	if clean_str in nodes_index:
		#string is already indexed, return node_id
		node_id = nodes_index[clean_str]
	else:
		#string not indexed, generate unique id and add to graph
		unique_id_found = False
		give_up_counter = 0
		while (not(unique_id_found)):
			rnd = random.getrandbits(32)
			node_id = node_type[0] + '.' + str(rnd)
			if (not node_id in nodes_index_inverse):
				unique_interests_count += 1
				#available unique id found, create node
				unique_id_found = True
				nodes_index[clean_str] = node_id
				nodes_index_inverse[node_id] = clean_str

				graph.add_node(node_id, name=clean_str)
			else:
				give_up_counter += 1 
				if give_up_counter > 100:
					print "Err"
	return node_id


############################################################################3
#main
parser = argparse.ArgumentParser(description='parse to graph ')
parser.add_argument("-d",'--dataFilePath' ,type=file,help='csv data file for creating graph in graphal format')

args =parser.parse_args()

dataFilePath=args.dataFilePath.name if args.dataFilePath.name!=None else 'data.csv'

########################################################################
# Create graph
pinterest_graph = nx.Graph()
users_interests = {}
########################################################################
# open CSV file
ifile  = open(dataFilePath, "rb")
reader = csv.reader(ifile)
print "start parsing file %s" % dataFilePath
########################################################################
#parse CSV and generate graph
rownum = 0
for row in reader:
	column = 0
	user_node_id = 0
	for col in row:
		if (column == 0):
			users_count += 1
			users_interests = []
			'''
			user_node_id = gen_node(col, 'user', pinterest_graph)
			if (rownum >= 33000):
				print col			
			'''
		else:
			interest_node_id = gen_node(col, 'interest', pinterest_graph)
			users_interests.append(interest_node_id)
		#print 'node_id:%s, node_str:%s' % (node_id, node_str)
		column += 1
	
	if (not column in users_degrees_distribution):
		users_degrees_distribution[column] = 1
	else:
		users_degrees_distribution[column] += 1

	for i in range(len(users_interests)):
		for j in range(i, len(users_interests)):
			src_node_id = users_interests[i]
			trgt_node_id = users_interests[j]
			if pinterest_graph.has_edge(src_node_id, trgt_node_id):
				#edge exists, update weight
				pinterest_graph[src_node_id][trgt_node_id]['weight'] += 1
			else:
				#edge doesn't exist, add it and set initial weight to =1
				pinterest_graph.add_edge(src_node_id, trgt_node_id, {'weight': 1})

	if (rownum % 1000 == 0):
		print rownum
	rownum += 1
ifile.close()
########################################################################
print "finished reading at ", str(rownum)
stats = {}
# save graph to file
#nx.write_graphml(pinterest_graph, 'pinterest.graphml')
########################################################################
# calc edge weight distribution
interests_degrees_vector = pinterest_graph.degree()

interests_degree_distribution = collections.Counter(interests_degrees_vector)
print "interests_degree_distribution= ", interests_degree_distribution
stats['interests_degree_distribution'] = interests_degree_distribution
########################################################################
# print stats
print "users_count= ", users_count
print "unique_interests_count= ", unique_interests_count
print "users_degrees_distribution= ", users_degrees_distribution

stats['users_count'] = users_count
stats['unique_interests_count'] = unique_interests_count
stats['users_degrees_distribution'] = users_degrees_distribution
stats['nodes_before_clean'] = len(pinterest_graph.nodes())
stats['edges_before_clean'] = len(pinterest_graph.edges())

print "nodes_before_clean= ", stats['nodes_before_clean']
print "edges_before_clean= ", stats['edges_before_clean']
########################################################################
# clean graph
for edge in pinterest_graph.edges(data=True):
	edge_weight = edge[2]['weight']
	if (edge_weight==1):
		pinterest_graph.remove_edge(edge[0], edge[1])

nodes_to_remove = [n for n in interests_degrees_vector if (interests_degrees_vector[n] == 0)]
pinterest_graph.remove_nodes_from(nodes_to_remove)

nx.write_graphml(pinterest_graph, 'pinterest_clean.graphml')
########################################################################
stats['nodes_after_clean'] = len(pinterest_graph.nodes())
stats['edges_after_clean'] = len(pinterest_graph.edges())
print "nodes_after_clean= ", stats['nodes_after_clean']
print "edges_after_clean= ", stats['edges_after_clean']

# save dictionaries
f = open('nodes_index.pickle', 'w')
pickle.dump(nodes_index, f)
f.close()

f = open('nodes_index_inverse.pickle', 'w')
pickle.dump(nodes_index_inverse, f)
f.close()

f = open('pinterest_graph.pickle', 'w')
pickle.dump(pinterest_graph, f)
f.close()

f = open('stats.pickle', 'w')
pickle.dump(stats, f)
f.close()