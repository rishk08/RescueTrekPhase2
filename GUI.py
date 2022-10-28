from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QPushButton, QVBoxLayout, QWidget
# import pyqt
import pyqtgraph
from pyqtgraph import ImageView
import cv2
from threading import Thread
from collections import deque
import InputFeedClasses.IPCamera

class GUI:
    def __init__(self,camera):
        self.app = QApplication([])
        self.window = CameraWindow(camera)
        self.window2 = CameraWindow(camera)

    def run(self):
        self.window.show()
        self.app.exit(self.app.exec())

"""Individual window for a camera feed"""
class CameraWindow(QMainWindow):
    def __init__(self,camera):
        super().__init__()

        self.deque = deque(maxlen=20)

        self.camera = camera
        
        self.central_widget = QWidget()
        
        self.button_max = QPushButton('openCV', self.central_widget)
        self.button_frame = QPushButton('Acquire Frame', self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        
        self.layout.addWidget(self.button_max)
        self.layout.addWidget(self.button_frame)

        self.setCentralWidget(self.central_widget)

        self.button_max.clicked.connect(self.button_pressed)
        self.button_frame.clicked.connect(self.update_image)
        
        self.image_view = ImageView()
        self.layout.addWidget(self.image_view)

        # self.video_frame = QtGui.QLabel()

        self.get_frame_thread = Thread(target=self.get_frame)
        self.get_frame_thread.start()

        # self.set_frame()



    def button_pressed(self):
        print('Button Pressed')
        # w.webcamCV()
        self.startCamera()
        # self.video()

    def update_image(self):
        frame = self.camera.get_frame()
        self.image_view.setImage(frame.T)

    def startCamera(self):
        self.camera.initialize()

    #thread here
    def video(self):
        #create class boolean to determine if camera needs initialized
        for _ in range (50):
            frame = self.camera.get_frame()
            self.image_view.setImage(frame.T)
    def get_frame(self):
        # self.startCamera()
        while True:
            try:
                frame = self.camera.get_frame()
                self.deque.append(frame)
                frame = self.deque[-1]
                self.image_view.setImage(frame.T)
            except:
                print("deque error probably full")
    
    def set_frame(self):
        try:
            frame = self.deque[-1]
            self.image_view.setImage(frame)
        except:
            print("exception")
    
