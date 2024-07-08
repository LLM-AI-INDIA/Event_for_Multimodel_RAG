import streamlit as st
from openai import OpenAI
import time
import os
from streamlit_chat import message
import json
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

def Sql_agent(vAR_question):
    db = SQLDatabase.from_uri("mysql+pymysql://root:12345@35.188.163.239/otis_demo")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    text=agent_executor.invoke(vAR_question)
    return text['output']

def agent_with_calling(user_input):
    if 'client' not in st.session_state:
        st.session_state.client = OpenAI(api_key=os.environ["API_KEY"])
    if 'thread' not in st.session_state:
        st.session_state.thread = st.session_state.client.beta.threads.create()
    message = st.session_state.client.beta.threads.messages.create(thread_id=st.session_state.thread.id,role="user",content=user_input)
    run = st.session_state.client.beta.threads.runs.create(thread_id=st.session_state.thread.id,assistant_id="asst_ScYZ1DWxPcdi3jA5uOdQuY0h")
    
    while True:
        time.sleep(2)
        
        # Retrieve the run status
        run_status = st.session_state.client.beta.threads.runs.retrieve(thread_id=st.session_state.thread.id,run_id=run.id)
        
        print('run status - ',run_status.model_dump_json(indent=4))

        # If run is completed, get messages
        if run_status.status == 'completed':
            messages = st.session_state.client.beta.threads.messages.list(
                thread_id=st.session_state.thread.id
            )
            # Loop through messages and print content based on role
            for msg in messages.data:
                role = msg.role
                content = msg.content[0].text.value
                print(f"{role.capitalize()}: {content}")
                return content
        elif run_status.status == 'requires_action':
                print("Function Calling")
                required_actions = run_status.required_action.submit_tool_outputs.model_dump()
                print('required_actions - ',required_actions)
                tool_outputs = []
                for action in required_actions["tool_calls"]:
                    func_name = action['function']['name']
                    arguments = json.loads(action['function']['arguments'])
                    print("arguments - ",arguments)
                    
                    if func_name == "Sql_agent":
                        output = Sql_agent(arguments["vAR_question"])
                        
                        tool_outputs.append({
                            "tool_call_id": action['id'],
                            "output": output
                        })
                    else:
                        raise ValueError(f"Unknown function: {func_name}")
                    
                print("Submitting outputs back to the Assistant...")
                st.session_state.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=st.session_state.thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
        else:
            print("Waiting for the Assistant to process...")
            time.sleep(4)
