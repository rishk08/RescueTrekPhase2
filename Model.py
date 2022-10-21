import cv2
from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self, filepath) -> None:
        self.filepath = filepath

    @property
    def get_file_path(self):
        return f"{self.filepath}"


class GunDetection(Model):
    def __init__(self, filepath) -> None:
        super().__init__()
        self.filepath = filepath

    
    def get_file_path(self):
        return super().get_file_path()

    def assess(self, frame):
        #run model here
        #return assessment
        pass