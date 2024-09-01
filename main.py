import streamlit as st

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
    
    if uploaded_image_file is not None:
        with open(f"/workspace/Live_expression/uploads/{uploaded_image_file.name}", "wb") as f:
            f.write(uploaded_image_file.getbuffer())
    
    if uploaded_video_file is not None:
        with open(f"/workspace/Live_expression/uploads/{uploaded_video_file.name}", "wb") as f:
            f.write(uploaded_video_file.getbuffer())

    st.video(uploaded_video_file)