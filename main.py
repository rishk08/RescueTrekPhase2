import histogram as w
import GUI as g
# w.webcamCV()

cam = g.Camera(0)
cam.initialize()

G = g.GUI(cam)

G.run()

# G.run()
# app = g.QApplication([])
# window = g.GUI()
# window.show()
# app.exit(app.exec())

# cam = g.Camera(0)
# cam.initialize()
# print(cam)
# cam.show()
# cam.close()