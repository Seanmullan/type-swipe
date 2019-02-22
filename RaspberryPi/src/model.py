import threading

class Model(threading.Thread):

    def __init__(self, image):
        self.image = image

    def run(self):
        # Classify object here
        pass
