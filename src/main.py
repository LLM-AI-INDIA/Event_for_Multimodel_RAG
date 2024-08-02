import streamlit as st
from src.textonly import text_based
from src.voice import voice_based
from src.imagewithtext import image_based
from src.memory import memory_chat
from src.chain import chain_chat
from src.callback import callback_chat

def main_ui():
    w1,col1,col2,w2=st.columns([0.8,2.5,2.7,0.5])
    with col1:
        st.write("### ")
        st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Knowledge base</span></p>", unsafe_allow_html=True)
    with col2:
        vAR_kb=st.radio("",["Database", "Langchain", "Catalog(PDF)"], horizontal=True,key="kb_input")
    if vAR_kb=="Database":
        text_based()

    if vAR_kb== "Langchain":
        with col1:
            st.write("### ")
            st.write("")
            
            st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Select Functions</span></p>", unsafe_allow_html=True)
        with col2:
            # st.write("")
            vAR_mit=st.selectbox("",["Select","Memory","Chain","Callbacks"],key="mit")
        if vAR_mit == "Chain":
            chain_chat()
        if vAR_mit == "Memory":
            memory_chat()
        if vAR_mit == "Callbacks":
            callback_chat()
                
    
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
        