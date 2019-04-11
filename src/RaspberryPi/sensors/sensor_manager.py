import proximity
import inductive
import weight

class SensorManager(object):

    def __init__(self, io):
        self.proximity = proximity.Proximity()
        self.inductive = inductive.Inductive(io)
        self.weight = weight.Weight(io)

    def start_sensors(self):
        """
        Starts sensor threads
        """
        self.proximity.start()
        self.inductive.start()
        self.weight.start()