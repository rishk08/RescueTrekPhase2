from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QPushButton, QVBoxLayout, QWidget, QGridLayout,QLayoutItem, QLabel, QSizePolicy
from PyQt6.QtCore import QTimer, Qt
# from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
# import pyqt
import pyqtgraph
from pyqtgraph import ImageView, RawImageWidget, ImageItem
import cv2
from threading import Thread
from collections import deque
import InputFeedClasses.IPCamera
import queue
import threading
import time

pyqtgraph.setConfigOptions(imageAxisOrder = 'row-major')

class GUI():
    def __init__(self,cameras) -> None:
        #start system here
        self.app = QApplication([])
        self.window = MainWindow(cameras)
        self.window.show()
        self.app.exit(self.app.exec())

    def run(self):
        # self.window.run()
        pass
        
        


class MainWindow(QMainWindow):
    def __init__(self,cameras):
        super().__init__()
        self.setStyleSheet(open('css/stylesheet.css').read())
        self.cameras = []
        self.cameraWindows = []
        self.central_widget = QLabel("Null Threat")
        self.main_layout = QGridLayout()
        self.setWindowTitle("Null Threat")
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
        self.showMaximized()
        self.button_start = QPushButton('start')
        self.button_start.setStyleSheet(open('css/buttons.css').read())
        self.main_layout.addWidget(self.button_start,1,0,2,1)
        self.button_start.clicked.connect(self.run)
        self.priority_view = RawImageWidget(scaled=True)
        self.priority_label = QLabel()
        self.priority_num = 0
        # self.main_layout.setRowMinimumHeight( 0, 3)
        self.button_start.setFixedHeight(100)
        self.button_start.setFixedWidth(300)

        self.label = QLabel("Null Threat", self.central_widget)
        # self.main_layout.addWidget(self.label,0,0)
        self.central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap('null_threat_grey.png')
        self.central_widget.setPixmap(pixmap)
        self.central_widget.setScaledContents(True)
        
        self.main_layout.addWidget(self.priority_view, 0, 0, 3, 1)
        self.main_layout.addWidget(self.priority_label, 0, 0, 3, 1)
        self.priority_view.hide()
        self.priority_label.hide()

        self.start = 0
        self.current = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_priority)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)


        #make system provide cameras, put this in a function and remove parameter
        for camera in cameras:
            self.cameras.append(camera)
        
        
    #modify this to check from list of priorities
    def update_priority(self):
        if self.priority_num < (len(self.cameraWindows) - 1):
            self.priority_num = self.priority_num + 1
        else:
            self.priority_num = 0
        self.priority_view.setImage(self.cameraWindows[self.priority_num].frame) #= self.cameraWindows[0].return_frame()
        # self.priority_view.setImage(cv2.resize(self.cameraWindows[self.priority_num].frame, (400, 400)))
        # self.cameraWindows[self.priority_num].resize(400,400)
        print("attempted to update priority")

    def update_time(self):
        self.current = time.time()

        
    def startup():
        """call system startup and get the number of feeds so the GUI can organize itself"""
        pass
    def run(self):
        self.button_start.hide()
        self.priority_view.show()
        # self.priority_label.show()
        # Replace self.cameras with location of cameras from system produced by startup()
        i = 0
        for camera in self.cameras:
            cam = CameraWindow(camera)
            self.main_layout.addWidget(cam.return_frame(),i,1,1,1)
            self.cameraWindows.append(cam)
            i += 1
        for camera in self.cameraWindows:
            camera.startCamera()
        

"""Individual window for a camera feed"""
class CameraWindow(QWidget):
    def __init__(self,camera):
        super().__init__()
        self.setStyleSheet(open('css/cameraWindow.css').read())
        self.deque = deque(maxlen=100)

        self.camera = camera
        self.layout = QVBoxLayout()

        self.image_view = RawImageWidget(scaled=True)
        self.frame = None
        self.frame_updated = False
        
        self.layout.addWidget(self.image_view)

        self.start = 0
        self.current = 0
        # self.video_frame = QtGui.QLabel()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image_no_deque)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(.05)

        #thread to pull in images in a loop
        self.get_frame_thread = Thread(target=self.get_frame)
        self.get_frame_thread.daemon = True
        self.get_frame_thread.start()
        # self.update_image()
        


    def update_time(self):
        self.current = time.time()
    def update_image_fps(self):
        # frame = self.camera.get_data()
        if self.deque:
            try:
                # frame = self.deque[-1]
                frame = self.deque.pop()
                fps = 1 / (self.current - self.start)
                self.start = time.time()
                print(type(frame))
                print(str(int(fps)) + " cam " + str(self.camera.ip))
                cv2.putText(frame, "FPS: " + str(int(fps)) + " cam " + str(self.camera.ip), (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                self.image_view.setImage(frame)
                self.frame = frame
            except:
                print("maybe empty")
        else:
            # print("deque empty?")
            pass
    
    def update_image_no_deque(self):
        # self.startCamera()
        if self.frame_updated:
            try:
                frame = self.frame
                fps = 1 / (self.current - self.start)
                self.start = time.time()
                print(type(frame))
                print(str(int(fps)) + " cam " + str(self.camera.ip))
                cv2.putText(frame, "FPS: " + str(int(fps)) + " cam " + str(self.camera.ip), (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                self.image_view.setImage(frame)
                
                self.frame_updated = False
                print("update_image_no_deque worked")
            except Exception as err:
                print(err)
                print("error in no deque")
    

    def startCamera(self):
        self.camera.initialize()
    
    def get_frame(self):
        # self.startCamera()
        while True:
            try:
                frame = self.camera.get_data()
                # self.deque.append(frame)
                self.frame = frame
                self.frame_updated = True
                # self.deque.append(frame)
                # frame = self.deque[-1]
                # self.image_view.setImage(frame.T)
                print("get_frame worked")
            except Exception as err:
                print(err)
                print("deque error probably full")
    
    def get_frame_detector(self):
        pass

    def return_frame(self):
        return self.image_view

    def return_cv2_frame(self):
        return self.frame
    


    # get_frame(self)
    #   bool, frame = cv2.VideoCapture()
    #   self.frame = frame
    #   self.frame_updated = True

    # update_image_no_deque(self)
    #   frame = self.frame
    #   self.image_view.setImage(frame)
    #   self.frame_updated = False

    # frame = detector.predict(frame)
    # RawImageWidget(frame)