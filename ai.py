import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Quran Study Companion",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS Injection (App Aesthetic & Colors)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Canvas Styling */
    .stApp {
        background-color: #121A22;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove standard Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* Top App Navigation Header */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 1.5rem;
        background: linear-gradient(180deg, #1A2530 0%, #121A22 100%);
        border: 1px solid rgba(212, 175, 55, 0.15);
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .app-logo {
        color: #D4AF37;
        font-size: 1.3rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .status-badge {
        background: rgba(15, 46, 40, 0.8);
        color: #2DD4BF;
        border: 1px solid rgba(45, 212, 191, 0.3);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
    }

    /* Main Verse Card Styling */
    .verse-card {
        background: linear-gradient(135deg, #16222F 0%, #0F2E28 100%);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 16px;
        padding: 2.2rem;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
        margin-bottom: 1.5rem;
    }
    .verse-meta {
        color: #D4AF37;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        margin-bottom: 1.2rem;
    }
    .arabic-text {
        font-family: 'Amiri', serif;
        font-size: 2.2rem;
        line-height: 2.2;
        text-align: right;
        direction: rtl;
        color: #FFFFFF;
        margin-bottom: 1.5rem;
    }
    .translation-text {
        font-size: 1.05rem;
        color: #CBD5E1;
        line-height: 1.7;
        font-weight: 300;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 1.2rem;
    }

    /* Custom Input & Button Overrides */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #16222F;
        padding: 6px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 6px;
        color: #94A3B8;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0F2E28 !important;
        color: #D4AF37 !important;
        border: 1px solid rgba(212, 175, 55, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# 3. App Header Bar
st.markdown("""
<div class="app-header">
    <div class="app-logo">✨ Quran Study Companion</div>
    <div class="status-badge">AI Assistant Active</div>
</div>
""", unsafe_allow_html=True)

# 4. App Navigation Tabs (Top-Level)
tab_home, tab_browse, tab_ai, tab_coach = st.tabs([
    "🏠 Dashboard", 
    "📖 Browse Quran", 
    "🤖 AI Companion", 
    "🎙️ Recitation Coach"
])

with tab_home:
    # Verse of the Day Showcase
    st.markdown("""
    <div class="verse-card">
        <div class="verse-meta">Verse of the Day • Surah Al-Fatiha (1:1-7)</div>
        <div class="arabic-text">
            𩧯 ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ ۝ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ ۝ مَٰلِكِ يَوۡمِ ٱلدِّينِ
        </div>
        <div class="translation-text">
            "All praise is due to Allah, Lord of the worlds — The Entirely Merciful, the Especially Merciful — Sovereign of the Day of Recompense."
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Audio Control Bar
    st.markdown("#### Audio Recitation")
    audio_col1, audio_col2, audio_col3 = st.columns([1, 4, 1])
    with audio_col1:
        st.button("▶ Play", use_container_width=True)
    with audio_col2:
        st.slider("Audio Progress", 0, 100, 35, label_visibility="collapsed")
    with audio_col3:
        st.selectbox("Reciter", ["Mishary Rashid", "Abdul Basit", "Al-Sudais"], label_visibility="collapsed")

    st.divider()

    # Quick Feature Hub
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.subheader("Tafsir Insights")
        st.caption("Deep-dive historical context and linguistic analysis powered by AI.")
        st.button("Explore Tafsir", key="tafsir_btn")
    with col_b:
        st.subheader("Daily Goals")
        st.progress(0.7, text="70% of Daily Reading Completed")
        st.button("Continue Reading", key="goal_btn")
    with col_c:
        st.subheader("Voice Analysis")
        st.caption("Practice Tajweed rules and receive instant audio feedback.")
        st.button("Start Practice", key="voice_btn")

with tab_browse:
    st.subheader("Browse Surahs")
    st.text_input("Search by Surah name or page number...", placeholder="e.g., Al-Baqarah")

with tab_ai:
    st.subheader("AI Study Assistant")
    st.chat_input("Ask a question about verses, themes, or historical contexts...")

with tab_coach:
    st.subheader("Recitation Coach")
    st.file_uploader("Upload audio recording (.mp3, .wav) for Tajweed evaluation", type=["mp3", "wav"])
