import streamlit as st
from api import chat, get_chat_history, get_all_sessions

st.set_page_config(page_title="Legal Advisor AI", page_icon="⚖️")

st.title("Legal Advisor AI")

if "session_id" not in st.session_state:
    st.session_state.session_id = None
    st.session_state.messages = []

def fetch_and_validate_sessions():
    """Fetch sessions and validate the response structure."""
    response = get_all_sessions()
    sessions = response.get("sessions")  # Use get to avoid KeyError
    if not isinstance(sessions, list):
        raise ValueError(f"Expected 'sessions' to be a list, got {type(sessions).__name__} instead.")
    return sessions

# Sidebar for session management
with st.sidebar:
    if st.button("New Chat"):
        st.session_state.session_id = None
        st.session_state.messages = []
        st.rerun()

    st.write("Previous Sessions:")
    try:
        sessions = fetch_and_validate_sessions()
        formatted_sessions = {
            f"Session {s['id']} ({s['created_at'][:16]})": s['id']
            for s in sessions
        }
        selected = st.selectbox(
            "Select a session",
            options=list(formatted_sessions.keys()),
            index=None,
            placeholder="Choose a previous session..."
        )
        if selected and formatted_sessions[selected] != st.session_state.session_id:
            st.session_state.session_id = formatted_sessions[selected]
            st.rerun()
    except Exception as e:
        st.error(f"Failed to load sessions: {str(e)}")
        print(f"Debug - Error details: {str(e)}")

# Load current session's chat history
if st.session_state.session_id is not None:
    try:
        print(f"Loading chat history for session {st.session_state.session_id}")
        response = get_chat_history(st.session_state.session_id)
        messages = response["messages"]
        st.session_state.messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in messages
        ]
    except Exception as e:
        st.error(f"Failed to load chat history: {str(e)}")
        print(f"Debug - Chat history error: {str(e)}")

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
            
            # Update session_id if this is a new conversation
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