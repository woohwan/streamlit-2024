import streamlit as st
import boto3

# langchain
from langchain.chains import ConversationChain
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import BaseCallbackHandler

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
    )
    model = ConversationChain(llm=llm, verbose=False, memory=ConversationBufferMemory())
    return model

# https://github.com/davidshtian/Bedrock-ChatBot-with-LangChain-and-Streamlit/tree/hand
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

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

        response = model.run(input=prompt, callbacks=[StreamHandler(st.empty())])

    st.session_state.messages.append({"role": "assistant", "content": response})

    