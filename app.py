import streamlit as st
import auto_shorts
import auto_shorts.main
import os


with st.form("Shorts_maker", clear_on_submit=True):
    st.write("Shorts Generator")
    vid_url = st.text_input("Enter the video url")
    submit = st.form_submit_button("Generate")

vids = []

if submit:
    vids = auto_shorts.main.process_video(vid_url, 9)
    
# for vid in vids:
#     st.video(vid)

def download_vid(video: str, col):
    try:
        with open(video, "rb") as file:
            col.download_button(
                label="Download",
                data=file,
                file_name=os.path.basename(video),
            )
    except Exception as e:
        col.error(f"Error loading video : {str(e)}")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8, col9 = st.columns(3)
if vids:
    with col1:
        if len(vids) > 0:
            st.video(vids[0])
            download_vid(vids[0], col1)
    

    with col2:
        if len(vids) > 1:
            st.video(vids[1])
            download_vid(vids[1], col2)

    with col3:
        if len(vids) > 2:
            st.video(vids[2])
            download_vid(vids[2], col3)

    with col4:
        if len(vids) > 3:
            st.video(vids[3])
            download_vid(vids[3], col4)

    with col5:
        if len(vids) > 4:
            st.video(vids[4])
            download_vid(vids[4], col5)

    with col6:
        if len(vids) > 5:
            st.video(vids[5])
            download_vid(vids[5], col6)
        
    with col7:
        if len(vids) > 6:
            st.video(vids[6])
            download_vid(vids[6], col7)
        
    with col8:
        if len(vids) > 7:
            st.video(vids[7])
            download_vid(vids[7], col8)
        
    with col9:
        if len(vids) > 8:
            st.video(vids[8])
            download_vid(vids[8], col9)

        