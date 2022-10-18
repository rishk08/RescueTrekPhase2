from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QPushButton, QVBoxLayout, QWidget
# import pyqt
import pyqtgraph
from pyqtgraph import ImageView
import histogram as w
import cv2
from threading import Thread
from collections import deque

class GUI:
    def __init__(self,camera):
        self.app = QApplication([])
        self.window = CameraWindow(camera)
        self.window2 = CameraWindow(camera)

    def run(self):
        self.window.show()
        self.app.exit(self.app.exec())

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
    

class Camera:
    def __init__(self, cam_num):
        self.cap = None
        self.cam_num = cam_num
        
    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)
        cv2.startWindowThread()

        # open webcam video stream
        self.cap = cv2.VideoCapture(0)

    #this will need a thread as is
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
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, (400, 400))
        return frame








#formerly in window class
        # def activateHist():
    #     w.webcamCV()

    # def run(self):
    #     # app = QApplication([])
    #     # win = QMainWindow()
    #     # central_widget = QWidget()
    #     # button = QPushButton('Test', central_widget)
    #     # button.clicked.connect(GUI.button_pressed)
    #     # layout = QVBoxLayout(central_widget)
    #     # layout.addWidget(button)
    #     # win.setCentralWidget(button)
    #     # win.show()
    #     # app.exit(app.exec())
        
    #     # window = self.GUI()
    #     # window.show()
    #     self.show()
        
    # def close(self):
    #     self.app.exit(self.app.exec_())