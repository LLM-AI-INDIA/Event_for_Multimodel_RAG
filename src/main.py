import streamlit as st
from src.textonly import text_based
from src.voice import voice_based
from src.imagewithtext import image_based

def main_ui():
    w1,col1,col2,w2=st.columns([0.8,2.5,2.7,0.5])
    with col1:
        st.write("### ")
        st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Knowledge base</span></p>", unsafe_allow_html=True)
    with col2:
        vAR_kb=st.radio("",["Database", "Web", "Catalog(PDF)"], horizontal=True,key="kb_input")
    if vAR_kb=="Database":
        text_based()

    if vAR_kb== "Web":
        with col1:
            st.write("### ")
            st.write("")
            
            st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Database/web link</span></p>", unsafe_allow_html=True)
        with col2:
            # st.write("")
            vAR_mit=st.text_input("",key="mit")
    
    if vAR_kb== "Catalog(PDF)":
        with col1:
            st.write("### ")
            st.write("### ")
            st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Model Input Type</span></p>", unsafe_allow_html=True)
        with col2:
            st.write("")
            vAR_mit=st.selectbox("",["Select", "Text", "Voice", "Image"],key="mit")
        if vAR_mit=="Text":
            text_based()
        elif vAR_mit == "Voice":
            voice_based()
        elif vAR_mit == "Image":
            image_based()
        else:
            pass
        