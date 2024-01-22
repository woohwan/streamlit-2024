import time

import streamlit as st
import boto3

# langchain
from langchain.chains import ConversationChain
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory

# streaming
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

st.title(" Bedrock Chatbot")

# set up boto3
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)


# Initailize Amazon Bedrock with LangChain
@st.cache_resource
def load_llm():
    llm = Bedrock(
        client=bedrock_runtime,
        model_id='anthropic.claude-v2:1',
        model_kwargs={
            "max_tokens_to_sample": 2048,
            "temperature": 0.7
        },
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()]
    )
    model = ConversationChain(llm=llm, verbose=True, memory=ConversationBufferMemory())
    return model

model = load_llm()

# chat history 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        result = model.predict(input=prompt)

        # Simulate stream of response with msecs delay
        for chunk in result.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + " ")
        
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

    