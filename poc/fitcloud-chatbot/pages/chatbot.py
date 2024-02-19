import streamlit as st
import boto3

# create agnet runtime
session = boto3.session.Session(region_name='us-east-1')
br_agnet_client = session.client(
    service_name='bedrock-agent-runtime'
)

# information for bedrock agent in us-east-1
agentId = "MARTXEGJPP"              # agennt id
agentAliasId='UUHTRMUTE6'           # alias id
sessionId  = "fitcloud"             # 임의로 정함

# account information
# accountId = st.session_state.accountId
# token = st.session_state.session_id                 # session id


st.set_page_config(initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("FitCloud Chatbot")

st.write("ssession id: ", st.session_state.session_id)
# # Display chat messages from history on app rerun 
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # React to user input
# if prompt := st.chat_input("What is up"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     with st.chat_message("assistant"):

#         response = resp = br_agnet_client.invoke_agent(
#                         sessionState = {
#                             'sessionAttributes': {
#                                 "token": token,
#                                 "accountId": accountId,
#                             },
#                         },
#                         agentId=agentId,
#                         agentAliasId=agentAliasId,
#                         sessionId=sessionId, 
#                         inputText=prompt  )

#     st.session_state.messages.append({"role": "assistant", "content": response})
