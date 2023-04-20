# Import required libraries
import os
import cv2
import numpy as np
import mtcnn
#import FaceDetection_v1.architecture as arch
import architecture as arch
from train_v2 import normalize, l2_normalizer
from scipy.spatial.distance import cosine
#from tensorflow.keras.models import load_model
import pickle
import shutil
import time
from pathlib import Path

# Confidence threshold for MTCNN face detector
confidence_t = 0.99
# Recognition threshold for face recognition model
recognition_t = 0.5
# Required size for face recognition model
required_size = (160,160)

# Shared variable to store the name of the detected face
detected_name = None

#To access the detected name in other files, simply import 
#the function get_detected_name and call it. Here's an example:

#from main_script import get_detected_name
#name = get_detected_name()
#print(f"The detected face name is: {name}")

def get_detected_name():
    return detected_name

def wipe_output_folder(folder_path, exclude_file=None):
    for filename in os.listdir(folder_path):
        if filename == exclude_file:
            continue

        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

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
    with open(path, 'rb') as f:
        encoding_dict = pickle.load(f)
    return encoding_dict

def detect(img ,detector,encoder,encoding_dict):
    """
    Detects faces in the provided image using MTCNN face detector and performs face recognition using the provided
    FaceNet model and encoding dictionary
    """
    global detected_name
    detected_name = "unknown"
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(img_rgb)
    for res in results:
        # Check if face detection confidence is above the set threshold
        if res['confidence'] < confidence_t:
            continue
        # Crop the face from the image
        face, pt_1, pt_2 = get_face(img_rgb, res['box'])
        # Encode the face using the FaceNet model
        encode = get_encode(encoder, face, required_size)
        # L2 normalize the encoding
        encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
        name = 'unknown'

        # Compute cosine distance between the face encoding and all encodings in the dictionary to perform face recognition
        distance = float("inf")
        for db_name, db_encode in encoding_dict.items():
            dist = cosine(db_encode, encode)
            # Check if distance is below the set recognition threshold and smaller than the current smallest distance
            if dist < recognition_t and dist < distance:
                name = db_name
                distance = dist

        # Draw bounding box and label on the image based on the recognized person's name
        if name == 'unknown':
            cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
            cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1) 
        else:
            cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
            cv2.putText(img, name + f'__{distance:.2f}', (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 2,
                        (0, 200, 200), 1)  

            detected_name = name
    return img



def main(filename="input_frames"):
    print("\n\n\n\n\nRAN\n\n\n\n\n")
    # Set the required shape of the input image
    required_shape = (160,160)
    # Load the FaceNet model
    face_encoder = arch.InceptionResNetV2()
    #path_m = "FaceDetection_v1\\facenet_keras_weights.h5"
    path_m = ".\\facenet_keras_weights.h5"
    face_encoder.load_weights(path_m)

    # Load the encoded feature vectors of known faces from the pickle file
    #encodings_path = 'FaceDetection_v1\\encodings\\encodings.pkl'
    encodings_path = 'encodings\\encodings.pkl'
    encoding_dict = load_pickle(encodings_path)

    # Create an instance of MTCNN face detector
    face_detector = mtcnn.MTCNN()

    # path to folders with frames
    
    #image_folder = filename
    #image_folder = "FaceDetection_v1\\input_frames"
    #output_folder = "FaceDetection_v1\\output_frames"
    image_folder = "input_frames"
    output_folder = "output_frames"

    # Initialize a set to store detected names
    detected_names_set = set()

    filename_arr = []

    dummy_true_var = True
    #a while loop that checks through the file folder 
    while dummy_true_var:
        
        #if folder is empty, then reset the filename_arr
        if os.listdir(image_folder) == []:
            filename_arr = []
        # A loop that iterates through the image files in the folder
        #for image_file in os.listdir(image_folder)[-3:]:
        for image_file in os.listdir(image_folder):
            if image_file in filename_arr:
                next
            else:
                print(image_file)
                filename_arr.append(image_file)
                # Check if the file is an image (you can modify the list of valid extensions if needed)
                if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # Replace this line with code to read an image file using cv2.imread()
                    frame = cv2.imread(os.path.join(image_folder, image_file))

                    # Detect and recognize faces in the current frame
                    frame = detect(frame, face_detector, face_encoder, encoding_dict)

                    # Save the processed frame with bounding boxes and names
                    if detected_name != "unknown" and detected_name not in detected_names_set:
                        output_file = os.path.join(output_folder, f"{detected_name}.jpg")
                        cv2.imwrite(output_file, frame)
                        print(f"Face detected: {detected_name}")
                        detected_names_set.add(detected_name)
        time.sleep(5)
    # Close all windows
    cv2.destroyAllWindows()
    return detected_names_set

if __name__ == '__main__':
    main()