import streamlit as st
from api import chat, get_chat_history

st.set_page_config(page_title="Legal Advisor AI", page_icon="⚖️")

st.title("Legal Advisor AI")

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask a legal question:"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        with st.spinner("Thinking..."):
            response = chat(
                message=user_input,
                session_id=st.session_state.session_id
            )
            
            if not st.session_state.session_id and "session_id" in response:
                st.session_state.session_id = response["session_id"]
            
            if "response" in response:
                assistant_message = {"role": "assistant", "content": response["response"]}
                st.session_state.messages.append(assistant_message)
                with st.chat_message("assistant"):
                    st.markdown(response["response"])
            else:
                st.error("Invalid response format from API")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        print(f"Debug - Error details: {str(e)}")  