from train_v2 import full
import streamlit as st

import os



def write_to_file(filename, stringer):
    filer = open(filename, "a")
    filer.write(stringer)
    filer.close()
            
def facial_detection_page():
    st.write("Welcome to the Facial Detection Page!")

    # Accept text input for the name
    name = st.empty()
    name_text = name.text_input("Enter a name:", key = "initial_name")

    # Choose a file to upload
    filer = st.empty()
    uploaded_file = filer.file_uploader("Choose a file to upload", key = "initial_file")

    train = st.empty()
    train_button = train.button("Train on New Image", key = "initial_button")

    trained = st.empty()
    
    if uploaded_file is not None and name_text != "":
        # Create a new directory with the given name
        base_path = "./FaceDetection_v1/facepics"
        new_folder_path = os.path.join(base_path, name_text)

        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        # Save the file in the created directory
        file_path = os.path.join(new_folder_path, f"{name_text}.jpg")

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        uploaded = st.empty()
        uploaded_text = uploaded.success(f"You uploaded a file, saved as {name_text}/{name_text}.jpg")


        if train_button:
            uploaded_text = uploaded.empty()
            trained_text = trained.warning("TRAINING, PLEASE WAIT")
            
            full()
            trained.empty()
            name_text = name.text_input("Enter a name:", key = name_text)
            uploaded_file = filer.file_uploader("Choose a file to upload", key = name_text)
            train_button = False


        


def main():
    num_cams = 0

    st.sidebar.image("rescuetrek.png", use_column_width=True)

    facial_detection_page()



if __name__ == "__main__":
    main()
