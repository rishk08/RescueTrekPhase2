import Yolov5.detect as Yd
import threading
import streamlit as st
import signal

import os
import subprocess
import glob
import base64


def Yolo_site():
    # st.title("RescueTrek")
    opts = Yd.parse_opt()
    opts.source = "cam_locations.streams"
    Yd.main(opts)


def write_to_file(filename, stringer):
    filer = open(filename, "a")
    filer.write(stringer)
    filer.close()

def display_images(folder_path):
    image_files = glob.glob(f"{folder_path}/*.jpg")

    if len(image_files) == 0:
        st.write("No images found in the specified folder.")
    else:
        for image_file in image_files:
            file_name = os.path.basename(image_file)
            file_name_withoutext  = os.path.splitext(file_name)

            with open(image_file, "rb") as f:
                image_data = f.read()
                b64_data = base64.b64encode(image_data).decode("utf-8")
                image_data_url = f"data:image/jpeg;base64,{b64_data}"

            st.write(
                f'<div style="text-align: center;">'
                f'<img src="{image_data_url}" alt="{file_name}" width="300">'
                f'<p>Name: {file_name_withoutext}</p>'
                f"</div>",
                unsafe_allow_html=True
            )
            
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
        write_to_file("cam_locations.streams", "\n" + camera_location + "\n")
        camera_location = ""

    if done:
        emp.empty()
        Yolo_site()        

        


def main():
    num_cams = 0

    st.sidebar.image("rescuetrek.png", use_column_width=True)
    pages = {
        "Home": home_page,
        "Facial Detection": facial_detection_page,
        "Display Images": lambda: display_images("./FaceDetection_v1/output_frames")
    }
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
