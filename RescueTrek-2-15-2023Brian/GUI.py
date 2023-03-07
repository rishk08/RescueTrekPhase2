from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QPushButton, QVBoxLayout, QWidget, QGridLayout,QLayoutItem, QLabel, QSizePolicy, \
    QLineEdit, QFormLayout
from PyQt6.QtCore import QTimer, Qt
# from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap, QImage, QDoubleValidator
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
from system import System
from modelclass import *
import numpy as np

import constant as const

pyqtgraph.setConfigOptions(imageAxisOrder = 'row-major')


# Create the image detector object
itemDetector = imageDetector("my_mobilenet_v14_model", "../pretrained_models", "../coco_v2.names", 0.5)
itemDetector_created_bool = False

class GUI:
    def __init__(self, configFile):
        # Start the system and set up the GUI
        self.system = System(configFile)
        self.cameras = self.system.GetCameras()
        self.itemDetectorThreshold = 0.5
        self.app = QApplication([])
        self.window = MainWindow(self.cameras)
        self.window.show()
        self.app.exec()

    def run(self):
        # Call the GUI's run method
        self.window.run()


class MainWindow(QMainWindow):
    def __init__(self, cameras):
        super().__init__()
        
        self.setStyleSheet(open('css/stylesheet.css').read())
        self.confidenceLevels = []
        self.cameras = []
        self.cameraWindows = []
        self.colorList = np.random.uniform(low=0, high=255, size=(len(cameras), 3))
        self.priorityWindow = None
        self.oldPriorityWindow = None
        
        # Here to keep feed with most recent gun detected in the priority feed if no further guns are detected in other feeds
        self.central_widget = QLabel("Null Threat")
        self.central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap('imgs/null_threat_grey.png')
        self.central_widget.setPixmap(pixmap)
        self.central_widget.setScaledContents(True)
        
        self.setWindowTitle("Null Threat")
        self.setCentralWidget(self.central_widget)
        self.showMaximized()

        self.button_start = QPushButton('start')
        self.button_start.setStyleSheet(open('css/buttons.css').read())
        self.button_start.setFixedHeight(100)
        self.button_start.setFixedWidth(300)
        
        self.main_layout = QGridLayout(self.central_widget) 
        self.main_layout.addWidget(self.button_start, 1, 0, 2, 1)
        
        self.priority_view = QLabel(pixmap=QPixmap("imgs/null_threat_discord.png"))
        self.priority_view.setFixedHeight(900)
        self.priority_view.setFixedWidth(900)
        self.priority_view.setScaledContents(True)
        self.priority_view.setStyleSheet('margin-bottom: 150%; margin-top: 150%;')
        self.main_layout.addWidget(self.priority_view, 0, 0, 3, 1)
        
        self.priority_label = QLabel(text="Priority Cam: ")
        self.priority_label.setFixedWidth(900)
        self.priority_label.setStyleSheet('background-color:black; color: white; margin-bottom: 150%; margin-top: 150%; magin-left: -350%')
        self.main_layout.addWidget(self.priority_label, 0, 0, 3, 1, Qt.AlignmentFlag.AlignTop)
        
        self.priority_view.hide()
        self.priority_label.hide()

        self.button_start.clicked.connect(self.run)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_priority)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(10)

        self.confidenceVal = None
        self.priorityCameraWindow = None
        self.maxConfidence = 0
        self.currPriorityCamera = 0
        self.currOldPriorityCamera = 0

        # make system provide cameras, put this in a function and remove parameter
        for camera in cameras:
            self.cameras.append(camera)
        
        
    def update_priority(self):
        # Create a list of tuples of (camera, priority) from the cameras list
        priorities = [(camera, i) for i, camera in enumerate(self.cameras)]
        
        # Sort the priorities list by priority level in descending order
        priorities.sort(key=lambda x: x[1], reverse=True)
        
        # Get the camera object with the highest priority level
        priority_camera = priorities[0][0]
        
        # Set the priority window to display the bounding box frame of the camera object
        if self.priorityWindow is None:
            self.priorityWindow = priority_camera
        elif priority_camera != self.priorityWindow and priority_camera != self.oldPriorityWindow:
            self.oldPriorityWindow = self.priorityWindow
            self.priorityWindow = priority_camera
        
        frame = self.priorityWindow.boundingBoxFrame
        image = QImage(frame, frame.shape[1], frame.shape[0], 
                    frame.strides[0], QImage.Format.Format_RGB888)
        image = image.rgbSwapped()
        self.priority_view.setPixmap(QPixmap.fromImage(image))


    def update_time(self):
        self.current = time.time()

        
    def startup():
        """call system startup and get the number of feeds so the GUI can organize itself"""
        pass

    def run(self):
        self.button_start.hide()
        self.priority_view.show()
        self.priority_label.show()
        # Replace self.cameras with location of cameras from system produced by startup()
        for i, camera in enumerate(self.cameras):
            cam = CameraWindow(camera)
            self.main_layout.addWidget(cam.return_frame(), i, 1, 1, 1)
            self.cameraWindows.append(cam)
        for camera in self.cameraWindows:
            camera.startCamera()

        self.button_update_threshold = QPushButton('Update Threshold')
        self.button_update_threshold.clicked.connect(self.open_threshold_menu)
        self.button_update_threshold.setStyleSheet('background-color: black; color: white; margin-right:50%; margin-left: 250%')
        self.main_layout.addWidget(self.button_update_threshold, len(self.cameraWindows), 1, 1, 1)

    def open_threshold_menu(self):
        try:
            self.threshold_window = ThresholdWindow()
            self.threshold_window.show()
        except Exception as err:
            print(err)
            print("Unable to initializeWindow")
            sys.exit(0)
            

