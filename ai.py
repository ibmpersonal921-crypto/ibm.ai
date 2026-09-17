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

# 2. Pure Black Background with Smooth RGB Border & Accent Animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Absolute Pitch Black Background Engine */
    html, body, .stApp, 
    [data-testid="stHeader"], 
    [data-testid="stToolbar"], 
    [data-testid="stAppViewContainer"], 
    [data-testid="stMain"], 
    [data-testid="stBottom"], 
    [data-testid="stSidebar"],
    footer {
        background-color: #000000 !important;
        background: #000000 !important;
    }

    /* Hide Top Streamlit Color Bar Header Accent */
    [data-testid="stHeader"] {
        display: none !important;
    }

    /* RGB Animated Border Keyframes */
    @keyframes rgbGlow {
        0% { border-color: #ff0055; box-shadow: 0 0 12px rgba(255, 0, 85, 0.25); }
        33% { border-color: #00e5ff; box-shadow: 0 0 12px rgba(0, 229, 255, 0.25); }
        66% { border-color: #9d00ff; box-shadow: 0 0 12px rgba(157, 0, 255, 0.25); }
        100% { border-color: #ff0055; box-shadow: 0 0 12px rgba(255, 0, 85, 0.25); }
    }

    @keyframes rgbText {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Stealth Container with RGB Animated Border */
    .hero-card {
        background: #080808;
        border: 1px solid #ff0055;
        border-radius: 16px;
        padding: 26px;
        margin-bottom: 24px;
        animation: rgbGlow 8s linear infinite;
    }

    /* Animated Dynamic Gradient Title */
    .hero-title {
        font-size: 26px;
        font-weight: 700;
        background: linear-gradient(90deg, #ff0055, #00e5ff, #9d00ff, #ff0055);
        background-size: 300% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: rgbText 6s ease infinite;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }

    .hero-desc {
        color: #a1a1aa;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 18px;
    }

    /* RGB Accented Badges */
    .badge-container {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    .status-badge, .quran-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #111111;
        border: 1px solid #222222;
        color: #f4f4f5;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        background-color: #00e5ff;
        border-radius: 50%;
        box-shadow: 0 0 8px #00e5ff;
    }

    /* Chat Messages & Sidebar Styling Overrides */
    [data-testid="stChatMessage"] {
        background-color: #080808 !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 12px;
        margin-bottom: 12px;
        color: #f4f4f5 !important;
    }

    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] textarea {
        background-color: #080808 !important;
        border-color: #222222 !important;
        color: #ffffff !important;
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: #00e5ff !important;
        box-shadow: 0 0 8px rgba(0, 229, 255, 0.3) !important;
    }

    [data-testid="stChatInput"] button {
        background-color: #121212 !important;
        border: 1px solid #222222 !important;
        color: #ffffff !important;
    }

    /* Sidebar RGB Styling */
    section[data-testid="stSidebar"] {
        border-right: 1px solid #1a1a1a !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Tool Panel for Attachments & Extra Options
with st.sidebar:
    st.markdown("### 🛠️ Options & Attachments")
    uploaded_file = st.file_uploader(
        "Upload Document / Image",
        type=["pdf", "txt", "png", "jpg", "jpeg", "csv"],
        help="Upload context documents or images for Gemini 3.6 Flash analysis"
    )
    if uploaded_file:
        st.success(f"Attached: {uploaded_file.name}")
    
    st.markdown("---")
    st.markdown("**Engine Specs:**")
    st.caption("• Model: Gemini 3.6 Flash")
    st.caption("• Verification: Active Quran & Hadith Engine")
    st.caption("• Output Policy: Zero-Fluff Executive Mode")

# 4. Main RGB Header Interface
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

# 5. Authentication & Secrets Verification
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY is missing from Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# 6. Session State Management
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Stream Processing & Multimodal Input Support
if prompt := st.chat_input("Submit query..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            # Prepare Multi-modal contents list if document/file is uploaded
            contents_payload = []
            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
                mime_type = uploaded_file.type
                contents_payload.append(types.Part.from_bytes(data=file_bytes, mime_type=mime_type))
            
            contents_payload.append(prompt)

            system_instruction = (
                "You are an executive AI assistant engineered by Ibrahim for Adeel Bhai. Ibrahim is a very good person.\n"
                "Strict Operating Principles:\n"
                "1. Answer STRICTLY and ONLY what is asked. Avoid any conversational fluff, generic advice, unrequested context, or explanatory preambles. Be direct, professional, and precise.\n"
                "2. For any religious or Islamic query, provide exact Quranic references (Surah name and Ayah number) "
                "and authentic Hadith citations (e.g., Sahih al-Bukhari, Sahih Muslim) to eliminate misconceptions.\n"
                "3. If a document or image is attached, analyze its contents directly and directly answer the query regarding it."
            )

            config = types.GenerateContentConfig(system_instruction=system_instruction)

            response = client.models.generate_content_stream(
                model="gemini-3.6-flash",
                contents=contents_payload,
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
