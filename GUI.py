from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QPushButton, QVBoxLayout, QWidget
# import pyqt
import pyqtgraph
from pyqtgraph import ImageView
import histogram as w
import cv2

class GUI:
    def __init__(self,camera):
        self.app = QApplication([])
        self.window = Window(camera)

    def run(self):
        self.window.show()
        self.app.exit(self.app.exec())

class Window(QMainWindow):
    def __init__(self,camera):
        super().__init__()
        self.camera = camera
        self.central_widget = QWidget()
        # self.button_min = QPushButton('Get Minimum', self.central_widget)
        self.button_max = QPushButton('openCV', self.central_widget)
        self.button_frame = QPushButton('Acquire Frame', self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        # self.layout.addWidget(self.button_min)
        self.layout.addWidget(self.button_max)
        self.layout.addWidget(self.button_frame)
        self.setCentralWidget(self.central_widget)
        self.button_max.clicked.connect(self.button_pressed)

        self.button_frame.clicked.connect(self.update_image)
        self.image_view = ImageView()
        self.layout.addWidget(self.image_view)

    def button_pressed(self):
        print('Button Pressed')
        w.webcamCV()

    def update_image(self):
        frame = self.camera.get_frame()
        self.image_view.setImage(frame.T)
    

class Camera:
    def __init__(self, cam_num):
        self.cap = None
        self.cam_num = cam_num
        
    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)
        cv2.startWindowThread()

        # open webcam video stream
        # cap = cv2.VideoCapture(0)

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
        ret, self.last_frame = self.cap.read()
        return self.last_frame






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