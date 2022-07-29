import streamlit as st
from helper import search_frame, cut_results, read_video, write_video
import os
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
            spams, ndarray, scores = search_frame(uploaded_file.name, text_prompt, int(topn_value), float(cut_sim_value))
            video_data = read_video(uploaded_file.name)
            os.makedirs('tmp_videos', exist_ok=True)
            for spam in spams:
                i = spams.index(spam)
                save_name = 'tmp_videos/' + str(i) + '_tmp.mp4'
                write_video(save_name, video_data[int(spam['left']):int(spam['right'])])
                st.video(save_name)
                os.remove(save_name)
        st.success('Done!')
    else:
        st.write('Please upload your video first')
