import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Quran Study Companion",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Session State Management for Right Side Panel
if "show_side_panel" not in st.session_state:
    st.session_state.show_side_panel = True
if "side_panel_content" not in st.session_state:
    st.session_state.side_panel_content = "tafsir"  # Options: 'tafsir', 'voice_test', 'word_analysis'

# 3. Custom CSS (Charcoal #121A22, Emerald Gradient, Gold Accents)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Canvas */
    .stApp {
        background-color: #121A22;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1.2rem 2rem; }

    /* Left Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E1816 0%, #0B1312 100%);
        border-right: 1px solid rgba(45, 212, 191, 0.15);
    }
    .sidebar-brand {
        color: #D4AF37;
        font-size: 1.15rem;
        font-weight: 700;
        padding-bottom: 1.2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.2rem;
    }

    /* Main Verse Card */
    .verse-card {
        background: linear-gradient(150deg, #182623 0%, #101B19 100%);
        border: 1px solid rgba(45, 212, 191, 0.2);
        border-radius: 14px;
        padding: 2rem;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        margin-bottom: 1.2rem;
    }
    .verse-title {
        color: #D4AF37;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    .arabic-text {
        font-family: 'Amiri', serif;
        font-size: 2.2rem;
        line-height: 2.2;
        text-align: center;
        direction: rtl;
        color: #FFFFFF;
        margin-bottom: 1.2rem;
    }
    .translation-text {
        color: #CBD5E1;
        font-size: 0.95rem;
        text-align: center;
        line-height: 1.6;
    }

    /* Right Side Panel Styling */
    .right-panel-box {
        background: linear-gradient(180deg, #152220 0%, #0E1816 100%);
        border: 1px solid rgba(45, 212, 191, 0.25);
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: -5px 10px 25px rgba(0,0,0,0.3);
    }
    .panel-header {
        color: #2DD4BF;
        font-size: 1.05rem;
        font-weight: 700;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 0.8rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Phoneme Feedback Badges */
    .phoneme-box {
        background-color: #0B1312;
        border: 1px solid rgba(45, 212, 191, 0.2);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .feedback-green { color: #10B981; font-weight: bold; }
    .feedback-yellow { color: #F59E0B; font-weight: bold; text-decoration: underline; }
    .feedback-red { color: #EF4444; font-weight: bold; background: rgba(239, 68, 68, 0.15); padding: 2px 6px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# 4. Left Sidebar (Main Navigation)
with st.sidebar:
    st.markdown('<div class="sidebar-brand">📖 Quran Companion</div>', unsafe_allow_html=True)
    
    nav = st.radio(
        "Nav",
        ["Dashboard", "Browse Quran", "AI Companion", "Recitation Coach"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("⚙️ **Side Panel Controls**")
    if st.button("📑 Toggle Right Side Panel", use_container_width=True):
        st.session_state.show_side_panel = not st.session_state.show_side_panel

# 5. Top Header & Search Bar
top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.text_input(
        "AI Search",
        placeholder="🔍 Search verses or ask AI (e.g., 'Surah Al-Fatiha Tafsir')...",
        label_visibility="collapsed"
    )
with top_col2:
    st.button("✨ Search AI", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. Main Dashboard & Right Side Panel Layout
if st.session_state.show_side_panel:
    main_col, side_panel = st.columns([2.7, 1.3], gap="medium")
else:
    main_col = st.container()
    side_panel = None

# --- MAIN CONTENT AREA (Left/Center) ---
with main_col:
    st.markdown("""
    <div class="verse-card">
        <div class="verse-title">Verse of the Day • Surah Al-Fatiha (1:1-7)</div>
        <div class="arabic-text">
            ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ ۝ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ ۝ مَٰلِكِ يَوۡمِ ٱلدِّينِ
        </div>
        <div class="translation-text">
            "All praise is due to Allah, Lord of the worlds — The Entirely Merciful, the Especially Merciful — Sovereign of the Day of Recompense."
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Audio Player Bar
    audio_col1, audio_col2, audio_col3 = st.columns([1, 3, 1])
    with audio_col1:
        st.button("▶ Play Audio", type="primary", use_container_width=True)
    with audio_col2:
        st.slider("Seek", 0, 100, 30, label_visibility="collapsed")
    with audio_col3:
        st.selectbox("Speed", ["1.0x", "0.75x", "1.25x"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### 📌 Quick Actions (Opens Right Panel)")
    
    act_col1, act_col2, act_col3 = st.columns(3)
    with act_col1:
        if st.button("📖 Open Tafsir Insights", use_container_width=True):
            st.session_state.show_side_panel = True
            st.session_state.side_panel_content = "tafsir"
    with act_col2:
        if st.button("🎙️ Open Live Voice Test", use_container_width=True):
            st.session_state.show_side_panel = True
            st.session_state.side_panel_content = "voice_test"
    with act_col3:
        if st.button("🔍 Open Word Analysis", use_container_width=True):
            st.session_state.show_side_panel = True
            st.session_state.side_panel_content = "word_analysis"

# --- DEDICATED RIGHT SIDE PANEL ---
if st.session_state.show_side_panel and side_panel:
    with side_panel:
        st.markdown('<div class="right-panel-box">', unsafe_allow_html=True)
        
        # Panel Content Option 1: Tafsir Insights
        if st.session_state.side_panel_content == "tafsir":
            st.markdown('<div class="panel-header">📑 Verse Inspector (Tafsir)</div>', unsafe_allow_html=True)
            st.markdown("**Surah Al-Fatiha (Verses 1-3)**")
            st.info("**Theme:** Divine Praise & Merciful Sustenance")
            st.caption("**Linguistic Insight:** 'Al-Hamd' combines gratitude and adoration, specifically reserved for the divine creator.")
            st.divider()
            st.markdown("##### Related Verses")
            st.caption("• Surah Al-An'am (6:1)")
            st.caption("• Surah Saba (34:1)")

        # Panel Content Option 2: Live Voice Recitation Test
        elif st.session_state.side_panel_content == "voice_test":
            st.markdown('<div class="panel-header">🎙️ Live AI Voice Test</div>', unsafe_allow_html=True)
            st.caption("Click record and read the target verse into your mic:")
            
            if st.button("🔴 Start Live Recording", type="primary", use_container_width=True):
                st.toast("Recording live audio...", icon="🎙️")
            
            st.markdown("""
            <div class="phoneme-box">
                <div style="font-family: 'Amiri', serif; font-size: 1.8rem; direction: rtl;">
                    <span class="feedback-green">ٱلۡحَمۡدُ</span> 
                    <span class="feedback-green">لِلَّهِ</span> 
                    <span class="feedback-yellow">رَبِّ</span> 
                    <span class="feedback-red">ٱلۡعَٰلَمِينَ</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.error("**Makhraj Error on 'ٱلۡعَٰلَمِينَ':** Throat letter 'ع' needs deeper vocal cord compression.")
            st.warning("**Tajweed Notice on 'رَبِّ':** Slight over-rolling of the 'ر'.")

        # Panel Content Option 3: Word-by-Word Analysis
        elif st.session_state.side_panel_content == "word_analysis":
            st.markdown('<div class="panel-header">🔍 Word-by-Word Analysis</div>', unsafe_allow_html=True)
            st.markdown("**1. ٱلۡحَمۡدُ (Al-Hamd)**")
            st.caption("Root: *ḥ-m-d* • Noun • Meaning: 'All Praise'")
            st.divider()
            st.markdown("**2. لِلَّهِ (Lillāh)**")
            st.caption("Preposition + Proper Noun • Meaning: 'For Allah'")
            st.divider()
            st.markdown("**3. رَبِّ (Rabbi)**")
            st.caption("Root: *r-b-b* • Noun • Meaning: 'Sustainer / Lord'")

        st.markdown('</div>', unsafe_allow_html=True)
