
import base_c
import trainer_c

class plotter:
    
    def __init__(self,classfier = None):
        self.m_self = classfier
    
    def show(self,cls = None):
        if cls == None:
            if self.m_self == None : 
                return
            else:
                s_cls = self.m_self 
        else:
            s_cls = cls
            
        
        test_score = np.zeros((params['n_estimators'],), dtype=np.float64)
 
        for i, y_pred in enumerate(clf.staged_decision_function(x_test)):
            test_score[i] = s_cls.loss_(y_test, y_pred)
             
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 1, 1)
        plt.title('Deviance')
        plt.plot(np.arange(params['n_estimators']) + 1, clf.train_score_, 'b-',label='Training Set Deviance')
        plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-',label='Test Set Deviance')
        plt.legend(loc='upper right')
        plt.xlabel('Boosting Iterations')
        plt.ylabel('Deviance') 
        feature_importance = clf.feature_importances_
# make importances relative to max importance
        feature_importance = 100.0 * (feature_importance / feature_importance.max())
        sorted_idx = np.argsort(feature_importance)
        pos = np.arange(sorted_idx.shape[0]) + .5
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 1, 1)
        plt.barh(pos, feature_importance[sorted_idx], align='center')
        plt.yticks(pos, X.columns[sorted_idx])
        plt.xlabel('Relative Importance')   
        plt.title('Variable Importance')
        plt.show()

