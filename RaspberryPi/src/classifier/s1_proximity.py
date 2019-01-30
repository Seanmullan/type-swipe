class ProximityState():

    def __init__(self):
        pass

    # Returns state based on transition criteria
    def handle(self):
        print("State 1")
        if (self.checkConditions()):
            return "Inductive"

    # Check condition for state transition
    def checkConditions(self):
        return True