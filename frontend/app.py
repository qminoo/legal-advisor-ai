import streamlit as st
from api import send_chat_message, get_chat_history, get_sessions

def init_session_state():
    """Initialize session state variables if they don't exist."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
        st.session_state.messages = []
        st.session_state.loading_session = False
        st.session_state.session_to_load = None
    if "formatted_sessions" not in st.session_state:
        st.session_state.formatted_sessions = {}
    if "sessions_loaded" not in st.session_state:
        st.session_state.sessions_loaded = False
    if "history_loaded" not in st.session_state:
        st.session_state.history_loaded = False

def display_chat_history():
    """Display existing chat messages."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def add_new_session_to_list(session_id, created_at):
    """Add a newly created session to the sessions list."""
    if "formatted_sessions" in st.session_state:
        created_at_str = created_at[:16]
        new_session_key = f"Session {session_id} ({created_at_str})"        
        new_sessions_dict = {new_session_key: session_id}
        new_sessions_dict.update(st.session_state.formatted_sessions)
        st.session_state.formatted_sessions = new_sessions_dict
        st.session_state.selected_session = new_session_key
      
def handle_session_creation(response):
    if not st.session_state.session_id and "session_id" in response:
        new_session_id = response["session_id"]
        st.session_state.session_id = new_session_id
                
        if "created_at" in response:
            add_new_session_to_list(new_session_id, response["created_at"])

def display_assistant_response(response):
    if "response" in response:
        assistant_message = {"role": "assistant", "content": response["response"]}
        st.session_state.messages.append(assistant_message)
        with st.chat_message("assistant"):
            st.markdown(response["response"])
    else:
        st.error("Invalid response format from API")

def handle_new_message(user_message):
    """Process a new user message and get AI response."""
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    try:
        with st.spinner("Thinking..."):
            response = send_chat_message(
                message=user_message,
                session_id=st.session_state.session_id
            )
            
            handle_session_creation(response)
            display_assistant_response(response)
    except Exception as e:
        st.error(f"Error: {str(e)}")

def start_new_chat():
    """Reset the UI for a new chat session."""
    st.session_state.session_id = None
    st.session_state.messages = []
    st.session_state.loading_session = False
    st.session_state.history_loaded = False
    if "selected_session" in st.session_state:
        st.session_state.selected_session = None
    st.rerun()

def fetch_and_validate_sessions():
    """Fetch sessions and validate the response structure."""
    response = get_sessions()
    sessions = response.get("sessions", [])
    return sessions

def format_sessions_for_display(sessions):
    """Format sessions for display in the select box."""
    return {
        f"Session {s['id']} ({s['created_at'][:16]})": s['id']
        for s in sessions
    }

def load_sessions():
    """Load chat sessions from the API."""
    if not st.session_state.sessions_loaded:
        try:
            with st.spinner("Loading previous sessions..."):
                sessions = fetch_and_validate_sessions()
                formatted_sessions = format_sessions_for_display(sessions)
                
                st.session_state.formatted_sessions = formatted_sessions
                st.session_state.sessions_loaded = True
        except Exception as e:
            st.error(f"Failed to load sessions: {str(e)}")

def load_chat_history(session_id):
    """Load chat history for the selected session."""
    if not st.session_state.history_loaded:
        with st.spinner("Loading chat history..."):
            try:
                response = get_chat_history(session_id)
                messages = response["messages"]
                st.session_state.messages = [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in messages
                ]
                st.session_state.loading_session = False
                st.session_state.session_to_load = None
                # Mark history as loaded
                st.session_state.history_loaded = True
            except Exception as e:
                st.error(f"Failed to load chat history: {str(e)}")
                st.session_state.loading_session = False
                st.session_state.session_to_load = None

def handle_session_selection(selected):
    """Process when a user selects a different chat session."""
    if selected:
        new_session_id = st.session_state.formatted_sessions[selected]
        
        if new_session_id != st.session_state.session_id:
            st.session_state.history_loaded = False
            st.session_state.session_id = new_session_id
            st.session_state.loading_session = True
            st.session_state.session_to_load = new_session_id
            
            if not st.session_state.history_loaded:
                st.rerun()

def main():
    """Main application function."""
    st.set_page_config(page_title="Legal Advisor AI", page_icon="⚖️")
    st.title("Legal Advisor AI")
    
    init_session_state()
    load_sessions()
    
    if st.session_state.session_id and st.session_state.loading_session and not st.session_state.history_loaded:
        load_chat_history(st.session_state.session_id)
    
    input_disabled = st.session_state.get("loading_session", False)
    
    display_chat_history()
    
    # Chat input
    if user_input := st.chat_input("Ask a legal question:", disabled=input_disabled):
        handle_new_message(user_input)
    
    # Sidebar
    with st.sidebar:
        if st.button("New Chat"):
            start_new_chat()

        st.write("Previous Sessions:")
        
        # Session selector
        selected = st.selectbox(
            "Select a session",
            label_visibility="hidden",
            options=list(st.session_state.formatted_sessions.keys()),
            index=None,
            key="selected_session",
            placeholder="Choose a previous session..."
        )
        
        handle_session_selection(selected)

if __name__ == "__main__":
    main()