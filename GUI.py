import Yolov5.detect as Yd
import threading
import streamlit as st
import signal

intro_ran = 0
def intro():
    if intro_ran == 0:
        st.write("# Welcome to Streamlit! 👋")
        st.sidebar.success("Select a demo above.")


def Yolo_site():
    st.title('RescueTrek')
    for i in Create_cams("Yolov5\cam_locations.txt"):
        opts = Yd.parse_opt()
        opts.source = i
    Yd.main(opts)

def Create_cams(filename):
    cams = []
    file = open(filename, "r")
    for line in file:
        cams.append(line)
    return cams


if __name__ == "__main__":
    Yolo_site()        
    
