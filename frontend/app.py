import streamlit as st
from api import chat, get_chat_history, get_all_sessions
from datetime import datetime

st.set_page_config(page_title="Legal Advisor AI", page_icon="⚖️")

st.title("Legal Advisor AI")

if "session_id" not in st.session_state:
    st.session_state.session_id = None
    st.session_state.messages = []
    st.session_state.loading_session = False
    st.session_state.session_to_load = None

input_disabled = st.session_state.get("loading_session", False)

def fetch_and_validate_sessions():
    """Fetch sessions and validate the response structure."""
    response = get_all_sessions()
    sessions = response.get("sessions")  # Use get to avoid KeyError
    if not isinstance(sessions, list):
        raise ValueError(f"Expected 'sessions' to be a list, got {type(sessions).__name__} instead.")
    return sessions

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask a legal question:", disabled=input_disabled):
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
                new_session_id = response["session_id"]
                st.session_state.session_id = new_session_id
                
                if "formatted_sessions" in st.session_state:
                    created_at = response["created_at"][:16]
                    new_session_key = f"Session {new_session_id} ({created_at})"        
                    new_sessions_dict = {new_session_key: new_session_id}
                    new_sessions_dict.update(st.session_state.formatted_sessions)
                    st.session_state.formatted_sessions = new_sessions_dict
                    st.session_state.selected_session = new_session_key
            
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
        
with st.sidebar:
    if st.button("New Chat"):
        st.session_state.session_id = None
        st.session_state.messages = []
        st.session_state.loading_session = False
        if "selected_session" in st.session_state:
            st.session_state.selected_session = None
        st.rerun()

    st.write("Previous Sessions:")
    
    if "formatted_sessions" not in st.session_state:
        try:
            with st.spinner("Loading previous sessions..."):
                sessions = fetch_and_validate_sessions()
                st.session_state.formatted_sessions = {
                    f"Session {s['id']} ({s['created_at'][:16]})": s['id']
                    for s in sessions
                }
        except Exception as e:
            st.error(f"Failed to load sessions: {str(e)}")
            print(f"Debug - Error details: {str(e)}")
    
    selected = st.selectbox(
        "Select a session",
        label_visibility="hidden",
        options=list(st.session_state.formatted_sessions.keys()),
        index=None,
        key="selected_session",
        placeholder="Choose a previous session..."
    )
    
    if selected:
        new_session_id = st.session_state.formatted_sessions[selected]
        
        if st.session_state.get("loading_session") and st.session_state.get("session_to_load") == new_session_id:
            with st.spinner("Loading chat history..."):
                try:
                    response = get_chat_history(st.session_state.session_id)
                    messages = response["messages"]
                    st.session_state.messages = [
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in messages
                    ]
                    st.session_state.loading_session = False
                    st.session_state.session_to_load = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to load chat history: {str(e)}")
                    print(f"Debug - Chat history error: {str(e)}")
                    st.session_state.loading_session = False
                    st.session_state.session_to_load = None
        
        elif new_session_id != st.session_state.session_id:
            st.session_state.session_id = new_session_id
            st.session_state.loading_session = True
            st.session_state.session_to_load = new_session_id
            st.rerun()