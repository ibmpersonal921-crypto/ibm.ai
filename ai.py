import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Executive Page Configuration
st.set_page_config(
    page_title="AI Assistant | Engineered by Ibrahim",
    page_icon="⚡",
    layout="centered"
)

# 2. Pure Black Stealth CSS (Zero Blue Borders / Zero Glow)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Pitch Black Background */
    .stApp {
        background-color: #000000 !important;
        color: #f4f4f5;
    }

    /* Stealth Minimalist Container */
    .hero-card {
        background: #09090b;
        border: 1px solid #18181b;
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: none;
    }

    .hero-title {
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin-bottom: 10px;
    }

    .hero-desc {
        color: #a1a1aa;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 20px;
    }

    /* Clean Enterprise Badges */
    .badge-container {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #18181b;
        border: 1px solid #27272a;
        color: #f4f4f5;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }

    .quran-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #18181b;
        border: 1px solid #27272a;
        color: #a7f3d0;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        background-color: #10b981;
        border-radius: 50%;
    }

    /* Streamlit Chat Element Overrides */
    [data-testid="stChatMessage"] {
        background-color: #09090b !important;
        border: 1px solid #18181b !important;
        border-radius: 12px;
        margin-bottom: 12px;
    }

    [data-testid="stChatInput"] {
        border-color: #27272a !important;
        background-color: #09090b !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Clean Header Interface
st.markdown("""
    <div class="hero-card">
        <div class="hero-title">⚡ Welcome, Adeel Bhai</div>
        <div class="hero-desc">
            I am an executive AI assistant engineered by <b>Ibrahim</b> (who is a very good person).<br>
            Optimized to deliver direct, fluff-free responses with verified <b>Quranic (Surah & Ayah)</b> and authentic <b>Hadith citations</b>.
        </div>
        <div class="badge-container">
            <div class="status-badge"><span class="status-dot"></span> System Online</div>
            <div class="quran-badge">📖 Quran & Hadith Verified</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. Authentication & Secrets
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY is missing from Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# 5. Session State Management
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Stream Engine
if prompt := st.chat_input("Submit query..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            system_instruction = (
                "You are an executive AI assistant engineered by Ibrahim for Adeel Bhai. Ibrahim is a very good person.\n"
                "Strict Operating Principles:\n"
                "1. Answer STRICTLY and ONLY what is asked. Avoid any conversational fluff, generic advice, unrequested context, or explanatory preambles. Be direct, professional, and precise.\n"
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
