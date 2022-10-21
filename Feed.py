from pkgutil import get_data
import histogram as w
import cv2
from threading import Thread
from abc import ABC, abstractmethod
from Model import GunDetection

    
class Feed(ABC):
    # def __init__(self) -> None:
    #     super().__init__()

    @abstractmethod
    def initialize(self):
        pass
    
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_data(self):
        pass
    
    @abstractmethod
    def get_sensor_type(self):
        pass

    @abstractmethod
    def detect_threat(self):
        pass


class Camera(Feed):
    def __init__(self, model, cam_num, ip = -1, username = "", password = ""):
        self.cap = None
        self.cam_num = cam_num
        self.ip = ip
        #not secure 
        self.username = username
        self.password = password
        #maybe more effecient way to do this
        self.GunDetection = GunDetection()
        
    def initialize(self):
        #IP camera
        if self.ip != -1:
            cam_string = "rtsp://"+self.username+":"+self.password+"@"+self.ip+"/1"
            self.cap = cv2.VideoCapture(cam_string)
        #USB camera
        else:
            self.cap = cv2.VideoCapture(self.cam_num)
        cv2.startWindowThread()

    #this will not be in final implimentation. It is just to test the camera is working
    def show(self):
        while(True):
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            # resizing for faster detection
            frame = cv2.resize(frame, (400, 400))
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    def close(self):
        print("camera closing")
        self.cap.release()

    #Retrieves an individual frame
    def get_data(self):
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, (400, 400))
        return frame

    #Runs model to detect threat
    def detect_threat(self):
        self.GunDetection.assess(self.get_data())
        
    #Returns sensor type
    def get_sensor_type(self):
        return "camera"

