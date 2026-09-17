import os
import streamlit as st
from google import genai

# 1. Page Configuration
st.set_page_config(page_title="Gemini AI Assistant", page_icon="🤖", layout="centered")
st.title("🤖 Custom Generative AI Assistant")
st.caption("Powered by Google Gemini & Streamlit")

# 2. Retrieve API Key securely from Streamlit Secrets
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing! Please set GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# 3. Initialize Client
client = genai.Client(api_key=api_key)

# 4. Initialize Session State Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Input & Streaming Response
if prompt := st.chat_input("Ask your AI assistant anything..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=prompt
            )
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"Error generating response: {e}")
            
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
