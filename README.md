# RescueTrek Phase 2 Gun Detection Model

This repository contains the machine learning gun detection model for RescueTrek Phase 2. The model is designed to detect guns in images and video footage.

## Installation

To set up the environment and install the necessary dependencies, follow these steps:

1. Install CUDA 11.7. https://developer.nvidia.com/cuda-11-7-0-download-archive
2. Install Python 3.9 https://www.python.org/downloads/release/python-398/
3. Create a virtual environment for Python 3.9 by running the following command in Command Prompt:

    ```
    python -m venv myenv
    ```

4. 
### Windows

    Activate the virtual environment by running the following command:

    ```
    myenv\Scripts\activate
    ```

### Linux/MacOS

    Activate the virtual environment by running the following command:

    ```
    source myenv/bin/activate
    ```

5. Install all the requirements listed in the `requirements.txt` file by running the following command:

    ```
    pip install -r requirements.txt
    ```

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

2. Run the face detection module by executing the following command in a separate terminal:

    ```
    python FaceDetection_v1/detect.py
    ```

3. Train the facial detection model by running the following command in the virtual environment within a separate terminal:

    ```
    streamlit run FaceDetection_v1/train_GUI.py
    ```

Please note that running the UI and face detection modules require separate terminals, while training the facial detection model can be done within the same terminal.

## License

This project is licensed under the [MIT License](LICENSE).