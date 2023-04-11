import Yolov5.detect as Yd
import threading
import streamlit as st
import signal


def Yolo_site():
    st.title('RescueTrek')
    opts = Yd.parse_opt()
    opts.source = "cam_locations.streams"
    Yd.main(opts)

def write_to_file(filename, stringer):
    filer = open(filename, "a")
    filer.write(stringer)
    filer.close()


def main():
    num_cams = 0
    # with open("cam_locations.streams", "r+") as my_file:
    #     my_file.seek(0)
    #     my_file.truncate()
    #     print("CLEARED")
    done = False
    camera_location = st.text_input('Add Camera')
    emp = st.empty()
    num_cams = 0
    done = emp.button("Done adding cameras!")

    if camera_location and not done:
        write_to_file("cam_locations.streams", camera_location + "\n")
        num_cams += 1
        print(num_cams)
        camera_location = ""
    
    if done:
        emp.empty()
        Yolo_site()

if __name__ == '__main__':
    main()



            


    
