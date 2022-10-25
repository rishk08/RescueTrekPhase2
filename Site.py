import Feed
import cv2

#example to test Camera class functionality. Not Final
class Site:
    def __init__(self) -> None:
        self.camera = Feed.IPCamera("10.165.3.64", "admin", "admin")
    
    def start(self):
        self.camera.initialize()
    
    def show(self):
        while True:
            frame = self.camera.get_data()
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    def close(self):
        self.camera.close()
