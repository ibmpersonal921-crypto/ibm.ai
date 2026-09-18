"""
Quran Study Companion
----------------------
A Streamlit app for exploring the Quran, asking study questions to an
AI-assisted companion, and practicing recitation with instant feedback.

Run locally:
    streamlit run app.py
"""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from modules import quran_api
from modules.ai_scholar import ScholarChat, DISCLAIMER
from modules.recitation_coach import (
    transcribe_audio,
    transcribe_with_whisper,
    compare_to_reference,
    synthesize_feedback_audio,
)

load_dotenv()

# ----------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Quran Study Companion",
    page_icon="☾",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = Path(__file__).parent / "assets" / "style.css"
st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


def hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="qc-hero">
            <p class="qc-hero-arabic">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</p>
            <hr class="qc-hero-rule" />
            <p class="qc-hero-title">{title}</p>
            <p class="qc-hero-sub">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_label(text: str) -> None:
    st.markdown(f'<p class="qc-section-label">{text}</p>', unsafe_allow_html=True)


def disclaimer(text: str = DISCLAIMER) -> None:
    st.markdown(f'<div class="qc-disclaimer">{text}</div>', unsafe_allow_html=True)


# ----------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ☾ Quran Study Companion")
    st.caption("An educational companion, not a religious authority.")
    page = st.radio(
        "Navigate",
        ["Home", "Browse Quran", "AI Study Companion", "Recitation Coach"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption(
        f"AI provider: **{os.getenv('AI_PROVIDER', 'anthropic')}**  \n"
        "Set keys in your `.env` file."
    )

# ----------------------------------------------------------------------
# HOME
# ----------------------------------------------------------------------
if page == "Home":
    hero(
        "Quran Study Companion",
        "Explore the Quran with verified text and translations, ask an AI study "
        "companion questions grounded in real verses, and practice your recitation "
        "with instant, word-level feedback.",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="qc-card"><b>📖 Browse Quran</b><br>'
            "Read any surah with Arabic text and translation, verse by verse, "
            "with audio recitation.</div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="qc-card"><b>💬 AI Study Companion</b><br>'
            "Ask questions about meaning and context. Answers are grounded in "
            "fetched verses and always cite their source.</div>",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="qc-card"><b>🎙️ Recitation Coach</b><br>'
            "Record yourself reciting a verse and get instant word-level "
            "accuracy feedback.</div>",
            unsafe_allow_html=True,
        )

    disclaimer(
        "This app is a study aid built on AI and public Quran data sources. "
        "It is not a substitute for a qualified human teacher or scholar, "
        "especially for matters of correct tajweed, fiqh, or religious rulings."
    )

# ----------------------------------------------------------------------
# BROWSE QURAN
# ----------------------------------------------------------------------
elif page == "Browse Quran":
    hero("Browse the Quran", "Verified Arabic text (Uthmani script) with translation.")

    surahs = quran_api.get_surah_list()
    surah_labels = [f"{s['number']}. {s['englishName']} ({s['name']})" for s in surahs]

    section_label("SELECT A SURAH")
    choice = st.selectbox("Surah", surah_labels, label_visibility="collapsed")
    surah_number = int(choice.split(".")[0])

    translation_edition = st.selectbox(
        "Translation",
        ["en.sahih", "en.pickthall", "en.yusufali"],
        format_func=lambda e: {
            "en.sahih": "Saheeh International (English)",
            "en.pickthall": "Pickthall (English)",
            "en.yusufali": "Yusuf Ali (English)",
        }[e],
    )

    arabic_surah = quran_api.get_surah(surah_number, quran_api.ARABIC_EDITION)
    translated_surah = quran_api.get_surah(surah_number, translation_edition)

    st.write("")
    for ar_ayah, tr_ayah in zip(arabic_surah["ayahs"], translated_surah["ayahs"]):
        st.markdown(
            f"""
            <div class="qc-card">
                <span class="qc-verse-ref">{surah_number}:{ar_ayah['numberInSurah']}</span>
                <div class="qc-verse-arabic">{ar_ayah['text']}</div>
                <div class="qc-verse-translation">{tr_ayah['text']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        audio_url = quran_api.get_audio_url(surah_number, ar_ayah["numberInSurah"])
        st.audio(audio_url)

# ----------------------------------------------------------------------
# AI STUDY COMPANION
# ----------------------------------------------------------------------
elif page == "AI Study Companion":
    hero("AI Study Companion", "Ask about meaning, context, and language — grounded in real verses.")
    disclaimer()

    if "chat" not in st.session_state:
        st.session_state.chat = ScholarChat()

    for msg in st.session_state.chat.history:
        css_class = "qc-chat-user" if msg.role == "user" else "qc-chat-ai"
        label = "You" if msg.role == "user" else "Study Companion"
        st.markdown(
            f'<div class="{css_class}"><b>{label}:</b><br>{msg.content}</div>',
            unsafe_allow_html=True,
        )

    question = st.chat_input("Ask about a verse, a theme, or historical context…")
    if question:
        with st.spinner("Searching verses and thinking…"):
            try:
                matches = quran_api.search_quran(question)
                context = "\n".join(
                    f"- ({m['surah']['englishName']} {m['surah']['number']}:{m['numberInSurah']}): {m['text']}"
                    for m in matches[:5]
                ) or None
            except Exception:
                context = None

            try:
                st.session_state.chat.ask(question, verse_context=context)
            except Exception as e:
                st.error(
                    f"Couldn't reach the AI provider ({e}). Check your API key in `.env`."
                )
        st.rerun()

# ----------------------------------------------------------------------
# RECITATION COACH
# ----------------------------------------------------------------------
elif page == "Recitation Coach":
    hero("Recitation Coach", "Record a verse, get instant word-level feedback.")
    disclaimer(
        "This tool checks whether the *words* you said match the verse. It does not "
        "assess tajweed (proper pronunciation rules) — for that, please learn with a "
        "qualified teacher."
    )

    surahs = quran_api.get_surah_list()
    surah_labels = [f"{s['number']}. {s['englishName']} ({s['name']})" for s in surahs]

    col_a, col_b = st.columns(2)
    with col_a:
        section_label("1. CHOOSE A VERSE")
        choice = st.selectbox("Surah", surah_labels, key="rc_surah")
        surah_number = int(choice.split(".")[0])
        ayah_number = st.number_input("Ayah number", min_value=1, value=1, step=1)

    try:
        reference = quran_api.get_ayah(surah_number, ayah_number, quran_api.ARABIC_EDITION)
        reference_text = reference["text"]
    except Exception:
        st.error("Couldn't fetch that verse. Check the ayah number for this surah.")
        st.stop()

    with col_b:
        section_label("REFERENCE VERSE")
        st.markdown(
            f'<div class="qc-card"><div class="qc-verse-arabic">{reference_text}</div></div>',
            unsafe_allow_html=True,
        )
        st.audio(quran_api.get_audio_url(surah_number, ayah_number))
        st.caption("Listen first, then record your own recitation below.")

    st.divider()
    section_label("2. RECORD YOUR RECITATION")
    audio_value = st.audio_input("Tap to record")

    if audio_value is not None:
        with st.spinner("Transcribing your recitation…"):
            audio_bytes = audio_value.read()
            use_whisper = bool(os.getenv("OPENAI_API_KEY")) and st.toggle(
                "Use Whisper (higher accuracy, needs OpenAI key)", value=False
            )
            try:
                transcribed = (
                    transcribe_with_whisper(audio_bytes)
                    if use_whisper
                    else transcribe_audio(audio_bytes)
                )
            except Exception as e:
                st.error(f"Transcription failed: {e}")
                st.stop()

        if not transcribed:
            st.warning("Couldn't make out any speech — try recording again, closer to the mic.")
        else:
            result = compare_to_reference(transcribed, reference_text)

            col_x, col_y = st.columns([1, 2])
            with col_x:
                st.markdown(
                    f"""
                    <div class="qc-card" style="text-align:center;">
                        <div class="qc-accuracy-big">{result.accuracy_pct}%</div>
                        <div class="qc-accuracy-label">word match accuracy</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_y:
                st.markdown(
                    f'<div class="qc-card"><b>Feedback</b><br>{result.feedback_message}</div>',
                    unsafe_allow_html=True,
                )
                if result.missed_words:
                    st.markdown(
                        f'<div class="qc-card"><b>Words to review</b><br>'
                        f'<span class="qc-verse-arabic" style="font-size:1.3rem;">'
                        f'{" ".join(result.missed_words)}</span></div>',
                        unsafe_allow_html=True,
                    )

            feedback_audio = synthesize_feedback_audio(result.feedback_message)
            st.audio(feedback_audio, format="audio/mp3")
