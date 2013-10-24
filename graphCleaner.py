'''
@author: oz
'''

class graph_cleaner_c:
    
    def __init__(self,graph,minWeight):
        self.m_orjGraph = graph
        self.m_cleanGraph = graph.copy()
        self.m_minWeight=minWeight # set to default value of minWeight
        self.m_isClean=0

    def SetMinWeight(self,minWeight):
        self.m_minWeight=minWeight
                   
    def GetCleanGraph(self):
        if self.m_isClean==1:
            return self.m_cleanGraph
        else:
            return None
                   
    def GetOriginalGraph(self):
        return self.m_orjGraph
                   
    def CleanGraph(self):
        
        edges= self.m_cleanGraph.edges();
        for edge in edges:
            weight=self.m_cleanGraph[edge[0]][edge[1]]['weight']
            if weight < self.m_minWeight:
                self.m_cleanGraph.remove_edge(edge[0],edge[1])
        nodes =self.m_cleanGraph.nodes();
        for node in nodes:
            if  len(self.m_cleanGraph.neighbors(node))==0:
                self.m_cleanGraph.remove_node(node)
        
        self.m_isClean=1
        return self.m_cleanGraph
             
        

    

