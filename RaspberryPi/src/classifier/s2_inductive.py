from src.classifier import State
from src.classifier import CameraState

class InductiveState(State):

    def __init__(self):
        pass

    # Returns state based on transition criteria
    def handle(self):
        if (self.checkConditions()):
            return CameraState()

    # Check condition for state transition
    def checkConditions(self):
        return True