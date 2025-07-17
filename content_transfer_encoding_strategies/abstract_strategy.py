from abc import ABC, abstractmethod

class AbstractStrategy(ABC):
    
    @abstractmethod
    def process(self, content_type, payload):
        pass