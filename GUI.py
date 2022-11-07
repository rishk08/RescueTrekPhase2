from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QPushButton, QVBoxLayout, QWidget, QGridLayout
from PyQt6.QtCore import QTimer
# from PyQt6.QtGui import QGridLayout
# import pyqt
import pyqtgraph
from pyqtgraph import ImageView
import cv2
from threading import Thread
from collections import deque
import InputFeedClasses.IPCamera
import queue
import threading
import time


class GUI:
    def __init__(self,cameras):
        self.app = QApplication([])
        self.cameras = []
        grid = QGridLayout()
        for camera in cameras:
            cam = CameraWindow(camera)
            grid.addWidget(cam)
            self.cameras.append(cam)
        

    def run(self):
        for camera in self.cameras:
            camera.show()
            camera.startCamera()
        self.app.exit(self.app.exec())

"""Individual window for a camera feed"""
class CameraWindow(QMainWindow):
    def __init__(self,camera):
        super().__init__()

        self.deque = deque(maxlen=100)

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
        self.start = 0
        self.current = 0
        # self.video_frame = QtGui.QLabel()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image_fps)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(.05)

        self.get_frame_thread = Thread(target=self.get_frame)
        self.get_frame_thread.daemon = True
        self.get_frame_thread.start()

        # self.set_frame()



    def button_pressed(self):
        print('Button Pressed')
        # self.startCamera()
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
                self.image_view.setImage(frame.T)
            except:
                print("maybe empty")
        else:
            # print("deque empty?")
            pass
    # cv2.putText(outputImage, "FPS: " + str(int(fps)), (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    def update_image(self):
        # frame = self.camera.get_data()
        if self.deque:
            frame = self.deque[-1]
            print(type(frame))
            self.image_view.setImage(frame.T)
        else:
            print("deque empty?")

    def start_threads(self):
        get_frame_thread = Thread(target=self.get_frame)
        get_frame_thread.daemon = True
        get_frame_thread.start()

    def startCamera(self):
        self.camera.initialize()

    #thread here
    def video(self):
        #create class boolean to determine if camera needs initialized
        for _ in range (50):
            frame = self.camera.get_data()
            self.image_view.setImage(frame.T)
    def get_frame(self):
        # self.startCamera()
        while True:
            try:
                frame = self.camera.get_data()
                self.deque.append(frame)
                # self.deque.append(frame)
                # frame = self.deque[-1]
                # self.image_view.setImage(frame.T)
                print("get_frame worked")
            except:
                print("deque error probably full")
    
    def set_frame(self):
        try:
            frame = self.deque[-1]
            self.image_view.setImage(frame)
        except:
            print("exception")
    




# class GUI():
#     def __init__(self, system):
#         super(GUI, self).__init__()
#         system.StartUp()
#         self.app = QApplication([])
#         self.deques = []
#         for deque in deques:
#             cam = CameraWindow(deque)
#             self.deques.append(cam)
        

#     def run(self):
#         for window in self.deques:
#             window.show()
#         self.app.exit(self.app.exec())

# """Individual window for a camera feed"""
# class CameraWindow(QMainWindow):
#     def __init__(self,deque):
#         super().__init__()

#         self.deque = deque
#         self.central_widget = QWidget()
        
#         self.button_max = QPushButton('openCV', self.central_widget)
#         # self.button_frame = QPushButton('Acquire Frame', self.central_widget)

#         self.layout = QVBoxLayout(self.central_widget)

#         self.layout.addWidget(self.button_max)
#         # self.layout.addWidget(self.button_frame)
#         self.button_max.clicked.connect(self.button_pressed)
#         # self.button_frame.clicked.connect(self.update_image)

        

        

#         # self.setCentralWidget(self.central_widget)

        
        
#         self.image_view = ImageView()
#         self.layout.addWidget(self.image_view)

#         # self.video_frame = QtGui.QLabel()

#         # self.get_frame_thread = Thread(target=self.get_frame)
#         # self.get_frame_thread.start()

#         # self.set_frame()



#     def button_pressed(self):
#         self.get_frame_thread = Thread(target=self.get_frame)
#         self.get_frame_thread.start()
#         print('Button Pressed')
#         self.startCamera()

#     def update_image(self):
#         frame = self.camera.get_frame()
#         self.image_view.setImage(frame.T)


#     #thread here
#     # def video(self):
#     #     #create class boolean to determine if camera needs initialized
#     #     for _ in range (50):
#     #         frame = self.camera.get_frame()
#     #         self.image_view.setImage(frame.T)
#     def get_frame(self):
#         # self.startCamera()
#         while True:
#             try:
#                 # frame = self.camera.get_frame()
#                 # self.deque.append(frame)
#                 frame = self.deque[-1]
#                 self.image_view.setImage(frame.T)
#             except:
#                 print("deque error probably full")
    
#     def set_frame(self):
#         try:
#             frame = self.deque[-1]
#             self.image_view.setImage(frame)
#         except:
#             print("exception")
