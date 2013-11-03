
import networkx
import community

class classifier_type_e:
    e_bestPractice=0
    e_networkx=1
    


class classifier_c:
    
    def __init__(self,graph,name, classify_type=None):
        self.m_graph = graph
        self.m_classifier_type = classify_type
        self.name =name 
    
    
    def classifey(self):
        if self.m_classifier_type!=None:
            return self.run_classifier(self.m_classifier_type)
        return None
    
    def GetName(self):
        return self.name
    
    def GeyType(self):
        return self.m_classifier_type
    
    def run_classifier(self,classfier_type):
       
        if classfier_type == classifier_type_e.e_bestPractice:
            return community.best_partition(self.m_graph)
        elif classfier_type == classifier_type_e.e_networkx:
            return networkx.clustering(self.m_graph)
     
        
    
    