import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI
# from langchain.llms import OpenAI
import os


def chain_chat():
    w1,col1,col2,w2=st.columns([0.8,2.5,2.7,0.5])
    w1,c1,w2=st.columns([0.8,5.2,0.5])
    w1,col3,col4,w2=st.columns([0.8,2.5,2.7,0.5])
    w1,c2,w2=st.columns([0.8,5.2,0.5])

    # Use API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        st.error("API key not found. Please set the OPENAI_API_KEY environment variable.")
    else:
        llm = OpenAI(api_key=api_key)
    with col1:
        st.write("## ")
        st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Select the type of chaining</span></p>", unsafe_allow_html=True)
    with col2:

        # Add a select box to choose between basic and advanced chaining
        chain_type = st.selectbox('', ['Select','Basic Prompt Chaining', 'Advanced Prompt Chaining'])

    if chain_type == 'Basic Prompt Chaining':
        # st.subheader('Basic Prompt Chaining')
        with c1:
            st.write("## ")
            # Showcase Prompt Template
            st.write("**Prompt Template for Basic Prompt Chaining:**")
            st.code("What are some interesting facts about {name}?", language="plain")

            # Explain the prompt template
            st.write("This prompt template takes a 'name' as input and generates interesting facts about the given name.")

        # Define and demonstrate the chain
        prompt_template = PromptTemplate(
            input_variables=["name"],
            template="What are 6 to 7 interesting facts about {name}?"
        )

        chain = LLMChain(llm=llm, prompt=prompt_template)
        with col3:
            st.write("## ")
            st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Enter a name to learn interesting facts</span></p>", unsafe_allow_html=True)
        with col4:
            name_input = st.text_input('', key='name_input')
        if name_input:
            result = chain.run({"name": name_input})
            with c2:
                st.success(result)

    elif chain_type == 'Advanced Prompt Chaining':
        # st.subheader('Advanced Prompt Chaining')
        with c1:
            st.write("## ")
            # Showcase Prompt Templates
            st.write("**Prompt Template 1 for Advanced Prompt Chaining:**")
            st.code("Provide a brief biography of {person}.", language="plain")

            st.write("**Prompt Template 2 for Advanced Prompt Chaining:**")
            st.code("List some achievements of the following person based on their biography: {biography}.", language="plain")

            st.write("**Prompt Template 3 for Advanced Prompt Chaining:**")
            st.code("Extract the top-ranked achievement from the following list of achievements: {achievements}.", language="plain")

            # Explain the prompt templates
            st.write("""
            The first prompt template takes a 'person' as input and generates a brief biography about the given person.
            The second prompt template takes the generated biography as input and extracts key achievements from it.
            The third prompt template takes the list of achievements as input and extracts the top-ranked achievement.
            """)

        # Define the chains
        prompt_template1 = PromptTemplate(
            input_variables=["person"],
            template="Provide a brief biography of {person}."
        )

        prompt_template2 = PromptTemplate(
            input_variables=["biography"],
            template="List some achievements of the following person based on their biography: {biography}."
        )
        
        prompt_template3 = PromptTemplate(
            input_variables=["achievements"],
            template="Extract the top-ranked achievement from the following list of achievements: {achievements}."
        )

        chain1 = LLMChain(llm=llm, prompt=prompt_template1)
        chain2 = LLMChain(llm=llm, prompt=prompt_template2)
        chain3 = LLMChain(llm=llm, prompt=prompt_template3)

        with col3:
            st.write("## ")
            st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Enter the name of a well-known person</span></p>", unsafe_allow_html=True)
        with col4:
            person_input = st.text_input('', key='person_input')
        with col4:
            st.write("")
            if person_input and st.button('Generate'):
                # Run the first chain to get the biography
                biography = chain1.run({"person": person_input})
                with c2:
                    st.write("**Biography:**")
                    st.write(biography)

                # Run the second chain to get the achievements using the biography
                achievements = chain2.run({"biography": biography})
                with c2:
                    st.write("**Achievements:**")
                    st.write(achievements)

                # Run the third chain to get the top-ranked achievement using the achievements list
                top_ranked_achievement = chain3.run({"achievements": achievements})
                with c2:
                    st.write("**Top-Ranked Achievement:**")
                    st.write(top_ranked_achievement)