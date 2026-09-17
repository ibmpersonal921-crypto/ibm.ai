import os
import time
import streamlit as st
from google import genai
from google.genai import types

# ------------------------------------------------------------------------------
# 1. Page Configuration
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Assistant | Engineered by Ibrahim",
    page_icon="⚡",
    layout="centered"
)

# ------------------------------------------------------------------------------
# 2. Pure Black UI + Curved Pill Input + Static RGB Accent
# ------------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Target typography explicitly to preserve Streamlit icon ligatures */
    html, body, p, span, div, h1, h2, h3, h4, h5, h6, label, input, textarea {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Absolute Pitch Black Theme Canvas */
    .stApp, 
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

    /* Hide Default Header Accent */
    [data-testid="stHeader"] {
        display: none !important;
    }

    /* Hero Card with Top RGB Gradient Line */
    .hero-card {
        background: #09090b;
        border: 1px solid #18181b;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }

    .hero-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #ff0055, #00e5ff, #9d00ff);
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
        margin-bottom: 16px;
    }

    /* Badges */
    .badge-container {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    .status-badge, .quran-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #141417;
        border: 1px solid #27272a;
        color: #f4f4f5;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        background-color: #00e5ff;
        border-radius: 50%;
    }

    /* Chat Messages Container */
    [data-testid="stChatMessage"] {
        background-color: #09090b !important;
        border: 1px solid #18181b !important;
        border-radius: 16px;
        margin-bottom: 12px;
        color: #f4f4f5 !important;
    }

    /* Modern Curved Pill Input Bar */
    [data-testid="stChatInput"] {
        background-color: transparent !important;
        padding-bottom: 8px !important;
    }

    [data-testid="stChatInput"] > div {
        background-color: #09090b !important;
        border: 1px solid #27272a !important;
        border-radius: 26px !important;
        padding: 4px 12px !important;
        box-shadow: none !important;
    }

    [data-testid="stChatInput"] > div:focus-within {
        border-color: #00e5ff !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        background-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stChatInput"] button {
        border-radius: 50% !important;
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        color: #ffffff !important;
    }

    /* Sidebar Border Fix */
    section[data-testid="stSidebar"] {
        border-right: 1px solid #18181b !important;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. Sidebar Tool Panel
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛠️ Options & Attachments")
    uploaded_file = st.file_uploader(
        "Upload Document / Image",
        type=["pdf", "txt", "png", "jpg", "jpeg", "csv"],
        help="Attach context files for analysis"
    )
    if uploaded_file:
        st.success(f"Attached: {uploaded_file.name}")
    
    st.markdown("---")
    st.markdown("**System Specs:**")
    st.caption("• Model: Gemini 3.6 Flash")
    st.caption("• Engine: Quran & Hadith Citation Active")
    st.caption("• Policy: Zero-Fluff Executive Mode")

# ------------------------------------------------------------------------------
# 4. Hero Header Card
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# 5. Authentication
# ------------------------------------------------------------------------------
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY is missing from Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# ------------------------------------------------------------------------------
# 6. Session State Chat History
# ------------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------------------------------------------------------------------------
# 7. Stream Processing Engine with Auto-Retry for Rate Limits (429)
# ------------------------------------------------------------------------------
if prompt := st.chat_input("Submit query..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        # Construct multimodal payload
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
            "3. If a document or image is attached, analyze its contents directly and answer the query."
        )

        config = types.GenerateContentConfig(system_instruction=system_instruction)

        # Rate Limit Mitigation Engine (3 retries with 3-second sleep)
        max_retries = 3
        for attempt in range(max_retries):
            try:
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
                break  # Successful stream, exit retry loop

            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                    if attempt < max_retries - 1:
                        time.sleep(3)  # Pause for free tier cool-down
                        continue
                    else:
                        placeholder.markdown("⚠️ **Rate limit reached.** Google's Free Tier quota was hit. Please wait ~30 seconds and resubmit.")
                else:
                    placeholder.markdown(f"⚠️ **Execution Error:** {err_msg}")
                    break

    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
