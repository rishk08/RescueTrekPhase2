import threading
import GUI
import queue

def main():
    q = queue.Queue()
    qq = queue.Queue()
    qqq = queue.Queue()
    dequeues = [q, qq, qqq]
    def fillQueues(dequeus):
        while True:
            if not q.full:
                dequeues[0].put(cv2.imread("photos/images.jpg"))
                dequeues[0].put(cv2.imread("photos/images2.jpg"))
    fill = threading.Thread(target=fillQueues, args=(dequeues,))
    fill.start()
    
    displayObj = GUI.GUI(dequeues)
    displayObj.start()
    displayObj.join()

#After running the GUI, continue the rest of the application task

t = threading.Thread(target=main)
t.daemon = True
t.start()

while True:
    print("other stuff")



#############
