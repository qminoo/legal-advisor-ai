import streamlit as st

st.set_page_config(page_title="Legal Advisor AI", page_icon="⚖️")

st.title("Legal Advisor AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask your legal question...")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        

    with st.chat_message("assistant"):
        st.markdown("This feature will be implemented soon!") 