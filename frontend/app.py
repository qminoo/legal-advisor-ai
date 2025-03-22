import streamlit as st
from requests.exceptions import ConnectionError, Timeout, RequestException
from api import send_chat_request

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

    try:
        with st.spinner("Thinking..."):
            response = send_chat_request(user_input)

            if response.status_code == 200:
                ai_response = response.json()["response"]

                st.session_state.messages.append({"role": "assistant", "content": ai_response})

                with st.chat_message("assistant"):
                    st.markdown(ai_response)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
    except ConnectionError:
        st.error("Unable to connect to the backend server. Please ensure it is running.")
    except Timeout:
        st.error("The request timed out. Please try again later.")
    except RequestException as e:
        st.error(f"An error occurred: {str(e)}")  