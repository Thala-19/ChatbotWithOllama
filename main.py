import streamlit as st
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import HumanMessage, AIMessage
from ui_components import render_sidebar


@st.cache_resource
def get_ollama_model(model_name="llama3"):
    try:
        llm = Ollama(model=model_name)
        llm.invoke("Hi") 
        return llm
    except Exception as e:
        st.error(f"Failed to connect to Ollama. Error: {e}")
        return None

class OllamaChatbot:
    def __init__(self, model_name="llama3"):
        self.llm = get_ollama_model(model_name)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer all questions to the best of your ability."),
            MessagesPlaceholder(variable_name="messages"),
        ])
        if self.llm:
            self.chain = self.prompt_template | self.llm

    def get_response(self, prompt, chat_history):
        if not self.llm:
            return "Ollama model is not available. Cannot get a response."
        try:
            messages = [HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"]) for msg in chat_history]
            messages.append(HumanMessage(content=prompt))
            response = self.chain.invoke({"messages": messages})
            return response.strip()
        except Exception as e:
            return f"An error occurred while getting a response from Ollama: {e}"

    def summarize_conversation(self, chat_history):
        if not chat_history:
            return "No conversation to summarize."
        full_conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
        summary_prompt = f"Please summarize the following conversation concisely:\n\n{full_conversation}\n\nSummary:"
        return self.get_response(summary_prompt, [])


def main():
    st.set_page_config(page_title="Chat with Ollama", page_icon="🦙")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("Chat with Ollama 🦙")

    chatbot = OllamaChatbot() 

    if st.session_state.get("summarize_request", False):
        if st.session_state.messages:
            with st.sidebar:
                with st.spinner("Summarizing..."):
                    summary = chatbot.summarize_conversation(st.session_state.messages)
                    st.subheader("Conversation Summary")
                    st.write(summary)
        else:
            st.sidebar.warning("There is no conversation to summarize yet.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                response = chatbot.get_response(prompt, st.session_state.messages[:-1])
                message_placeholder.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()