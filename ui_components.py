import streamlit as st

def render_sidebar():
    st.sidebar.title("🤖 Chatbot Settings")
    selected_model = st.sidebar.selectbox(
        "Choose AI Model", ("Ollama"),
        help="Select the AI model you want to chat with."
    )

    with st.sidebar.expander("Advanced Settings"):
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05, help="Controls randomness. Lower is more deterministic.")
        max_tokens = st.number_input("Max Tokens", min_value=50, max_value=4096, value=1024, help="Maximum number of tokens to generate.")
        top_p = st.slider("Top-P", 0.0, 1.0, 0.9, 0.05, help="Controls nucleus sampling.")
        top_k = st.number_input("Top-K", min_value=1, value=40, help="Considers the top k tokens (Gemini only).") if selected_model == "Gemini" else None

    summarize_button = st.sidebar.button("Summarize Conversation", key="summarize")
    
    return selected_model, temperature, max_tokens, top_p, top_k, summarize_button

def render_chat_interface():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    return st.chat_input("What is up?")
