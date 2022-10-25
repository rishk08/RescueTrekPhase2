from pkgutil import get_data
import histogram as w
import cv2
from threading import Thread
from abc import ABC, abstractmethod
# from Model import GunDetection
from collections import deque

    
class Feed(ABC):
    def __init__(self, models = None) -> None:
        super().__init__()
        #array of models
        self.models = models

    @abstractmethod
    def __init__(self, model = None):
        pass
    #Initiliaze feed object. Inlcudes any setup not involved in initial __init__
    @abstractmethod
    def initialize(self):
        pass
    
    #Release feed object resource
    @abstractmethod
    def close(self):
        pass
    
    # Verify that the feed can be accessed
    @abstractmethod
    def verify_feed(self, source):
        pass

    # Retrieve data from sensor
    @abstractmethod
    def get_data(self):
        pass
    
    # Return string indicating sensor type
    @abstractmethod
    def get_sensor_type(self):
        pass
    
    # Run individual model associated with sensor (i.e. camera can run GunDetection Model)
    @abstractmethod
    def run_model(self, source):
        pass
    
    # Run all models
    def run_models(self):
        pass


class IPCamera(Feed):
    def __init__(self, ip, username = "", password = "", models = None):
        super().__init__(models)
        self.cap = None
        self.frame = None
        self.ip = ip
        self.deque = deque(maxlen = 20)

        #not secure 
        self.username = username
        self.password = password

        #maybe more effecient way to do this
        self.link = ""
        
    #starts the camera stream and initialized the self.cap variable
    def initialize(self):
        try:
            cam_string = "rtsp://"+self.username+":"+self.password+"@"+self.ip+"/1"
            self.link = cam_string
            self.cap = cv2.VideoCapture(0)
        except Exception as Argument:
            print("error with camera with ip", self.ip, "\n", "Error:", Argument)
    
    # attempts to connect to camera feed. Returns True if succesful
    def verify_feed(self, source):
        ret, cap = cv2.VideoCapture(source)  
        if not cap.isOpened():
            return False
        else:
            cap.release()
        return True

    #Attempt to Re-establish connection with the feed
    def reconnect(self, source):
        cap = cv2.VideoCapture(source)  
        if not cap.isOpened():
            return False
        else:
            self.cap = cap
        return True

    #Releases camera capture
    def close(self):
        self.cap.release()

    #Retrieves an individual frame
    def get_data(self):
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, (400, 400))
        return frame
    
    # gets new frame from camera and sets it as attribute
    def update_frame(self):
        frame = get_data()
        self.frame = frame

    # Runs model to detect threat
    # Might need to be in the model class
    def run_model(self, source):
        self.model.assess(self.frame)
        # self.model.assess(get_data())

    #primative solution to run all models
    def run_models(self):
        for model in self.models:
            self.run_model(model)
        
    #Returns sensor type
    def get_sensor_type(self):
        return "camera"

