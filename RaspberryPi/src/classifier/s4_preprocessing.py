class PreprocessingState():

    def __init__(self):
        pass

    # Returns state based on transition criteria
    def handle(self):
        print("State 4")
        if (self.checkConditions()):
            return "Model"

    # Check condition for state transition
    def checkConditions(self):
        return True