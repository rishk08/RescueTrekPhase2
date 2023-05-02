# RescueTrek Phase 2 Gun Detection Model

This repository includes the RescueTrek Phase 2 machine learning model for gun detection. The model leverages Yolov5 with PyTorch as the underlying framework for gun detection in both images and video footage. It effectively identifies guns and humans in the provided data, enabling the identification of potential shooters. Additionally, facial detection is employed using FaceNet, which operates on the TensorFlow framework. This combination of Yolov5 with PyTorch for gun detection and FaceNet with TensorFlow for facial detection ensures accurate and efficient analysis of the input imagery and video.

Furthermore, this repository integrates Twilio, a communication platform, to enhance the functionality of the system. The detect.py script in the FacialDetection module utilizes Twilio to send alerts about potential shooters. It pulls contact information from the contacts.csv file, which contains the necessary details of recipients. By leveraging Twilio's capabilities, the system can quickly notify relevant parties in case of detected threats.

## Installation

To set up the environment and install the necessary dependencies, follow these steps:

1. Install Python 3.9 https://www.python.org/downloads/release/python-398/
2. Create a virtual environment for Python 3.9 by running the following command in Command Prompt:

    ```
    python -m venv myenv
    ```

3. Activate the virtual environment by running the following command:
### Windows

    source myenv/Scripts/activate

### Linux/MacOS

    source myenv/bin/activate

4. Install all the requirements listed in the `requirements.txt` file by running the following command:

    ```
    pip install -r requirements.txt
    ```

### Running Object Detection on GPU (Optional)

5. Install CUDA 11.7. https://developer.nvidia.com/cuda-11-7-0-download-archive

6. Install PyTorch and related libraries by running the following command:

    ```
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
    ```

## Usage

Once the environment is set up, you can use the model with the following steps:

1. Run the UI by executing the following command in a separate terminal within the virtual environment:

    ```
    streamlit run GUI.py
    ```

2. Run the facial detection model by executing the following command in a separate terminal within the virtual environment. This model uses the weights stored in facenet_keras_weights.h5 to detect faces and Twilio API to send alerts:

    ```
    python FaceDetection_v1/detect.py
    ```

3. Train the facial detection model by running the following command in the virtual environment within a separate terminal. This model trains faces using the images stored in facepics folder and saves the weights to facenet_keras_weights.h5:

    ```
    streamlit run FaceDetection_v1/train_GUI.py
    ```

Please note that running the user interface and facial detection models require separate terminals to run simultaneously. The contacts.csv file is used by the detect.py script to pull the contacts' information to send the alerts.

## License

This project is licensed under the [MIT License](LICENSE).