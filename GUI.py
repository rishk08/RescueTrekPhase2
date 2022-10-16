from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
# import pyqt
import pyqtgraph
import histogram as w

class GUI:
    def button_pressed():
        print('Button Pressed')
        w.webcamCV()
    
    # def activateHist():
    #     w.webcamCV()

    def run():
        app = QApplication([])
        win = QMainWindow()
        button = QPushButton('Test')
        button.clicked.connect(GUI.button_pressed)
        win.setCentralWidget(button)
        win.show()
        app.exit(app.exec())