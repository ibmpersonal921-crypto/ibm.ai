import streamlit as st
import os
from utils.quran_api import get_surah_list, get_surah_data, get_daily_verse, RECITERS
from utils.ai_bot import query_quran_ai
from utils.audio_coach import analyze_recitation
from streamlit_mic_recorder import mic_recorder

# Set Page Config
st.set_page_config(
    page_title="Quran Study Companion",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom Emerald CSS Styling
with open("styles/emerald_theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Session State
if "points" not in st.session_state:
    st.session_state.points = 120
if "streak" not in st.session_state:
    st.session_state.streak = 5
if "completed_goals" not in st.session_state:
    st.session_state.completed_goals = set()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Navigation Sidebar
with st.sidebar:
    st.markdown("## 📖 Quran Study Companion")
    st.caption("Read · Listen · Reflect")
    st.markdown("---")
    
    nav = st.radio(
        "Navigation",
        ["🏠 Home Dashboard", "📖 Browse Quran", "🧠 AI Companion", "🎙️ Recitation Coach"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    # Gamification Sidebar Metrics
    st.markdown("### 🏆 User Progress")
    col_a, col_b = st.columns(2)
    col_a.metric("Points", f"{st.session_state.points} XP")
    col_b.metric("Streak", f"{st.session_state.streak} Days")
    
    st.markdown("---")
    st.markdown("⚙️ **Settings**")
    selected_reciter_name = st.selectbox("Preferred Reciter", list(RECITERS.keys()))
    selected_reciter_id = RECITERS[selected_reciter_name]

# HOME DASHBOARD
if nav == "🏠 Home Dashboard":
    st.markdown("<h1>Dashboard</h1>", unsafe_allow_html=True)
    
    # Verse of the Day Card
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(15, 40, 30, 0.8) 0%, rgba(8, 24, 18, 0.95) 100%);
                border: 1px solid rgba(52, 211, 153, 0.25); border-radius: 20px; padding: 25px; margin-bottom: 25px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <span style="color: #34D399; font-weight: 600;">Verse of the Day</span>
            <span style="color: #CBD5E0; font-size: 14px;">Surah An-Nasr (110:1-3)</span>
        </div>
        <div class="arabic-text">
            بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ<br>
            إِذَا جَآءَ نَصْرُ ٱللَّهِ وَٱلْفَتْحُ ﴿١﴾ وَرَأَيْتَ ٱلنَّاسَ يَدْخُلُونَ فِى دِينِ ٱللَّهِ أَفْوَاجًـا ﴿٢﴾ فَسَبِّحْ بِحَمْدِ رَبِّكَ وَٱسْتَغْفِرْهُ ۚ إِنَّهُۥ كَانَ تَوَّابًـا ﴿٣﴾
        </div>
        <div class="transliteration">
            Iza jaa-a nasrullahi walfath. Wa ra-aitan naasa yadkhuloona fee deenil laahi afwaaja. Fa sabbih bihamdi rabbika was taghfir, innahu kaana tawwaaba.
        </div>
        <div class="translation">
            When the victory of Allah has come and the conquest, And you see the people entering into the religion of Allah in multitudes, Then exalt [Him] with praise of your Lord and ask forgiveness of Him. Indeed, He is ever Accepting of repentance.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Daily Goals Section
    st.markdown("### 🎯 Daily Goals & Target Learning")
    
    goals = [
        ("goal_1", "Learn Verse of the Day (Surah An-Nasr) (+20 XP)"),
        ("goal_2", "Recite 1 Page with Live AI Coach (+30 XP)"),
        ("goal_3", "Ask AI Companion a Tafseer Question (+10 XP)")
    ]
    
    progress = len(st.session_state.completed_goals) / len(goals)
    st.progress(progress)
    
    for g_id, g_label in goals:
        checked = g_id in st.session_state.completed_goals
        if st.checkbox(g_label, value=checked, key=g_id):
            if g_id not in st.session_state.completed_goals:
                st.session_state.completed_goals.add(g_id)
                st.session_state.points += 20
                st.rerun()

# BROWSE QURAN
elif nav == "📖 Browse Quran":
    st.markdown("<h1>Browse Quran</h1>", unsafe_allow_html=True)
    
    surahs = get_surah_list()
    if surahs:
        surah_options = {f"{s['number']}. {s['englishName']} ({s['name']})": s['number'] for s in surahs}
        selected_surah_str = st.selectbox("Select Surah", list(surah_options.keys()))
        surah_num = surah_options[selected_surah_str]
        
        data = get_surah_data(surah_num, selected_reciter_id)
        if data:
            st.markdown(f"### Audio Recitation by {selected_reciter_name}")
            # Global Surah Audio Stream
            st.audio(data["audio"][0]["audio"], format="audio/mp3")
            
            st.markdown("---")
            for i in range(len(data["arabic"])):
                st.markdown(f"""
                <div style="background: rgba(15, 40, 30, 0.5); border-radius: 15px; padding: 18px; margin-bottom: 15px; border: 1px solid rgba(52, 211, 153, 0.15);">
                    <div style="color: #34D399; font-size: 13px;">Verse {data['arabic'][i]['numberInSurah']}</div>
                    <div class="arabic-text">{data['arabic'][i]['text']}</div>
                    <div class="translation">{data['english'][i]['text']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.audio(data["audio"][i]["audio"], format="audio/mp3")

# AI CHATBOT COMPANION
elif nav == "🧠 AI Companion":
    st.markdown("<h1>Quran & Hadith AI Scholar</h1>", unsafe_allow_html=True)
    st.caption("Ask questions on Tafseer, Tajweed rules, or Sahih Hadith rulings.")
    
    # Render Chat
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("Ask e.g., 'What is the significance of Ayat Al-Kursi?'"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Searching Quran & Sahih Hadith sources..."):
                response = query_quran_ai(prompt, st.session_state.chat_history[:-1])
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

# LIVE VOICE RECITATION COACH
elif nav == "🎙️ Recitation Coach":
    st.markdown("<h1>Live AI Recitation Coach</h1>", unsafe_allow_html=True)
    st.write("Recite the verse live. The AI evaluates your **Talaffuz** (pronunciation) and **Tahajji** (phonetics) with voice feedback in Urdu and English.")
    
    target_verse = "إِذَا جَآءَ نَصْرُ ٱللَّهِ وَٱلْفَتْحُ"
    
    st.markdown(f"""
    <div style="background: rgba(15, 40, 30, 0.8); border-radius: 16px; padding: 20px; border: 1px solid #34D399; text-align: center; margin-bottom: 20px;">
        <span style="color: #9AE6B4;">Practice Target Verse:</span>
        <div class="arabic-text">{target_verse}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎙️ Record Live Voice Input")
    audio = mic_recorder(
        start_prompt="🔴 Start Reciting Live Call",
        stop_prompt="⏹️ End Recording & Evaluate",
        key="recitation_recorder"
    )
    
    if audio:
        st.audio(audio["bytes"], format="audio/webm")
        with st.spinner("Analyzing pronunciation and generating Urdu voice feedback..."):
            spoken, feedback, urdu_audio = analyze_recitation(audio["bytes"], target_verse)
            
            st.markdown(f"**Recognized Speech:** `{spoken}`")
            st.markdown("### 📋 AI Coach Assessment")
            st.write(feedback)
            
            if urdu_audio:
                st.markdown("### 🔊 Urdu Voice Feedback")
                st.audio(urdu_audio, format="audio/mp3")
