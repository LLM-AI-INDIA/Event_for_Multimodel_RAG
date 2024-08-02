import streamlit as st
from PIL import Image
import os
from openai import OpenAI
from src.main import main_ui

st.set_page_config(layout="wide")
# Adding (css)stye to application
with open('style/final.css') as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
    
st.markdown("<p style='text-align: center; color: black;margin-top: -10px ;font-size:40px;'><span style='font-weight: bold'>Generative AI-powered Conversational Q&A Platform </span></p>", unsafe_allow_html=True)
# Adding company logo
imcol1, imcol2, imcol3= st.columns((4,3.5,4.5))

# with imcol2:
#     st.write("## ")
#     st.image('image/deeplogo.png')
with imcol2:
    st.image('image/default_logo.png')   

# st.markdown("<p style='text-align: center; color: black; font-size:25px; margin-top: -30px'><span style='font-weight: bold'></span>Interact with our RAG bot powered by LLM with text, image, and voice </p>", unsafe_allow_html=True)
st.write("")

# st.markdown("<hr style=height:2.5px;margin-top:0px;width:80%;background-color:gray;>",unsafe_allow_html=True)
st.markdown("<hr style='height:2.5px; margin-top:0px; width:80%; background-color:gray; margin-left:auto; margin-right:auto;'>", unsafe_allow_html=True)



#---------Side bar-------#
with st.sidebar:
    st.markdown("<p style='text-align: center; color: white; font-size:25px;'><span style='font-weight: bold; font-family: century-gothic';></span>Solutions Scope</p>", unsafe_allow_html=True)
    vAR_AI_application = st.selectbox("",['Home','Conversational Q&A'],key='application')
    # selected = st.selectbox("",['User',"Logout"],key='text')
    vAR_LLM_model = st.selectbox("",['LLM Models',"gpt-4o","gpt-3.5-turbo-16k-0613","gpt-4-0314","gpt-3.5-turbo-1106"],key='text_llmmodel')
    # vAR_LLM_framework = st.selectbox("",['LLM Framework',"Langchain"],key='text_framework')

    vAR_Library = st.selectbox("",
                    ["Library Used","Streamlit","Image","Pandas","openAI"],key='text1')
    vAR_Gcp_cloud = st.selectbox("",
                    ["GCP Services Used","VM Instance","Computer Engine","Cloud Storage"],key='text2')
    st.markdown("#### ")
    href = """<form action="#">
            <input type="submit" value="Clear/Reset"/>
            </form>"""
    st.sidebar.markdown(href, unsafe_allow_html=True)
    st.markdown("# ")
    st.markdown("<p style='text-align: center; color: White; font-size:20px;'>Build & Deployed on<span style='font-weight: bold'></span></p>", unsafe_allow_html=True)
    s1,s2=st.columns((2,2))
    with s1:
        st.markdown("### ")
        st.image('image/aws_logo.png')
    with s2:    
        st.markdown("### ")
        st.image("image/oie_png.png")

if vAR_AI_application == 'Conversational Q&A':
    main_ui()
    # Function to create a new thread
    # client = OpenAI(api_key=os.environ["API_KEY"])
    # def get_or_create_thread_id():
    #     if 'thread_id' not in st.session_state:
    #         thread = client.beta.threads.create()
    #         st.session_state.thread_id = thread.id
    #     return st.session_state.thread_id

    # # Call the function to get or create the thread_id when the app starts
    # thread_id = get_or_create_thread_id()
    
    