import histogram as w
import Feed as g
# w.webcamCV()

# cam = g.Camera('rtsp://admin:@10.224.3.244/1')
# cam.initialize()

# G = g.GUI(cam)

# G.run()

# while(input() != "q"):
#     print("running")
# G.run()
# app = g.QApplication([])
# window = g.GUI()
# window.show()
# app.exit(app.exec())

cam = g.Camera(0, -1, "admin", "admin")
cam.initialize()
print(cam)
cam.show()
cam.close()