class ThresholdWindow(QWidget):
    """
    This window allows the user to change the threshold value for item detection.
    """
    def __init__(self):
        super().__init__()

        self.password_input = QLineEdit()
        self.password_input.textChanged.connect(self.password_text_changed)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.threshold_input = QLineEdit()
        self.threshold_input.setValidator(QDoubleValidator(0.99, 99.99, 2))
        self.threshold_input.textChanged.connect(self.threshold_number_changed)

        self.status_label = QLabel("Enter Password and Threshold Values")

        enter_button = QPushButton('Enter')
        enter_button.clicked.connect(self.entered_values)

        layout = QFormLayout()
        layout.addRow(self.status_label)
        layout.addRow("Threshold Value", self.threshold_input)
        layout.addRow("Password", self.password_input)
        layout.addRow(enter_button)

        self.setLayout(layout)
        self.setWindowTitle("Change Threshold Value")

        self.password = ""
        self.threshold_value = const.ITEM_DETECTOR_THRESHOLD

    def password_text_changed(self, text):
        """Update the stored password when the password input changes."""
        self.password = text

    def threshold_number_changed(self, text):
        """Update the stored threshold value when the threshold input changes."""
        self.threshold_value = float(text)

    def validate_entered_values(self):
        """Validate the entered password and threshold value."""
        if self.password != const.ADMINISTRATOR_PASSWORD:
            return False, "Incorrect password."

        if self.threshold_value < 0.2 or self.threshold_value > 1:
            return False, "The threshold value must be between 0.2 and 1."

        return True, ""

    def entered_values(self):
        """
        Update the threshold value if the entered password is correct and
        the threshold value is valid.
        """
        is_valid, message = self.validate_entered_values()
        if not is_valid:
            self.status_label.setText(message)
            return

        const.list_of_values.change_threshold_value(self.threshold_value)
        self.status_label.setText(f"The threshold was changed to {self.threshold_value}.")


"""Individual window for a camera feed"""
class CameraWindow(QWidget):
    def __init__(self, camera):
        super().__init__()
        self.setStyleSheet(open('css/cameraWindow.css').read())
        self.deque = deque(maxlen=100)

        self.camera = camera
        self.layout = QGridLayout()

        self.frame = None
        self.boundingBoxFrame = None
        self.frame_updated = False

        self.image_view = QLabel(
            pixmap=QPixmap("imgs/null_threat_discord.png")
        )
        self.image_view.setScaledContents(True)
        self.image_view.setStyleSheet('margin-right:50%; margin-left: 250%;')
        self.is_pri = False
        self.is_old_pri = False

        self.start = 0
        self.current = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image_no_deque)
        self.timer.start(.05)

        self.get_frame_thread = Thread(target=self.get_frame)
        self.get_frame_thread.daemon = True
        self.get_frame_thread.start()

    def get_frame(self):
        while True:
            try:
                frame = self.camera.get_data()
                self.frame = frame
                self.frame_updated = True
            except Exception as err:
                print(err)
                print("deque error probably full")

    def update_image_no_deque(self):
        global itemDetector

        if self.frame_updated:
            try:
                self.confidenceLevel, frame = itemDetector.detector.createBoundingBox(self.frame, const.list_of_values.return_threshold_value())
                self.current = time.time()
                fps = 1 / (self.current - self.start)
                self.start = self.current
                cv2.putText(frame, "FPS: " + str(int(fps)) + " cam " + str(self.camera.ip), (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                image = QImage(frame, frame.shape[1], frame.shape[0], 
                       frame.strides[0], QImage.Format.Format_RGB888)
                image = image.rgbSwapped()
                self.image_view.setPixmap(QPixmap.fromImage(image))
                self.image_view.setScaledContents(True)
                self.boundingBoxFrame = frame
                self.frame_updated = False
            except Exception as err:
                print(err)
                print("error in no deque")

    def update_border(self, is_pri=False, is_old_pri=False):
        border_color = {
            True: 'red',
            False: {
                True: 'yellow',
                False: 'black'
            }
        }[is_pri][is_old_pri]
        border_style = f'margin-right:50%; margin-left: 250%; border: 10px solid {border_color};'
        
        self.image_view.setStyleSheet(border_style)
        self.is_pri = is_pri
        self.is_old_pri = is_old_pri

    def get_priority(self):
        return (self.is_pri, self.is_old_pri)

    def update_time(self):
        self.current = time.time()

    def update_image_fps(self):
        if not self.deque:
            return
        
        frame = self.deque.pop()
        fps = 1 / (self.current - self.start)
        self.start = time.time()
        
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.putText(frame, "FPS: " + str(int(fps)) + " cam " + str(self.camera.ip), (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
            image = image.rgbSwapped()

            self.image_view.setPixmap(QPixmap.fromImage(image))
            self.image_view.setScaledContents(True)
            self.frame = frame

        except Exception as e:
            print(f"Error in update_image_fps: {e}")
            
    def startCamera(self):
        self.camera.initialize()
   
    def get_frame_detector(self):
        pass

    def return_frame(self):
        return self.image_view

    def return_cv2_frame(self):
        return self.frame