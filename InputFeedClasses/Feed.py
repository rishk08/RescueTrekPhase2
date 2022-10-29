from pkgutil import get_data
from threading import Thread
from abc import ABC, abstractmethod
# from Model import GunDetection


    
class Feed(ABC):
    # def __init__(self, models = None) -> None:
    #     super().__init__()
    #     #array of models
    #     self.models = models

    @abstractmethod
    def __init__(self, model = None):
        pass
    #Initiliaze feed object. Inlcudes any setup not involved in initial __init__
    @abstractmethod
    def initialize(self):
        """Initiliaze feed object. Inlcudes any setup not involved in initial __init__"""
        pass
    
    #Release feed object resource
    @abstractmethod
    def close(self):
        """Release feed object resource"""
        pass
    
    # Verify that the feed can be accessed
    @abstractmethod
    def verify_feed(self, source):
        """Verify that the feed can be accessed"""
        pass

    # Retrieve data from sensor
    @abstractmethod
    def get_data(self):
        """Retrieve data from sensor"""
        pass
    
    # Return string indicating sensor type
    @abstractmethod
    def get_sensor_type(self):
        """Return string indicating sensor type"""
        pass
    
    # Run individual model associated with sensor (i.e. camera can run ObjectDetection Model)
    @abstractmethod
    def run_model(self, source):
        """Run individual model associated with sensor (i.e. camera can run ObjectDetection Model)"""
        pass
    
    # Run all models
    def run_models(self):
        """Run all models associated with the feed object"""
        pass




