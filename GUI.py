import Yolov5.detect as Yd
import threading
import streamlit as st

def intro():

    st.write("# Welcome to Streamlit! 👋")
    st.sidebar.success("Select a demo above.")


def Yolo_site():
    st.title('RescueTrek')
    opts = Yd.parse_opt()
    Yd.main(opts)

if __name__ == "__main__":
    page_names_to_funcs = {
        "Gun Detection": Yolo_site,
    }

    demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
    page_names_to_funcs[demo_name]()    