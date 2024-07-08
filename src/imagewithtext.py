import streamlit as st
from openai import OpenAI
import os,time
from PIL import Image

def image_based():
    w1,col1,col2,w2=st.columns([0.8,2.5,2.7,0.5])
    w1,c1,w2=st.columns([3,4.2,1])
    w1,col3,col4,w2=st.columns([0.8,2.5,2.7,0.5])
    w1,c2,w2=st.columns([1,4.2,1])
    with col1:
        st.write("### ")
        st.write("### ")
        st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Model Input</span></p>", unsafe_allow_html=True)
    with col2:
        # st.write("# ")
        vAR_img_upload=st.file_uploader("", type=["jpg", "png", "jpeg"])
    if vAR_img_upload is not None:
        image = Image.open(vAR_img_upload)
        resized_image = image.resize((300, 300))
        with c1:
            st.image(resized_image, caption='Uploaded Image')
        # Set the directory where you want to save the uploaded images
        save_directory = "uploaded_images"

        # Create the directory if it does not exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Save the image to the specified directory
        file_path = os.path.join(save_directory, vAR_img_upload.name)
        with open(file_path, "wb") as f:
            f.write(vAR_img_upload.getbuffer())

        with col3:
            st.write("## ")
            # st.write("### ")
            st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Prompt with Image</span></p>", unsafe_allow_html=True)
        with col4:
            # st.write("# ")
            vAR_text_wth_img=st.text_input("")
            st.write("")
            if st.button("Submit"):
                response = textmodel_with_file(vAR_text_wth_img, file_path)
                with c2:
                    st.write("")
                    st.success(response)
                # os.remove(file_path)


def textmodel_with_file(user_input, file_path):
    client = OpenAI(api_key=os.environ["API_KEY"])
    ASSISTANT_ID = 'asst_ScYZ1DWxPcdi3jA5uOdQuY0h'
    # Upload the file
    with open(file_path, "rb") as file:
        message_file = client.files.create(file=file, purpose='vision')
    file_id = message_file.id  # Correct way to access the file ID
    
    thread = client.beta.threads.create(
        messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": user_input
        },
        {
          "type": "image_file",
          "image_file": {"file_id": message_file.id}
        },
      ]
    }
  ]
)


    # Run the assistant
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

    # Polling for the completion of the run
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(2)
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            return text
        elif run.status == "failed":
            return "Currently, the service is not available. Please try again later."
        else:
            pass
