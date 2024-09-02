import streamlit as st
import requests
import os

with st.sidebar:
    st.subheader("PreSets")
    
    uploaded_image_file = st.file_uploader("Choose a image file", type=['png', 'jpg'])
    uploaded_video_file = st.file_uploader("Choose a video file", type=['mp4'])

    eye_option = st.selectbox(
        "eye retargeting?",
        ("False", "True"),)
    
    if eye_option == 'True':
        eye_option = True
    else:
        eye_option = False
    
    lip_option = st.selectbox(
        "lip retargeting?",
        ("False", "True"),)
    
    if lip_option == 'True':
        lip_option = True
    else:
        lip_option = False

    stitching_option = st.selectbox(
        "stitching ?",
        ("True", "False"),)
    
    if stitching_option == 'True':
        stitching_option = True
    else:
        stitching_option = False
    
    relative_motion_option = st.selectbox(
        "relative motion ?",
        ("True", "False"),)
    
    if relative_motion_option == 'True':
        relative_motion_option = True
    else:
        relative_motion_option = False
    
    button = st.button("Summit", type = 'primary')

if button:
    data = {
            "flag_eye_retargeting": eye_option,
            "flag_lip_retargeting": lip_option,
            "flag_stitching": stitching_option,
            "flag_relative_motion": relative_motion_option,}
    
    files = {
            "image": (uploaded_image_file.name, uploaded_image_file, uploaded_image_file.type),
            "video": (uploaded_video_file.name, uploaded_video_file, uploaded_video_file.type),
        }
    
    
    response = requests.post("http://127.0.0.1:8000/upload", files=files, data=data)
    result = response.json()
    result_filename = result['result_filename']
    
    video_file = open(os.path.join("/workspace/Live_expression/results/", uploaded_image_file.name.replace(".jpg", "").replace(".png", "") + "--" + uploaded_video_file.name), "rb")
    video_bytes = video_file.read()

    st.video(video_bytes)
