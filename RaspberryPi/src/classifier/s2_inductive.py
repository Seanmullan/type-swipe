class InductiveState():

    def __init__(self):
        pass

    # Returns state based on transition criteria
    def handle(self):
        print("State 2")
        if (self.checkConditions()):
            return "Camera"

    # Check condition for state transition
    def checkConditions(self):
        return True