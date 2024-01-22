import streamlit as st

"st.session_stae object: ",  st.session_state

if 'a_counter' not in st.session_state:
    st.session_state['a_counter'] = 0

if "boolean" not in st.session_state:
    st.session_state.boolean = False

st.write(st.session_state)