import streamlit as st
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder
import os,time

def voice_based():
    w1,col1,col2,w2=st.columns([0.8,2.5,2.7,0.5])
    w1,c1,w2=st.columns([1,4.2,1])
    with col1:
        st.write("## ")
        st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Voice Input Type</span></p>", unsafe_allow_html=True)
    with col2:
        # st.write("")
        vAR_voice_type=st.selectbox("",["Select","Audio uploader","Live Record"])
    if vAR_voice_type=="Live Record":
        with col1:
            st.write("### ")
            st.write("")
            st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Model Input</span></p>", unsafe_allow_html=True)
        with col2:
            st.write("# ")
            audio_bytes = audio_recorder(" ",icon_size="2x")
            # Include the JavaScript
            st.markdown("""
                <script>
                function triggerResize() {
                    window.dispatchEvent(new Event('resize'));
                }

                window.onload = triggerResize;
                </script>
            """, unsafe_allow_html=True)
            if audio_bytes:
                with open('result/file.wav', "wb") as f:
                    f.write(audio_bytes)
                with c1:
                    st.audio(audio_bytes, format="audio/wav")
                st.write("")
                if st.button("Submit"):
                    client = OpenAI(api_key=os.environ["API_KEY"])
                    filepath="result/file.wav"
                    audio_file= open(filepath, "rb")
                    transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
        )
                    text_fm_voice= transcription.text
                    with c1:
                        st.info(text_fm_voice)
                    result=voicemodel(text_fm_voice)
                    with c1:
                        st.write("")
                        st.success(result)
                    # os.remove(filepath)

    if vAR_voice_type=="Audio uploader":
        w1,col3,col4,w2=st.columns([0.8,2.5,2.7,0.5])
        w1,c2,w2=st.columns([1,4.2,1])
        with col3:
            st.write("### ")
            st.write("### ")
            st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Model Input Type</span></p>", unsafe_allow_html=True)
        with col4:
            # st.write("# ")
            vAR_audio_upload=st.file_uploader("", type=["wav", "mp3", "m4a"])
            if vAR_audio_upload is not None:
                # Set the directory where the MP3 files will be saved
                SAVE_DIRECTORY = "result"

                # Create the directory if it doesn't exist
                if not os.path.exists(SAVE_DIRECTORY):
                    os.makedirs(SAVE_DIRECTORY)
                # Save the uploaded file to the designated directory
                file_path = os.path.join(SAVE_DIRECTORY, vAR_audio_upload.name)
                with open(file_path, "wb") as f:
                    f.write(vAR_audio_upload.getbuffer())
                st.write("")
                if st.button("Submit"):
                    client = OpenAI(api_key=os.environ["API_KEY"])
                    audio_file= open(file_path, "rb")
                    transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
        )
                    text_fm_voice= transcription.text
                    with c2:
                        st.info(text_fm_voice)
                    result=voicemodel(text_fm_voice)
                    with c2:
                        st.write("")
                        st.success(result)
                    # os.remove(file_path)

def voicemodel(vAR_modelinput):
    client = OpenAI(api_key=os.environ["API_KEY"])
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(thread_id=thread.id,role="user",content=vAR_modelinput)
    run = client.beta.threads.runs.create(thread_id=thread.id,assistant_id="asst_ScYZ1DWxPcdi3jA5uOdQuY0h")
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(2)
        if run.status=="completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            return text