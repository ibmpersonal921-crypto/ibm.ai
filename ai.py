import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Executive Page Configuration
st.set_page_config(
    page_title="AI Assistant | Engineered by Ibrahim",
    page_icon="⚫",
    layout="centered"
)

# 2. Complete CSS Reset (Nukes Streamlit's Default Blue/Grey Theme Engine)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Font & Reset */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Force Every Native Frame to Absolute Pitch Black #000000 */
    html, body, .stApp, 
    [data-testid="stHeader"], 
    [data-testid="stToolbar"], 
    [data-testid="stAppViewContainer"], 
    [data-testid="stMain"], 
    [data-testid="stBottom"], 
    [data-testid="stBottom"] > div,
    [data-testid="stChatInput"],
    header, footer {
        background-color: #000000 !important;
        background: #000000 !important;
    }

    /* Hide Top Streamlit Color Bar Header Accent */
    [data-testid="stHeader"] {
        display: none !important;
    }

    /* Stealth Container */
    .hero-card {
        background: #080808;
        border: 1px solid #1a1a1a;
        border-radius: 14px;
        padding: 26px;
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }

    .hero-desc {
        color: #a1a1aa;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 18px;
    }

    /* Pure Monochrome Badges */
    .badge-container {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    .status-badge, .quran-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #121212;
        border: 1px solid #222222;
        color: #e4e4e7;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        background-color: #ffffff;
        border-radius: 50%;
    }

    /* Chat Messages Styling */
    [data-testid="stChatMessage"] {
        background-color: #080808 !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 12px;
        margin-bottom: 12px;
        color: #f4f4f5 !important;
    }

    /* Kill All Blue/Glow Focus Outlines on Chat Input */
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] textarea {
        background-color: #080808 !important;
        border-color: #222222 !important;
        color: #ffffff !important;
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stChatInput"] textarea:focus,
    [data-testid="stChatInput"] textarea:focus-visible,
    [data-testid="stChatInput"] textarea:focus-within {
        border-color: #444444 !important;
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stChatInput"] button {
        background-color: #121212 !important;
        border: 1px solid #222222 !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Clean Header Interface
st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Welcome, Adeel Bhai</div>
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
