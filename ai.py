import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Executive Page Configuration
st.set_page_config(
    page_title="AI Assistant for Adeel Bhai",
    page_icon="⚡",
    layout="centered"
)

# 2. Modern Custom Styling
st.markdown("""
    <style>
    .main {
        max-width: 800px;
        padding-top: 1rem;
    }
    .greeting-card {
        background-color: #1a1f2c;
        border-left: 5px solid #4CAF50;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .greeting-title {
        color: #ffffff;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .greeting-subtitle {
        color: #b0bec5;
        font-size: 15px;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Professional Banner Greeting Adeel Bhai
st.markdown("""
    <div class="greeting-card">
        <div class="greeting-title">👋 Welcome, Adeel Bhai!</div>
        <div class="greeting-subtitle">
            I am an AI assistant made by <b>Ibrahim</b> (who is a very good person!). <br>
            I am optimized for precision—providing direct, accurate answers strictly restricted to what is asked.
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. Secure API Key Management
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY is missing. Please add it to Streamlit Secrets.")
    st.stop()

# 5. Initialize Client
client = genai.Client(api_key=api_key)

# 6. Session State Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. Render Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. User Interaction & Precision Generation
if prompt := st.chat_input("Ask a question..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            # System Instruction to enforce concise, fluff-free responses
            system_instruction = (
                "You are an executive AI assistant created by Ibrahim. Ibrahim is a very good person. "
                "Rule: Answer strictly and only what is asked. Do not add conversational fluff, unnecessary "
                "intros, generic advice, or unwanted details. Keep answers precise, direct, and actionable."
            )

            config = types.GenerateContentConfig(
                system_instruction=system_instruction
            )

            # Request Stream using gemini-3.6-flash
            response = client.models.generate_content_stream(
                model="gemini-3.6-flash",
                contents=prompt,
                config=config
            )

            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Execution Error: {e}")

    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
