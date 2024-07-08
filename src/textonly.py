import streamlit as st
from openai import OpenAI
import time
import os
from streamlit_chat import message
import json
from src.langchain_agent import agent_with_calling


def text_based():
    # Function to create a new thread
    # st.session_state.client = OpenAI(api_key=os.environ["API_KEY"])
    # def get_or_create_thread_id():
    #     if 'thread_id' not in st.session_state:
    #         thread = st.session_state.client.beta.threads.create()
    #         st.session_state.thread_id = thread.id
    #     return st.session_state.thread_id
    # thread_id = get_or_create_thread_id()

    ########################################### chatbot UI###############################################

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Greetings!. How can I help you?"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["We are delighted to have you here in the Live Agent Chat room!"]
    
    w1,c1,w2=st.columns([0.5,5.2,0.5])
    with c1:
        st.write("## ")
        #container for the chat history
        response_container = st.container()
    
        #container for the user's text input
        container = st.container()
        with container:
            with st.form(key='my_form', clear_on_submit=True):
                
                user_input = st.text_input("Prompt:", placeholder="How can I help you?", key='input')
                submit_button = st.form_submit_button(label='Interact with LLM')
                
            if submit_button and user_input:
                # messages_history.append(HumanMessage(content=user_input))
                vAR_response = agent_with_calling(user_input)                 
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(vAR_response)

        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                    message(st.session_state["generated"][i], key=str(i+55), avatar_style="thumbs")
    
    # w1,col1,col2,w2=st.columns([1,2,2.2,1])
    # w1,c1,w2=st.columns([1,4.2,1])
    # with col1:
    #     st.write("### ")
    #     st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Model Input</span></p>", unsafe_allow_html=True)
    # with col2:
    #     vAR_modelinput=st.text_input("", key="text_prompt")
    #     # vAR_modelinput = st.chat_input("Say something")
    # if vAR_modelinput:
    #     text=textmodel(vAR_modelinput)
    #     with c1:
    #         st.write("")
    #         st.success(text)


# def textmodel(vAR_modelinput,thread_id):
#     client = OpenAI(api_key=os.environ["API_KEY"])
#     # thread = client.beta.threads.create()
#     message = client.beta.threads.messages.create(thread_id=thread_id,role="user",content=vAR_modelinput)
#     run = client.beta.threads.runs.create(thread_id=thread_id,assistant_id="asst_ScYZ1DWxPcdi3jA5uOdQuY0h")
#     while True:
#         time.sleep(2)
        
#         # Retrieve the run status
#         run_status = st.session_state.client.beta.threads.runs.retrieve(thread_id=st.session_state.thread.id,run_id=run.id)
        
#         print('run status - ',run_status.model_dump_json(indent=4))

#         # If run is completed, get messages
#         if run_status.status == 'completed':
#             messages = st.session_state.client.beta.threads.messages.list(
#                 thread_id=thread_id
#             )
#             # Loop through messages and print content based on role
#             for msg in messages.data:
#                 role = msg.role
#                 content = msg.content[0].text.value
#                 print(f"{role.capitalize()}: {content}")
#                 return content
#         elif run_status.status == 'requires_action':
#                 print("Function Calling")
#                 required_actions = run_status.required_action.submit_tool_outputs.model_dump()
#                 print('required_actions - ',required_actions)
#                 tool_outputs = []
#                 for action in required_actions["tool_calls"]:
#                     func_name = action['function']['name']
#                     arguments = json.loads(action['function']['arguments'])
#                     print("arguments - ",arguments)
                    
#                     if func_name == "Sql_agent":
#                         output = Sql_agent(arguments["vAR_qestion"])
                        
#                         tool_outputs.append({
#                             "tool_call_id": action['id'],
#                             "output": output
#                         })
#                     else:
#                         raise ValueError(f"Unknown function: {func_name}")
                    
#                 print("Submitting outputs back to the Assistant...")
#                 st.session_state.client.beta.threads.runs.submit_tool_outputs(
#                     thread_id=thread_id,
#                     run_id=run.id,
#                     tool_outputs=tool_outputs
#                 )
#         else:
#             print("Waiting for the Assistant to process...")
#             time.sleep(5)
    

# def voicemodel(vAR_modelinput):
#     client = OpenAI(api_key=os.environ["API_KEY"])
#     thread = client.beta.threads.create()
#     message = client.beta.threads.messages.create(thread_id=thread.id,role="user",content=vAR_modelinput)
#     run = client.beta.threads.runs.create(thread_id=thread.id,assistant_id="asst_ScYZ1DWxPcdi3jA5uOdQuY0h")
#     while True:
#         run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
#         time.sleep(2)
#         if run.status=="completed":
#             messages = client.beta.threads.messages.list(thread_id=thread.id)
#             latest_message = messages.data[0]
#             text = latest_message.content[0].text.value
#             return text
        