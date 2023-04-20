# Import required libraries
#import FaceDetection_v1.architecture as arch
import architecture as arch
import os 
import cv2
import mtcnn
import pickle 
import numpy as np 
from sklearn.preprocessing import Normalizer
from tensorflow.keras.models import load_model

# Set path to the face images and define the required image size for the model
#face_data = 'FaceDetection_v1\\facepics'  # Directory path containing face images
face_data = 'facepics'  # Directory path containing face images
required_shape = (160,160)  # Required image size for face recognition model

# Load the InceptionResNetV2 model weights from file
face_encoder = arch.InceptionResNetV2()  # Initialize FaceNet model
#path = "FaceDetection_v1\\facenet_keras_weights.h5" # Path to FaceNet model weights
path = "facenet_keras_weights.h5" # Path to FaceNet model weights
face_encoder.load_weights(path)  # Load FaceNet model weights

# Initialize the MTCNN face detector, encoding list, and dictionary
face_detector = mtcnn.MTCNN()  # Initialize MTCNN face detector
encodes = []  # List to store face encodings
encoding_dict = dict()  # Dictionary to store face encodings with person name as key

# Initialize the L2 normalizer
l2_normalizer = Normalizer('l2')  # Initialize L2 normalizer

# Define function to normalize image
def normalize(img):
    """
    Normalizes image by subtracting mean and dividing by standard deviation
    """
    mean, std = img.mean(), img.std()
    return (img - mean) / std

# Loop over all face images in the dataset
for face_names in os.listdir(face_data):
    person_dir = os.path.join(face_data,face_names)

    # Loop over all images of each person
    for image_name in os.listdir(person_dir):
        image_path = os.path.join(person_dir,image_name)

        # Read image and convert color from BGR to RGB
        img_BGR = cv2.imread(image_path)
        img_RGB = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2RGB)

        # Detect face using MTCNN and crop the image to the face
        x = face_detector.detect_faces(img_RGB)
        x1, y1, width, height = x[0]['box']
        x1, y1 = abs(x1) , abs(y1)
        x2, y2 = x1+width , y1+height
        face = img_RGB[y1:y2 , x1:x2]

        # Normalize the face image and resize to required shape
        face = normalize(face)
        face = cv2.resize(face, required_shape)
        face_d = np.expand_dims(face, axis=0)

        # Encode the face using the FaceNet model and append to encoding list
        encode = face_encoder.predict(face_d)[0]
        encodes.append(encode)

    # If there are any encodings, sum them and L2 normalize the final encoding
    if encodes:
        encode = np.sum(encodes, axis=0 )
        encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]
        encoding_dict[face_names] = encode  # Store face encoding in dictionary with person name as key
        encodes = []  # Reset encodes list for the next person

# Save the encoding dictionary to file
#path = 'FaceDetection_v1\\encodings\\encodings.pkl'  # Path to save encoding dictionary
path = 'encodings\\encodings.pkl'  # Path to save encoding dictionary
with open(path, 'wb') as file:
    pickle.dump(encoding_dict, file)  # Save encoding dictionary to file using pickle
