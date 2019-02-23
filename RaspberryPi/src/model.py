import threading

class Model(threading.Thread):

    def __init__(self, image):
        threading.Thread.__init__(self)
        self.image = image

    def run(self):
        # Classify object here
        pass
