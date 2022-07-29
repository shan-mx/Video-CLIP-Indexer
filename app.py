import streamlit as st
from helper import search_frame, get_keyframes_data
import os
import skvideo.io

st.set_page_config(page_title='CLIP Video Indexer', page_icon='🔍')
st.title('CLIP Video Indexer')
uploaded_file = st.file_uploader('Choose a file')
text_prompt = st.text_input('Text Prompt', '')
topn_value = st.text_input('Top N', '5')
cut_sim_value = st.text_input('Cut Sim', '0.6')
search_button = st.button('Search')
if search_button:
    if uploaded_file is not None:
        with st.spinner('Processing...'):
            video_data = skvideo.io.vread(uploaded_file.name)
            keyframe_data = get_keyframes_data(video_data, float(cut_sim_value))
            spams, ndarray, scores = search_frame(keyframe_data, text_prompt, int(topn_value))
            os.makedirs('tmp_videos', exist_ok=True)
            for spam in spams:
                i = spams.index(spam)
                save_name = 'tmp_videos/' + str(i) + '_tmp.mp4'
                skvideo.io.vwrite(save_name, video_data[int(spam['left']):int(spam['right'])])
                st.video(save_name)
                os.remove(save_name)
        st.success('Done!')
    else:
        st.write('Please upload your video first')
