import Yolov5.detect as Yd
import threading
import streamlit as st
import signal

import os
import subprocess


def Yolo_site():
    # st.title("RescueTrek")
    opts = Yd.parse_opt()
    opts.source = "cam_locations.streams"
    Yd.main(opts)


def write_to_file(filename, stringer):
    filer = open(filename, "a")
    filer.write(stringer)
    filer.close()


def facial_detection_page():
    st.write("Welcome to the Facial Detection Page!")

    # Accept text input for the name
    name = st.text_input("Enter a name:")

    # Choose a file to upload
    uploaded_file = st.file_uploader("Choose a file to upload")

    if uploaded_file is not None:
        # Create a new directory with the given name
        base_path = "./FaceDetection_v1/facepics"
        new_folder_path = os.path.join(base_path, name)

        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        # Save the file in the created directory
        file_path = os.path.join(new_folder_path, f"{name}.jpg")

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write(f"You uploaded a file, saved as {name}/{name}.jpg")


def home_page():
    done = False
    camera_location = st.text_input("Add Camera")
    emp = st.empty()
    done = emp.button("Done adding cameras!")

    if camera_location and not done:
        write_to_file("cam_locations.streams", camera_location + "\n")
        camera_location = ""

    if done:
        emp.empty()
        Yolo_site()


def main():
    num_cams = 0

    st.sidebar.image("rescuetrek.png", use_column_width=True)
    pages = {"Home": home_page, "Facial Detection": facial_detection_page}
    page = st.sidebar.radio("Go to", list(pages.keys()))

    # Display the selected page
    pages[page]()
    # st.image("rescuetrek.png")
    # st.markdown("<br>", unsafe_allow_html=True)
    # st.sidebar.markdown("<br>", unsafe_allow_html=True)
    # with open("cam_locations.streams", "r+") as my_file:
    #     my_file.seek(0)
    #     my_file.truncate()
    #     print("CLEARED")


if __name__ == "__main__":
    main()
