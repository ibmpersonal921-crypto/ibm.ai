import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Quran Study Companion",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS Injection (Emerald Dark Theme & Sidebar Styling)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global App Canvas */
    .stApp {
        background-color: #121A22;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Chrome Cleanup */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E161F 0%, #0A1C18 100%);
        border-right: 1px solid rgba(45, 212, 191, 0.15);
    }
    .sidebar-brand {
        color: #D4AF37;
        font-size: 1.25rem;
        font-weight: 700;
        padding: 0.5rem 0 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.5rem;
    }

    /* Cards with Emerald Tint */
    .app-card {
        background: linear-gradient(135deg, #16222F 0%, #0D2621 100%);
        border: 1px solid rgba(45, 212, 191, 0.2);
        border-radius: 14px;
        padding: 1.8rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
        margin-bottom: 1.2rem;
    }
    
    /* Verse Formatting */
    .verse-meta {
        color: #D4AF37;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .arabic-text {
        font-family: 'Amiri', serif;
        font-size: 2.1rem;
        line-height: 2.2;
        text-align: right;
        direction: rtl;
        color: #FFFFFF;
        margin-bottom: 1rem;
    }
    
    /* Live Recitation Feedback Elements */
    .recitation-box {
        background-color: #0A141D;
        border: 1px solid rgba(45, 212, 191, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    .feedback-green { color: #10B981; font-weight: 700; }
    .feedback-yellow { color: #F59E0B; font-weight: 700; text-decoration: underline; }
    .feedback-red { color: #EF4444; font-weight: 700; background: rgba(239, 68, 68, 0.15); padding: 2px 6px; border-radius: 4px; }
    
    .status-badge-online {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span>📖 Quran Companion</span>
    </div>
    """, unsafe_allow_html=True)
    
    nav_option = st.radio(
        "Navigation",
        ["Dashboard", "Live Recitation Coach", "AI Companion", "Browse Quran"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("##### 🎙️ Audio Engine")
    st.caption("AI Model: **Tajweed-Net v2.4**")
    st.markdown('<span class="status-badge-online">● Mic Ready</span>', unsafe_allow_html=True)

# 4. Global Search Header (Top of Main View)
search_col1, search_col2 = st.columns([4, 1])
with search_col1:
    ai_query = st.text_input(
        "AI Search",
        placeholder="🔍 Ask AI: 'Explain Surah Al-Mulk verse 2' or search by topic...",
        label_visibility="collapsed"
    )
with search_col2:
    st.button("✨ Ask AI", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. Main Views Logic
if nav_option == "Dashboard":
    # Verse of the Day Card
    st.markdown("""
    <div class="app-card">
        <div class="verse-meta">Verse of the Day • Surah Al-Fatiha (1:1-3)</div>
        <div class="arabic-text">
            ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ ۝ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ ۝ مَٰلِكِ يَوۡمِ ٱلدِّينِ
        </div>
        <p style="color: #CBD5E1; font-size: 0.98rem; margin-top: 1rem;">
            "All praise is due to Allah, Lord of the worlds — The Entirely Merciful, the Especially Merciful — Sovereign of the Day of Recompense."
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Audio Controls Row
    col_play, col_slider, col_reciter = st.columns([1, 3, 1])
    with col_play:
        st.button("▶ Play Audio", use_container_width=True)
    with col_slider:
        st.slider("Seek", 0, 100, 20, label_visibility="collapsed")
    with col_reciter:
        st.selectbox("Reciter", ["Mishary Rashid", "Al-Minshawi"], label_visibility="collapsed")

    # Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Weekly Streak", "5 Days", "+1 today")
    with m2:
        st.metric("Tajweed Accuracy", "92%", "+3%")
    with m3:
        st.metric("Verses Revised", "42", "Target: 50")

elif nav_option == "Live Recitation Coach":
    st.subheader("🎙️ Live AI Recitation & Tajweed Correction")
    st.caption("Read aloud into your microphone. The AI engine will analyze your pronunciation and Tajweed rules in real-time.")

    # Target Verse Card
    st.markdown("""
    <div class="app-card">
        <div class="verse-meta">Target Recitation: Surah Al-Ikhlas (112:1-2)</div>
        <div class="arabic-text">
            قُلۡ هُوَ ٱللَّهُ أَحَدٌ ۝ ٱللَّهُ ٱلصَّمَدُ
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Recording Control Panel
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1, 2, 1])
    with ctrl_col1:
        st.button("🔴 Start Live Recording", type="primary", use_container_width=True)
    with ctrl_col2:
        st.progress(65, text="AI Listening... Analyzing waveform")
    with ctrl_col3:
        st.button("⏹️ Stop & Analyze", use_container_width=True)

    st.markdown("### 📊 Real-Time AI Diagnostics")
    
    diag_col1, diag_col2 = st.columns([3, 2])
    
    with diag_col1:
        # Visual Phoneme Feedback Box
        st.markdown("""
        <div class="recitation-box">
            <h5 style="color: #94A3B8; margin-bottom: 1rem;">Phoneme & Tajweed Visual Feedback</h5>
            <div style="font-family: 'Amiri', serif; font-size: 2.2rem; direction: rtl; line-height: 2.2;">
                <span class="feedback-green">قُلۡ</span> 
                <span class="feedback-green">هُوَ</span> 
                <span class="feedback-green">ٱللَّهُ</span> 
                <span class="feedback-yellow">أَحَدٌ</span> 
                <span class="feedback-red">ٱلصَّمَدُ</span>
            </div>
            <div style="margin-top: 1rem; font-size: 0.85rem; color: #94A3B8;">
                <span style="color: #10B981;">■ Correct</span> &nbsp;&nbsp;
                <span style="color: #F59E0B;">■ Minor Vowel Drift</span> &nbsp;&nbsp;
                <span style="color: #EF4444;">■ Makhraj Error</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with diag_col2:
        st.markdown("##### 💡 AI Correction Suggestions")
        st.error("**Word 5: ٱلصَّمَدُ**\n\nMissed the heavy 'ص' (Sad) sound. You pronounced it closer to 'س' (Sin). Focus on elevating the back of the tongue.")
        st.warning("**Word 4: أَحَدٌ**\n\nSlightly shortened the Qalqalah at the stop. Give the 'د' a sharper bounce.")

elif nav_option == "AI Companion":
    st.subheader("🤖 AI Quranic Study Assistant")
    st.caption("Ask complex questions regarding context, linguistic root words, or thematic connections.")
    
    # Mock Chat History
    st.chat_message("user").write("What is the central theme of Surah Al-Kahf?")
    st.chat_message("assistant").write("Surah Al-Kahf focuses on protection from tribulations through four major stories representing trials of Faith, Wealth, Knowledge, and Power.")
    
    st.chat_input("Ask a follow-up question...")

elif nav_option == "Browse Quran":
    st.subheader("📖 Browse Quran")
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("Select Surah", ["1. Al-Fatiha", "2. Al-Baqarah", "36. Ya-Sin", "67. Al-Mulk", "112. Al-Ikhlas"])
    with c2:
        st.number_input("Ayah Number", min_value=1, value=1)
    
    st.info("Surah content viewer container loaded.")
