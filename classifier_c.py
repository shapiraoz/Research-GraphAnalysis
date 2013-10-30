
import networkx
import community

class classifier_type_e:
    e_bestPractice =0
    e_networkx=1
    


class classifier_c:
    
    def __init__(self,graph, classify_type=None):
        self.m_graph = graph
        self.m_classifier_type = classify_type
    
    
    def classifey(self):
        if self.m_classifier_type!=None:
            return self.run_classifier(self,self.m_classifier_type)
        return None
    
    def run_classifier(self,classfier_type):
        dic =[]
        if classfier_type == classifier_type_e.e_bestPractice:
            dic = community.best_partition(self.m_graph)
        elif classfier_type == classifier_type_e.e_networkx:
            dic = networkx.clustering(self.m_graph)
        return dic
        
    
    