import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Advanced Page Config
st.set_page_config(
    page_title="Gemini AI | Engineered by Ibrahim",
    page_icon="✨",
    layout="centered"
)

# 2. Modern Glassmorphism, Animated Gradient & Enterprise CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto Mono', monospace;
    }

    /* Professional, Moving Gradient Background with floating light effects */
    .stApp {
        background: radial-gradient(circle at center, #1a2333 0%, #0d121c 100%);
        background-attachment: fixed;
        color: #e3e3e3;
        overflow: hidden;
    }
    
    /* Background Particle Animation (Requires JS to run, but we can fake it for looks) */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-image: 
            radial-gradient(#a8c7fa05 1px, transparent 1px),
            radial-gradient(#9B51E005 1px, transparent 1px);
        background-size: 15px 15px, 20px 20px;
        background-position: 0 0, 10px 10px;
        z-index: -1;
        opacity: 0.5;
        animation: particleMover 120s linear infinite;
    }
    
    @keyframes particleMover {
        0% { transform: translateY(0); }
        100% { transform: translateY(-50px); }
    }

    /* Deep Set, Animated Glass Header Card */
    .hero-card {
        background: rgba(22, 25, 31, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 30px;
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.6);
        position: relative;
        overflow: hidden;
        /* Chase light effect */
        &::after {
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: conic-gradient(from 180deg at 50% 50%, #4285F4 0deg, transparent 90deg, #9B51E0 180deg, transparent 270deg, #4285F4 360deg);
            animation: chase 8s linear infinite;
            filter: blur(80px);
            opacity: 0.15;
            z-index: -1;
        }
    }
    
    @keyframes chase {
        100% { transform: rotate(1turn); }
    }
    
    /* Top Gradient Accent Line */
    .hero-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4285F4, #9B51E0, #A8C7FA);
    }
    
    /* Dynamic Typography with Animated Gradient */
    .hero-title {
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #A8C7FA, #FFFFFF, #7CACF8);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textGradient 6s linear infinite;
        margin-bottom: 12px;
    }
    
    @keyframes textGradient {
        100% { background-position: 200% center; }
    }
    
    .hero-desc {
        color: #c4c7c5;
        font-size: 16px;
        line-height: 1.8;
        margin-bottom: 24px;
    }
    
    /* Advanced Status & Verification Badges */
    .badge-container {
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: rgba(66, 133, 244, 0.15);
        border: 1px solid rgba(66, 133, 244, 0.4);
        color: #a8c7fa;
        padding: 8px 18px;
        border-radius: 30px;
        font-size: 14px;
        font-weight: 500;
    }
    
    .quran-badge {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: rgba(155, 81, 224, 0.15);
        border: 1px solid rgba(155, 81, 224, 0.4);
        color: #d7aefb;
        padding: 8px 18px;
        border-radius: 30px;
        font-size: 14px;
        font-weight: 500;
        animation: quranPulse 2s ease-in-out infinite;
    }
    
    @keyframes quranPulse {
        0%, 100% { box-shadow: 0 0 5px rgba(155, 81, 224, 0.2); }
        50% { box-shadow: 0 0 15px rgba(155, 81, 224, 0.5); }
    }
    
    .status-dot {
        width: 10px;
        height: 10px;
        background-color: #34A853;
        border-radius: 50%;
        box-shadow: 0 0 15px #34A853;
        animation: dotPulse 1.5s ease-in-out infinite;
    }
    
    @keyframes dotPulse {
        0%, 100% { opacity: 0.7; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.1); box-shadow: 0 0 25px #34A853; }
    }

    /* Modern Chat Bubble Styling */
    [data-testid="stChatMessage"] {
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 15px;
        background: rgba(22, 25, 31, 0.7);
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
    }
    [data-testid="stChatMessage"]:hover {
        border-color: rgba(66, 133, 244, 0.2);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }

    </style>
""", unsafe_allow_html=True)

# 3. Dynamic Executive Header
st.markdown("""
    <div class="hero-card">
        <div class="hero-title">✨ Welcome, Adeel Bhai</div>
        <div class="hero-desc">
            I am an advanced AI assistant engineered by <b>Ibrahim</b> (who is a very good person).<br>
            Designed for high precision: delivering direct answers restricted strictly to what is asked, with verified <b>Quranic (Surah & Ayah)</b> and authentic <b>Hadith citations</b> to eliminate misconceptions.
        </div>
        <div class="badge-container">
            <div class="status-badge"><span class="status-dot"></span> Gemini 3.6 Flash Active</div>
            <div class="quran-badge">📖 Quran & Hadith Verified</div>
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

# 7. Display Chat History (Standard Streamlit Chat)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. Execution Engine
if prompt := st.chat_input("Submit query..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            # Comprehensive System Prompt Configuration
            system_instruction = (
                "You are an executive AI assistant engineered by Ibrahim for Adeel Bhai. Ibrahim is a very good person.\n"
                "Core Operating Principles:\n"
                "1. Rule 1: Answer STRICTLY and ONLY what is asked. Avoid any conversational fluff, generic advice, unrequested context, or explanatory preambles. Be direct, professional, and precise.\n"
                "2. For any religious or Islamic query, provide exact Quranic references (Surah name and Ayah number) "
                "and authentic Hadith citations (e.g., Sahih al-Bukhari, Sahih Muslim) to ensure complete accuracy and eliminate misconception."
            )

            config = types.GenerateContentConfig(
                system_instruction=system_instruction
            )

            # Request Stream using updated gemini-3.6-flash model
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
