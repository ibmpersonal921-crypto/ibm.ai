import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Quran Study Companion",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Session State Setup for "Opening" Views
if "opened_surah" not in st.session_state:
    st.session_state.opened_surah = None
if "show_tafsir" not in st.session_state:
    st.session_state.show_tafsir = False
if "audio_playing" not in st.session_state:
    st.session_state.audio_playing = False

# 3. Custom CSS (Emerald Dark Theme & Custom Action Styling)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        background-color: #121A22;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E161F 0%, #0A1C18 100%);
        border-right: 1px solid rgba(45, 212, 191, 0.15);
    }
    
    .sidebar-brand {
        color: #D4AF37;
        font-size: 1.25rem;
        font-weight: 700;
        padding: 0.5rem 0 1.2rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.2rem;
    }

    .app-card {
        background: linear-gradient(135deg, #16222F 0%, #0D2621 100%);
        border: 1px solid rgba(45, 212, 191, 0.22);
        border-radius: 14px;
        padding: 1.8rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
        margin-bottom: 1.2rem;
    }

    .verse-meta {
        color: #D4AF37;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    .arabic-text {
        font-family: 'Amiri', serif;
        font-size: 2.2rem;
        line-height: 2.3;
        text-align: right;
        direction: rtl;
        color: #FFFFFF;
        margin-bottom: 1rem;
    }

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
    
    .status-badge {
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

# 4. Sidebar Navigation
with st.sidebar:
    st.markdown('<div class="sidebar-brand">📖 Quran Companion</div>', unsafe_allow_html=True)
    
    nav_option = st.radio(
        "Navigation",
        ["Dashboard", "Live Recitation Coach", "AI Companion", "Browse Quran"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("##### 🎙️ Voice Model Engine")
    st.caption("Engine: **Tajweed-Net v2.4 (Live)**")
    st.markdown('<span class="status-badge">● Engine Online</span>', unsafe_allow_html=True)

# 5. Top Bar AI Search
search_col1, search_col2 = st.columns([4, 1])
with search_col1:
    search_input = st.text_input(
        "AI Search",
        placeholder="🔍 Type to search or ask AI (e.g., 'Open Surah Mulk', 'Verses about patience')...",
        label_visibility="collapsed"
    )
with search_col2:
    if st.button("✨ Search / Ask", use_container_width=True):
        if search_input:
            st.toast(f"Searching query: '{search_input}'", icon="🔍")

st.markdown("<br>", unsafe_allow_html=True)

# 6. Navigation Views
if nav_option == "Dashboard":
    st.markdown("""
    <div class="app-card">
        <div class="verse-meta">Verse of the Day • Surah Al-Fatiha (1:1-3)</div>
        <div class="arabic-text">
            ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ ۝ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ ۝ مَٰلِكِ يَوۡمِ ٱلدِّينِ
        </div>
        <p style="color: #CBD5E1; font-size: 1rem; margin-top: 1rem;">
            "All praise is due to Allah, Lord of the worlds — The Entirely Merciful, the Especially Merciful — Sovereign of the Day of Recompense."
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Interactive Action Buttons
    action_col1, action_col2, action_col3 = st.columns(3)
    with action_col1:
        if st.button("📖 Open Full Surah Al-Fatiha", use_container_width=True):
            st.session_state.opened_surah = "1. Al-Fatiha"
            st.toast("Opening Surah Al-Fatiha view...", icon="📂")
    with action_col2:
        if st.button("💡 Open AI Tafsir Analysis", use_container_width=True):
            st.session_state.show_tafsir = not st.session_state.show_tafsir
    with action_col3:
        if st.button("▶ Open Audio Player", use_container_width=True):
            st.session_state.audio_playing = True

    # Expandable Tafsir Panel
    if st.session_state.show_tafsir:
        with st.expander("📖 Detailed Tafsir & Linguistic Insights", expanded=True):
            st.markdown("""
            **Key Insights for Surah Al-Fatiha (Verses 1-3):**
            * **Rabb (رَبِّ):** Implies ownership, nurturing, and sustaining everything in existence.
            * **Ar-Rahman vs Ar-Rahim:** *Ar-Rahman* refers to all-encompassing mercy for all creation, while *Ar-Rahim* emphasizes specific, continuous mercy.
            """)

    # Audio Player Bar
    if st.session_state.audio_playing:
        st.info("🎵 Playing Recitation: **Mishary Rashid Alafasy**")
        st.slider("Audio Progress", 0, 100, 30, label_visibility="collapsed")

    st.divider()
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Reading Streak", "7 Days", "+1 today")
    with m2:
        st.metric("Tajweed Accuracy", "94%", "+2%")
    with m3:
        st.metric("Verses Memorized", "128", "+5 this week")

elif nav_option == "Live Recitation Coach":
    st.subheader("🎙️ Live AI Recitation & Voice Test")
    st.caption("Read the prompt aloud into your microphone to get real-time tajweed corrections.")

    st.markdown("""
    <div class="app-card">
        <div class="verse-meta">Target Verse: Surah Al-Ikhlas (112:1-2)</div>
        <div class="arabic-text">
            قُلۡ هُوَ ٱللَّهُ أَحَدٌ ۝ ٱللَّهُ ٱلصَّمَدُ
        </div>
    </div>
    """, unsafe_allow_html=True)

    rec_col1, rec_col2 = st.columns([1, 2])
    with rec_col1:
        start_rec = st.button("🔴 Start Live Voice Test", type="primary", use_container_width=True)
    with rec_col2:
        if start_rec:
            st.progress(85, text="🎙️ Listening & analyzing speech phonemes...")

    st.markdown("### 📊 Live AI Pronunciation Feedback")
    
    st.markdown("""
    <div class="recitation-box">
        <h5 style="color: #94A3B8; margin-bottom: 1rem;">Phoneme Diagnostics</h5>
        <div style="font-family: 'Amiri', serif; font-size: 2.2rem; direction: rtl; line-height: 2.2;">
            <span class="feedback-green">قُلۡ</span> 
            <span class="feedback-green">هُوَ</span> 
            <span class="feedback-green">ٱللَّهُ</span> 
            <span class="feedback-yellow">أَحَدٌ</span> 
            <span class="feedback-red">ٱلصَّمَدُ</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Open Diagnostics Expander
    with st.expander("🔍 Open Full Tajweed Breakdown & Correction Steps"):
        st.error("**Makhraj Error on 'ٱلصَّمَدُ':** Heavy 'ص' was softened into 'س'. Focus on tongue elevation.")
        st.warning("**Qalqalah Notice on 'أَحَدٌ':** Make the stopping bounce cleaner at the end of the verse.")

elif nav_option == "Browse Quran":
    st.subheader("📖 Browse & Read Surahs")
    
    surah_list = [
        {"id": 1, "name": "Al-Fatiha", "arabic": "الفاتحة", "verses": 7, "type": "Meccan"},
        {"id": 2, "name": "Al-Baqarah", "arabic": "البقرة", "verses": 286, "type": "Medinan"},
        {"id": 36, "name": "Ya-Sin", "arabic": "يس", "verses": 83, "type": "Meccan"},
        {"id": 67, "name": "Al-Mulk", "arabic": "الملك", "verses": 30, "type": "Meccan"},
        {"id": 112, "name": "Al-Ikhlas", "arabic": "الإخلاص", "verses": 4, "type": "Meccan"},
    ]

    # Grid Display of Surahs with "Open" Action
    for item in surah_list:
        with st.container():
            col_info, col_btn = st.columns([4, 1])
            with col_info:
                st.markdown(f"**{item['id']}. {item['name']}** ({item['arabic']}) — *{item['verses']} Verses • {item['type']}*")
            with col_btn:
                if st.button(f"Open Surah", key=f"open_{item['id']}"):
                    st.session_state.opened_surah = f"{item['id']}. {item['name']}"
            st.divider()

    # Opened Surah Reader View
    if st.session_state.opened_surah:
        st.success(f"📂 Currently Reading: **Surah {st.session_state.opened_surah}**")
        with st.expander("📖 Open Full Text & Recitation View", expanded=True):
            st.markdown("""
            <div class="arabic-text">
                بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ <br>
                قُلۡ هُوَ ٱللَّهُ أَحَدٌ ۝ ٱللَّهُ ٱلصَّمَدُ ۝ لَمۡ يَلِدۡ وَلَمۡ يُولَدۡ ۝ وَلَمۡ يَكُن لَّهُۥ كُفُوًا أَحَدٌ
            </div>
            """, unsafe_allow_html=True)
            st.audio("https://server8.mp3quran.net/afs/112.mp3")

elif nav_option == "AI Companion":
    st.subheader("🤖 AI Quranic Study Assistant")
    st.caption("Ask questions about verse context, root words, or thematic analysis.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Assalamu Alaikum! How can I assist your Quran study today?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask anything about Surahs, Tafsir, or Tajweed rules..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        reply = f"Here are the study insights for: '{prompt}'."
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
