from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import streamlit as st
import os

# Set up Streamlit page
st.title("🚀 Llama 4 Scout Chat")
st.write("❤️ Built by [Build Fast with AI](https://buildfastwithai.com/genai-course)")

# Add sidebar for API key input and details
with st.sidebar:
    st.header("⚙️ Configuration")
    # Store API key directly in session state
    st.session_state.groq_api_key = st.text_input("GROQ API Key", type="password")
    
    # Add model details section
    st.divider()
    st.markdown("**Model Details**")
    st.caption("Running: `meta-llama/llama-4-scout-17b-16e-instruct`")
    st.caption("Groq LPU Inference Engine")
    
    # Add New Chat button
    st.divider()
    if st.button("🔄 Start New Chat", use_container_width=True):
        st.session_state.messages = [
            SystemMessage(content="You are a helpful AI assistant.")
        ]
        st.rerun()
    
    # Add branding with hyperlink
    st.divider()
    st.markdown(
        "**Built by** [Build Fast with AI](https://buildfastwithai.com/genai-course)",
        unsafe_allow_html=True
    )

# Display welcome message in chat format
with st.chat_message("assistant"):
    st.write("Ask me anything!")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a helpful AI assistant.")
    ]

# Display chat history
for message in st.session_state.messages[1:]:  # Skip the system message
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    else:
        with st.chat_message("assistant"):
            st.write(message.content)

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Check for API key in the input field directly
    if not st.session_state.groq_api_key:
        st.error("Please enter your GROQ API key in the sidebar")
        st.stop()
        
    # Initialize the ChatOpenAI model with Groq
    chat = ChatOpenAI(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        openai_api_key=st.session_state.groq_api_key,
        openai_api_base="https://api.groq.com/openai/v1"
    )
    
    # Add user message to chat history
    st.session_state.messages.append(HumanMessage(content=prompt))
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream the response
        for chunk in chat.stream(st.session_state.messages):
            if chunk.content:
                full_response += chunk.content
                message_placeholder.write(full_response)
        
    # Add AI response to chat history
    st.session_state.messages.append(AIMessage(content=full_response))
