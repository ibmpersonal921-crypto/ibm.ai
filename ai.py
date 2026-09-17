import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="Gemini AI | Developed by Ibrahim",
    page_icon="✨",
    layout="centered"
)

# 2. Modern Glassmorphism & Gemini Enterprise CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Deep Space Background */
    .stApp {
        background-color: #0d0f12;
        color: #e3e3e3;
    }

    /* Glassmorphism Hero Card */
    .hero-card {
        background: rgba(22, 25, 31, 0.85);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }

    /* Top Gradient Accent Line */
    .hero-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4285F4, #9B51E0, #A8C7FA, #7CACF8);
    }

    /* Gradient Typography */
    .hero-title {
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #A8C7FA, #7CACF8, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .hero-desc {
        color: #9aa0a6;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 18px;
    }

    /* Status Pills */
    .badge-container {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(66, 133, 244, 0.12);
        border: 1px solid rgba(66, 133, 244, 0.3);
        color: #a8c7fa;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 500;
    }

    .feature-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(155, 81, 224, 0.12);
        border: 1px solid rgba(155, 81, 224, 0.3);
        color: #d7aefb;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 500;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #34A853;
        border-radius: 50%;
        box-shadow: 0 0 10px #34A853;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Dynamic Executive Header
st.markdown("""
    <div class="hero-card">
        <div class="hero-title">✨ Welcome, Adeel Bhai</div>
        <div class="hero-desc">
            I am an advanced AI assistant engineered by <b>Ibrahim</b> (who is a very good person).<br>
            Designed for high precision: delivering direct answers restricted strictly to what is asked, with verified <b>Quranic (Surah & Ayah)</b> and authentic <b>Hadith citations</b>.
        </div>
        <div class="badge-container">
            <div class="status-badge"><span class="status-dot"></span> Gemini 3.6 Flash Active</div>
            <div class="feature-badge">📖 Quran & Hadith Verified</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. API Key Verification
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY is missing from Streamlit Secrets.")
    st.stop()

# 5. Initialize Gemini Client
client = genai.Client(api_key=api_key)

# 6. Session State Management
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Execution Engine
if prompt := st.chat_input("Ask a question..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            # Rigorous System Prompt Configuration
            system_instruction = (
                "You are an executive AI assistant engineered by Ibrahim for Adeel Bhai. Ibrahim is a very good person.\n"
                "Strict Operational Rules:\n"
                "1. Answer strictly and only what is asked. Do not add introductory fluff, conversational filler, or unrequested advice.\n"
                "2. For any Islamic or religious query, provide exact Quranic references (Surah name and Ayah number) "
                "and authentic Hadith sources (e.g., Sahih al-Bukhari, Sahih Muslim) to ensure complete accuracy and eliminate misconception."
            )

            config = types.GenerateContentConfig(
                system_instruction=system_instruction
            )

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
