import threading
from s0_idle import IdleState
from s1_proximity import ProximityState
from s2_inductive import InductiveState
from s3_camera import CameraState
from s4_preprocessing import PreprocessingState
from s5_model import ModelState

class StateMachine(threading.Thread):

    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.current_state = "Idle"
        
    def run(self):
        while(1):
            if (self.current_state == "Idle"):
                self.current_state = IdleState().handle()
            elif (self.current_state == "Proximity"):
                self.current_state = ProximityState().handle()
            elif (self.current_state == "Inductive"):
                self.current_state = InductiveState().handle()
            elif (self.current_state == "Camera"):
                self.current_state = CameraState().handle()
            elif (self.current_state == "Preprocessing"):
                self.current_state = PreprocessingState().handle()
            elif (self.current_state == "Model"):
                self.current_state = ModelState().handle()
            else:
                print("Finished")
                exit(1)


    
