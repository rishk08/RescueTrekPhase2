# Import required libraries
import cv2
import numpy as np
import mtcnn
from architecture import *
from train_v2 import normalize, l2_normalizer
from scipy.spatial.distance import cosine
from tensorflow.keras.models import load_model
import pickle
import streamlit as st

# Confidence threshold for MTCNN face detector
confidence_t = 0.99
# Recognition threshold for face recognition model
recognition_t = 0.5
# Required size for face recognition model
required_size = (160, 160)


def get_face(img, box):
    """
    Crops the face from the given image based on the box coordinates provided
    """
    x1, y1, width, height = box
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face, (x1, y1), (x2, y2)


def get_encode(face_encoder, face, size):
    """
    Encodes a given face image using the provided FaceNet model
    """
    face = normalize(face)
    face = cv2.resize(face, size)
    encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
    return encode


def load_pickle(path):
    """
    Loads a dictionary from a pickle file
    """
    with open(path, "rb") as f:
        encoding_dict = pickle.load(f)
    return encoding_dict


def detect(img, detector, encoder, encoding_dict):
    """
    Detects faces in the provided image using MTCNN face detector and performs face recognition using the provided
    FaceNet model and encoding dictionary
    """
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(img_rgb)
    for res in results:
        # Check if face detection confidence is above the set threshold
        if res["confidence"] < confidence_t:
            continue
        # Crop the face from the image
        face, pt_1, pt_2 = get_face(img_rgb, res["box"])
        # Encode the face using the FaceNet model
        encode = get_encode(encoder, face, required_size)
        # L2 normalize the encoding
        encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
        name = "unknown"

        # Compute cosine distance between the face encoding and all encodings in the dictionary to perform face recognition
        distance = float("inf")
        for db_name, db_encode in encoding_dict.items():
            dist = cosine(db_encode, encode)
            # Check if distance is below the set recognition threshold and smaller than the current smallest distance
            if dist < recognition_t and dist < distance:
                name = db_name
                distance = dist

        # Draw bounding box and label on the image based on the recognized person's name
        if name == "unknown":
            cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
            cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        else:
            cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
            cv2.putText(
                img,
                name + f"__{distance:.2f}",
                (pt_1[0], pt_1[1] - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 200, 200),
                2,
            )
    return img


if __name__ == "__main__":
    # Set the required shape of the input image
    required_shape = (160, 160)
    # Load the FaceNet model
    face_encoder = InceptionResNetV2()
    path_m = "facenet_keras_weights.h5"
    face_encoder.load_weights(path_m)

    # Load the encoded feature vectors of known faces from the pickle file
    encodings_path = "encodings/encodings.pkl"
    encoding_dict = load_pickle(encodings_path)

    # Create an instance of MTCNN face detector
    face_detector = mtcnn.MTCNN()

    # Open the default camera
    cap = cv2.VideoCapture(0)
    col1, col2 = st.columns(2)

    # Keep processing frames until the user exits
    while cap.isOpened():
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("CAM NOT OPEND")
            break

        # Detect and recognize faces in the current frame
        frame = detect(frame, face_detector, face_encoder, encoding_dict)

        # Display the output frame with bounding boxes and labels
        try:
            framer1.empty()
            framer2.empty()
        except Exception:
            pass
        with col1:
            framer1 = st.image(frame)
        with col2:
            framer2 = st.image(frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
