class CameraState():

    def __init__(self):
        pass

    # Returns state based on transition criteria
    def handle(self):
        print("State 3")
        if (self.checkConditions()):
            return "Preprocessing"

    # Check condition for state transition
    def checkConditions(self):
        return True