import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from keras_vggface.utils import preprocess_input

# Load the known face images and their names
known_faces = [
    image.load_img('C:/Users/richi/Downloads/RescueTrekPhase2/RescueTrek-2-15-2023Brian/facepics/richie1.jpg', target_size=(224, 224))
]
known_names = ['Richie']

# Load the VGGFace model for feature extraction
model = load_model('vggface.h5')

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Loop over the frames from the video stream
while True:
    # Read the frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    # Identify the persons in the detected faces
    names = []
    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (224, 224))
        face_img = image.img_to_array(face_img)
        face_img = np.expand_dims(face_img, axis=0)
        face_img = preprocess_input(face_img)
        face_encoding = model.predict(face_img)
        matches = []
        for known_face in known_faces:
            known_face = image.img_to_array(known_face)
            known_face = np.expand_dims(known_face, axis=0)
            known_face = preprocess_input(known_face)
            known_face_encoding = model.predict(known_face)
            match = np.dot(face_encoding.flatten(), known_face_encoding.flatten()) / (np.linalg.norm(face_encoding) * np.linalg.norm(known_face_encoding))
            matches.append(match)
        best_match_index = np.argmax(matches)
        if matches[best_match_index] > 0.5:
            name = known_names[best_match_index]
        else:
            name = 'Unknown'
        names.append(name)

    # Draw rectangles around the detected faces and label them with the persons' names
    for (x, y, w, h), name in zip(faces, names):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, name, (x + 6, y + h - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # Exit the program if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up the capture object and close the window
cap.release()
cv2.destroyAllWindows()
