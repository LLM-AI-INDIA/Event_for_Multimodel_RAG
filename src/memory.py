import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


def memory_chat():
    w1,col3,w2=st.columns([0.8,5.2,0.5])
    # Initialize the chat model
    chat = ChatOpenAI(model="gpt-3.5-turbo-0125")

    # Session state to store message history and current AI response
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
    if "current_response" not in st.session_state:
        st.session_state.current_response = ""
    
    with col3:
        st.write("")
        st.subheader("Chat with AI")

        st.write(st.session_state.messages)
        # User input
        user_input = st.text_input("Your Prompt: ")

        if st.button("Send"):
            if user_input:
                # Append human message to the session state
                st.session_state.messages.append(HumanMessage(content=user_input))

                # Get AI response
                response = chat.invoke(st.session_state.messages)
                
                # Append AI message to the session state
                st.session_state.messages.append(AIMessage(content=response.content))

                # Store current response separately
                st.session_state.current_response = response.content

                # Rerun to display the updated chat history
                st.experimental_rerun()

        # Display current AI response below the button
        if st.session_state.current_response:
            st.write("Current AI response:")
            st.success(st.session_state.current_response)