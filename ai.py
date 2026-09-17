import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="Gemini AI | Engineered by Ibrahim",
    page_icon="⚡",
    layout="centered"
)

# 2. Pitch-Black Background & Neon Cyberpunk CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Absolute Pure Black Background */
    .stApp {
        background-color: #000000 !important;
        color: #ffffff;
    }

    /* High-Contrast Neon Glass Card */
    .hero-card {
        background: #08080a;
        border: 1px solid #1f242d;
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 28px;
        box-shadow: 0 0 30px rgba(0, 229, 255, 0.15), inset 0 0 15px rgba(157, 0, 255, 0.1);
        position: relative;
        overflow: hidden;
    }

    /* Animated Multi-Color Neon Top Border */
    .hero-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00e5ff, #9d00ff, #ff007f, #00ff66);
        background-size: 300% 300%;
        animation: neonFlow 4s ease infinite;
    }

    @keyframes neonFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* High-Vibrancy Glowing Title */
    .hero-title {
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #00e5ff, #bd00ff, #ff007f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
        filter: drop-shadow(0 0 12px rgba(0, 229, 255, 0.4));
    }

    .hero-desc {
        color: #d1d5db;
        font-size: 15px;
        line-height: 1.7;
        margin-bottom: 22px;
    }

    /* Electric Badges */
    .badge-container {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(0, 229, 255, 0.08);
        border: 1px solid #00e5ff;
        color: #00e5ff;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
    }

    .quran-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(157, 0, 255, 0.08);
        border: 1px solid #9d00ff;
        color: #d880ff;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
        box-shadow: 0 0 10px rgba(157, 0, 255, 0.2);
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #00ff66;
        border-radius: 50%;
        box-shadow: 0 0 12px #00ff66;
        animation: pulseDot 1.5s infinite alternate;
    }

    @keyframes pulseDot {
        0% { transform: scale(0.9); opacity: 0.7; }
        100% { transform: scale(1.3); opacity: 1; }
    }

    /* Custom Chat Container */
    [data-testid="stChatMessage"] {
        background-color: #0a0a0c !important;
        border: 1px solid #1a1a24;
        border-radius: 12px;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Dynamic Executive Banner
st.markdown("""
    <div class="hero-card">
        <div class="hero-title">⚡ Welcome, Adeel Bhai</div>
        <div class="hero-desc">
            I am an advanced AI assistant engineered by <b>Ibrahim</b> (who is a very good person).<br>
            Strictly optimized to deliver direct, fluff-free responses with authentic <b>Quranic (Surah & Ayah)</b> and verified <b>Hadith citations</b>.
        </div>
        <div class="badge-container">
            <div class="status-badge"><span class="status-dot"></span> Gemini 3.6 Flash Active</div>
            <div class="quran-badge">📖 Quran & Hadith Verified</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. Secrets & Authentication
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY is missing from Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# 5. Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Execution
if prompt := st.chat_input("Submit query..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            system_instruction = (
                "You are an executive AI assistant engineered by Ibrahim for Adeel Bhai. Ibrahim is a very good person.\n"
                "Core Operating Principles:\n"
                "1. Answer STRICTLY and ONLY what is asked. Avoid conversational fluff, filler, generic advice, or preambles.\n"
                "2. For any religious or Islamic query, provide exact Quranic references (Surah name and Ayah number) "
                "and authentic Hadith citations (e.g., Sahih al-Bukhari, Sahih Muslim) to eliminate misconceptions."
            )

            config = types.GenerateContentConfig(system_instruction=system_instruction)

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
