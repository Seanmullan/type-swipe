"""
The State Machine calls the handle() method in each of the respective states,
and transitions to the appropriate state
"""

import threading
from s0_idle import IdleState
from s1_proximity import ProximityState
from s2_inductive import InductiveState
from s3_preprocessing import PreprocessingState
from s4_model import ModelState

class StateMachine(threading.Thread):
    """
    This thread runs in an infinite loop to transition to the appropriate states based
    on the response from each states handle() method
    """

    def __init__(self, thread_id):
        print 'Starting Classifier state machine...'
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.current_state = "Idle"

        self.idle = IdleState()
        self.proximity = ProximityState()
        self.inductive = InductiveState()
        self.preprocessing = PreprocessingState()
        self.model = ModelState()

    def run(self):
        """
        Transitions to the appropriate state based on the response from each states
        handle() method
        """
        while True:
            if self.current_state == "Idle":
                self.current_state = self.idle.handle()
            elif self.current_state == "Proximity":
                self.current_state = self.proximity.handle()
            elif self.current_state == "Inductive":
                self.current_state = self.inductive.handle()
            elif self.current_state == "Preprocessing":
                self.current_state = self.preprocessing.handle()
            elif self.current_state == "Model":
                self.current_state = self.model.handle()
            else:
                print 'Exiting Classifier state machine'
                exit(1)
