import streamlit as st
from helper import search_frame, get_img_np_from_b64
st.set_page_config(page_title="CLIP Video Indexer", page_icon="🔍")
st.title('CLIP Video Indexer')
uploaded_file = st.file_uploader("Choose a file")
video_data = ''
text_prompt = st.text_input("Text Prompt", "一群人站在一起")
topn_value = st.text_input("Top N", "5")
search_button = st.button("Search")
if search_button:
    if uploaded_file is not None:
        with st.spinner("Processing..."):
            candidates, b64, scores = search_frame(uploaded_file.name, text_prompt, int(topn_value))
            for each in candidates:
                i = candidates.index(each)
                st.image(get_img_np_from_b64(b64[i][22:]), caption=str(scores[i]))  # [22:] to cut the prefix for CaS
        st.success("Done!")
    else:
        st.write("Please upload your video first")
