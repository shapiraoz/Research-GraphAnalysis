
import utils


class base_c:
    
    def __init__(self):
        if not utils.startedLog:
            utils.StartLog()
    
    def LogPrint(self,strMsg):
        utils.LOG(strMsg)
        print strMsg
        