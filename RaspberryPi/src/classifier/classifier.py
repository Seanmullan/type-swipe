import threading
from src.classifier.classifier import Idle

class Classifier(threading.Thread):

    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.currentState = Idle()
        
    def run(self):
        while(1):
            self.currentState = self.currentState.handle()

    
