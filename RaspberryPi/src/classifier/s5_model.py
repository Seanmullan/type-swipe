from src.classifier import State
from src.classifier import ProximityState

class ModelState(State):

    def __init__(self):
        pass

    # Returns state based on transition criteria
    def handle(self):
        if (self.checkConditions()):
            return ProximityState()

    # Check condition for state transition
    def checkConditions(self):
        return True