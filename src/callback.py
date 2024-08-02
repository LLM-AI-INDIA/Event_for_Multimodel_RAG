import streamlit as st
import pandas as pd
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
import time
import warnings

# Ignore warnings
warnings.filterwarnings('ignore')


def callback_chat():
    w1,col1,col2,w2=st.columns([0.8,2.5,2.7,0.5])
    w1,c1,w2=st.columns([0.8,5.2,0.5])
    w1,col3,col4,w2=st.columns([0.8,2.5,2.7,0.5])
    w1,c2,w2=st.columns([0.8,5.2,0.5])
    # Custom CallbackHandler to capture logs
    class StreamlitCallbackHandler(BaseCallbackHandler):
        def __init__(self):
            self.logs = []

        def on_chain_start(self, serialized, inputs, **kwargs):
            self.logs.append({"Event": "Chain Start", "Details": str(inputs)})

        def on_chain_end(self, outputs, **kwargs):
            self.logs.append({"Event": "Chain End", "Details": str(outputs)})

        def on_llm_start(self, serialized, prompts, **kwargs):
            self.logs.append({"Event": "LLM Start", "Details": str(prompts)})

        def on_llm_end(self, response, **kwargs):
            self.logs.append({"Event": "LLM End", "Details": str(response)})

        def on_llm_new_token(self, token: str, **kwargs):
            self.logs.append({"Event": "New Token", "Details": token})

        def on_llm_error(self, error, **kwargs):
            self.logs.append({"Event": "LLM Error", "Details": str(error)})

        def on_chain_error(self, error, **kwargs):
            self.logs.append({"Event": "Chain Error", "Details": str(error)})
    # Simulate token-by-token processing
    def simulate_token_generation(text, callback_handler):
        tokens = text.split()
        response = ""
        for token in tokens:
            time.sleep(0.1)  # Simulate delay
            response += token + " "
            callback_handler.on_llm_new_token(token)
        return response.strip()
    
    # Initialize the callback handler
    handler = StreamlitCallbackHandler()

    # Define the OpenAI LLM
    api_key = os.getenv('OPENAI_API_KEY')
    llm = OpenAI(api_key=api_key)

    # Define the prompt template
    prompt = PromptTemplate.from_template("Please write a very short story about {input_text} in 200 words.")

    # Initialize the LLMChain with the callback handler
    chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])

    with c1:
        st.write("## ")
        # Showcase Prompt Template
        st.write("**Prompt Template for Prompt Chaining:**")
        st.code("write a story about {input_text}.", language="plain")
    with col3:
        st.write("## ")
        st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Enter text/topic for the story</span></p>", unsafe_allow_html=True)
    with col4:
        # st.title("LangChain Callback Demo")
        input_text = st.text_input("", value="a robot learning to dance")
    with col4:
        if st.button("Submit"):
            handler.logs.clear()
            try:
                handler.on_llm_start(serialized={}, prompts=[input_text])
                result = chain.invoke({"input_text": input_text})
                handler.on_llm_end(response=result)

                simulated_response = simulate_token_generation(result['text'], handler)
                with c2:
                    st.success(simulated_response)
            except Exception as e:
                handler.on_chain_error(error=str(e))
                st.write("An error occurred:", e)
            with c2:
                st.write("Logs:")
                logs_df = pd.DataFrame(handler.logs)
                st.dataframe(logs_df)