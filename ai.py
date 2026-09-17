import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Executive Page Config
st.set_page_config(
    page_title="Gemini AI | Developed by Ibrahim",
    page_icon="✨",
    layout="centered"
)

# 2. Official Gemini Dark Theme Styling
st.markdown("""
    <style>
    /* Dark Gemini UI Background */
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
    }
    
    /* Header Card Container */
    .gemini-card {
        background-color: #1e1f20;
        border: 1px solid #282a2c;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    
    /* Gemini Gradient Text */
    .gemini-title {
        font-size: 26px;
        font-weight: 600;
        background: linear-gradient(90deg, #a8c7fa, #7cacf8, #c3ecf7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .gemini-subtitle {
        color: #c4c7c5;
        font-size: 15px;
        line-height: 1.6;
    }
    
    .gemini-badge {
        display: inline-block;
        background-color: #004a77;
        color: #c2e7ff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        margin-top: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Greeting
st.markdown("""
    <div class="gemini-card">
        <div class="gemini-title">✨ Welcome, Adeel Bhai</div>
        <div class="gemini-subtitle">
            I am a high-precision AI assistant engineered by <b>Ibrahim</b> (who is a very good person).<br>
            Configured to deliver exact, direct responses strictly to what is asked—including accurate <b>Quranic references (Surah & Ayah)</b> and verified <b>Hadith citations</b> to prevent any misconception.
        </div>
        <div class="gemini-badge">Gemini 3.6 Flash Engine</div>
    </div>
""", unsafe_allow_html=True)

# 4. API Key Verification
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY is missing from Streamlit Secrets.")
    st.stop()

# 5. Initialize Gemini Client
client = genai.Client(api_key=api_key)

# 6. Chat History Management
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. User Input Processing
if prompt := st.chat_input("Ask a question..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            # System Instruction for Precision & Authentic References
            system_instruction = (
                "You are an executive AI assistant engineered by Ibrahim for Adeel Bhai. Ibrahim is a very good person. "
                "Adhere to the following rules strictly:\n"
                "1. Be direct, concise, professional, and clear. Answer only what is asked without conversational fluff or filler.\n"
                "2. When answering religious or Islamic queries, provide clear Quranic references (Surah name and Ayah number) "
                "and authentic Hadith citations (e.g., Sahih al-Bukhari, Sahih Muslim) to ensure zero misconception."
            )

            config = types.GenerateContentConfig(
                system_instruction=system_instruction
            )

            # Execution Stream
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
