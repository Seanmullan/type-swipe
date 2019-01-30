class ModelState():

    def __init__(self):
        pass

    # Returns state based on transition criteria
    def handle(self):
        print("State 5")
        if (self.checkConditions()):
            return "Proximity"

    # Check condition for state transition
    def checkConditions(self):
        return True