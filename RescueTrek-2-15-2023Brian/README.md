#### RescueTrek

### Prerequisites

- Python 3.7–3.9 installed on your system (dependency issues with later versions)
- pip package manager installed on your system

### Steps

**Note**: If you already have a Python virtual environment set up, you can skip the first few steps and start from step 4.

1. Open your terminal or command prompt.
2. Install the virtualenv package by running the following command:

    ```
    pip3 install virtualenv
    ```

3. Create a virtual environment folder named `venv` with Python 3.x by running the following command:

    ```
    virtualenv venv -p python3
    ```

4. Activate the virtual environment by running the following command:

    ```
    source venv/scripts/activate (Windows - Git bash terminal)
    ```

    or

    ```
    source venv/bin/activate (Linux/MacOS)
    ```

5. Install the required packages from the `requirements.txt` file by running the following command:

    ```
    pip install -r requirements.txt
    ```

6. Run the gun detection model:

    ```
    python main.py
    ```


(Optional) To list all the installed packages in the virtual environment into `requirements.txt`, run the following command:

    ```
    pip3 freeze > requirements.txt
    ```