import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Quran Study Companion",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Complete CSS Customization (Emerald & Charcoal Dark Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Body styling */
    .stApp {
        background-color: #121A22;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean Streamlit default elements */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1.5rem 2.5rem; }

    /* Left Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E1816 0%, #0B1312 100%);
        border-right: 1px solid rgba(45, 212, 191, 0.12);
        width: 260px !important;
    }
    .sidebar-title {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #E2E8F0;
        font-size: 1.1rem;
        font-weight: 700;
        padding: 0.5rem 0 1.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 1.5rem;
    }
    
    /* Custom Sidebar Nav Items */
    .stRadio > label { display: none; }
    .stRadio div[role="radiogroup"] { gap: 6px; }
    .stRadio div[role="radiogroup"] > label {
        background: transparent;
        border: 1px solid transparent;
        padding: 0.65rem 1rem;
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stRadio div[role="radiogroup"] > label:hover {
        background: rgba(45, 212, 191, 0.05);
        color: #E2E8F0;
    }
    .stRadio div[role="radiogroup"] > label[data-checked="true"] {
        background: rgba(13, 38, 33, 0.9) !important;
        border: 1px solid rgba(45, 212, 191, 0.3) !important;
        color: #2DD4BF !important;
    }

    /* Header Bar Controls */
    .header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.8rem;
    }
    .page-title {
        font-size: 1.35rem;
        font-weight: 600;
        color: #F8FAFC;
    }

    /* Main Verse Card Interface */
    .verse-card {
        background: linear-gradient(160deg, #182623 0%, #101B19 100%);
        border: 1px solid rgba(45, 212, 191, 0.18);
        border-radius: 14px;
        padding: 2.2rem;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45);
        position: relative;
    }
    .verse-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #94A3B8;
        font-size: 0.92rem;
        font-weight: 500;
        margin-bottom: 2rem;
    }
    .arabic-text-container {
        font-family: 'Amiri', serif;
        font-size: 2.3rem;
        line-height: 2.3;
        text-align: center;
        direction: rtl;
        color: #FFFFFF;
        margin: 1.5rem 0 2rem 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .transliteration-text {
        font-size: 0.88rem;
        color: #94A3B8;
        line-height: 1.6;
        text-align: center;
        max-width: 90%;
        margin: 0 auto 2rem auto;
    }

    /* Audio Bar Container */
    .audio-player-container {
        background: #0B1312;
        border: 1px solid rgba(45, 212, 191, 0.15);
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 1rem;
    }
    
    /* Utility Pills & Badges */
    .recitation-badge {
        background: rgba(45, 212, 191, 0.1);
        border: 1px solid rgba(45, 212, 191, 0.25);
        color: #2DD4BF;
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div class="sidebar-title">
        <span style="font-size: 1.3rem;">📖</span> Quran Study Companion
    </div>
    """, unsafe_allow_html=True)

    nav = st.radio(
        "Navigation Menu",
        ["🏠  Home", "📖  Browse Quran", "🤖  AI Companion", "🎙️  Recitation Coach"],
        index=0
    )

# 4. Top Header & Search Integration
header_col1, header_col2, header_col3 = st.columns([2, 4, 1])

with header_col1:
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)

with header_col2:
    search_query = st.text_input(
        "Search Bar",
        placeholder="🔍  Search or Ask AI (e.g., 'Al-Fatiha Tafsir')",
        label_visibility="collapsed"
    )

with header_col3:
    col_icon1, col_icon2 = st.columns(2)
    with col_icon1:
        st.button("🔔", help="Notifications", use_container_width=True)
    with col_icon2:
        st.button("👤", help="Profile", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. Verse of the Day Card View
st.markdown("""
<div class="verse-card">
    <div class="verse-card-header">
        <span>Verse of the Day (Surah Al-Fatiha, 1-7)</span>
        <span style="cursor: pointer; letter-spacing: 2px;">•••</span>
    </div>
    <div class="arabic-text-container">
        ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ ۝ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ ۝ مَٰلِكِ يَوۡمِ ٱلدِّينِ ۝ إِيَّاكَ نَعۡبُدُ وَإِيَّاكَ نَسۡتَعِينُ ۝ ٱهۡدِنَا ٱلصِّرَٰطَ ٱلۡمُسۡتَقِيمَ ۝ صِرَٰطَ ٱلَّذِينَ أَنۡعَمۡتَ عَلَيۡهِمۡ غَيۡرِ ٱلۡمَغۡضُوبِ عَلَيۡهِمۡ وَلَا ٱلضَّآلِّينَ ۝
    </div>
    <div class="transliteration-text">
        Bi-smi llāhi r-raḥmāni r-raḥīm. Al-ḥamdu li-llāhi rabbi l-ʿālamīn. Ar-raḥmāni r-raḥīm. Māliki yawmi d-dīn. Iyyāka naʿbudu wa-iyyāka nastaʿīn. Ihdinā ṣ-ṣirāṭa l-mustaqīm. Ṣirāṭa l-ladhīna anʿamta ʿalayhim ghayri l-maghḍūbi ʿalayhim wa-lā ḍ-ḍāllīn.
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Audio Player Bar & Action Button
player_col1, player_col2, player_col3, player_col4 = st.columns([1, 4, 2, 2])

with player_col1:
    btn_p1, btn_p2, btn_p3 = st.columns(3)
    with btn_p1:
        st.button("⏮", key="prev_btn")
    with btn_p2:
        st.button("▶", key="play_btn", type="primary")
    with btn_p3:
        st.button("⏭", key="next_btn")

with player_col2:
    st.slider("Audio Seek Bar", 0, 100, 35, label_visibility="collapsed")

with player_col3:
    st.markdown("<p style='text-align: right; color: #94A3B8; font-size: 0.85rem; margin-top: 8px;'>Speed &nbsp;&nbsp; <b>- &nbsp; 1 &nbsp; +</b></p>", unsafe_allow_html=True)

with player_col4:
    if st.button("🎙️ Live Recitation Practice", type="secondary", use_container_width=True):
        st.toast("Opening Live Recitation Coach for this verse...", icon="🎙️")
