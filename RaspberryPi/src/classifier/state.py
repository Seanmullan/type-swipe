from abc import ABC, abstractmethod
from src.classifier.classifier import Classifier

class State(ABC):

    @abstractmethod
    def handle():
        pass

    @abstractmethod
    def goNext():
        pass

