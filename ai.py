"""
Quran Study Companion
=====================

A single-file Streamlit app matching the dark charcoal / emerald / gold mockup.

Run:
    pip install streamlit requests
    streamlit run quran_study_companion.py

Optional (for the AI Companion page):
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...

Scripture text is never hard-coded beyond a verified Al-Fatiha fallback; everything
else is fetched from the AlQuran Cloud API (Tanzil Uthmani text) so the Arabic is
always authoritative rather than transcribed by hand.
"""

from __future__ import annotations

import datetime as dt
import json
import os

import requests
import streamlit as st
import streamlit.components.v1 as components

# --------------------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------------------

API_BASE = "https://api.alquran.cloud/v1"
AUDIO_BASE = "https://everyayah.com/data"

RECITERS = {
    "Mishary Alafasy": "Alafasy_128kbps",
    "Abdul Basit (murattal)": "Abdul_Basit_Murattal_192kbps",
    "Mahmoud Khalil Al-Husary": "Husary_128kbps",
    "Mohamed Siddiq El-Minshawi": "Minshawy_Murattal_128kbps",
    "Abdurrahman As-Sudais": "Abdurrahmaan_As-Sudais_192kbps",
}

TRANSLATIONS = {
    "Saheeh International": "en.sahih",
    "Muhammad Asad": "en.asad",
    "Abdullah Yusuf Ali": "en.yusufali",
    "Marmaduke Pickthall": "en.pickthall",
}

# Verse-of-the-day rotation. References only — the text itself comes from the API.
# Keep every passage to roughly four verses so the card fits on one screen without
# scrolling; longer surahs belong on Browse, not the dashboard.
DAILY_ROTATION = [
    (112, 1, 4),    # Al-Ikhlas
    (103, 1, 3),    # Al-'Asr
    (2, 255, 255),  # Ayat al-Kursi
    (94, 5, 6),     # with hardship comes ease
    (108, 1, 3),    # Al-Kawthar
    (13, 28, 28),   # hearts settle in remembrance
    (67, 1, 2),     # Al-Mulk, opening
    (39, 53, 53),   # do not despair
    (110, 1, 3),    # An-Nasr
    (55, 1, 4),     # Ar-Rahman, opening
    (49, 13, 13),   # made into peoples and tribes
    (93, 1, 5),     # Ad-Duha
    (2, 286, 286),  # closing of Al-Baqarah
    (36, 1, 4),     # Ya-Sin, opening
    (113, 1, 5),    # Al-Falaq
]

MAX_DAILY_AYAHS = 6  # hard stop, in case the rotation ever grows a long entry

# Verified Uthmani text, used only if the network is unavailable.
FATIHA_FALLBACK = {
    "number": 1,
    "englishName": "Al-Fatiha",
    "name": "الفاتحة",
    "englishNameTranslation": "The Opening",
    "revelationType": "Meccan",
    "numberOfAyahs": 7,
    "ayahs": [
        {
            "numberInSurah": 1,
            "arabic": "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
            "translation": "In the name of God, the Most Gracious, the Most Merciful.",
            "transliteration": "Bismi llāhi r-raḥmāni r-raḥīm",
        },
        {
            "numberInSurah": 2,
            "arabic": "ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَٰلَمِينَ",
            "translation": "All praise is due to God, Lord of all the worlds.",
            "transliteration": "Al-ḥamdu li-llāhi rabbi l-ʿālamīn",
        },
        {
            "numberInSurah": 3,
            "arabic": "ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
            "translation": "The Most Gracious, the Most Merciful.",
            "transliteration": "Ar-raḥmāni r-raḥīm",
        },
        {
            "numberInSurah": 4,
            "arabic": "مَٰلِكِ يَوْمِ ٱلدِّينِ",
            "translation": "Master of the Day of Judgement.",
            "transliteration": "Māliki yawmi d-dīn",
        },
        {
            "numberInSurah": 5,
            "arabic": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
            "translation": "You alone we worship, and You alone we ask for help.",
            "transliteration": "Iyyāka naʿbudu wa-iyyāka nastaʿīn",
        },
        {
            "numberInSurah": 6,
            "arabic": "ٱهْدِنَا ٱلصِّرَٰطَ ٱلْمُسْتَقِيمَ",
            "translation": "Guide us along the straight path —",
            "transliteration": "Ihdinā ṣ-ṣirāṭa l-mustaqīm",
        },
        {
            "numberInSurah": 7,
            "arabic": (
                "صِرَٰطَ ٱلَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ ٱلْمَغْضُوبِ "
                "عَلَيْهِمْ وَلَا ٱلضَّآلِّينَ"
            ),
            "translation": (
                "the path of those You have blessed, not of those who have incurred "
                "anger, nor of those who have gone astray."
            ),
            "transliteration": (
                "Ṣirāṭa lladhīna anʿamta ʿalayhim ghayri l-maghḍūbi ʿalayhim "
                "wa-lā ḍ-ḍāllīn"
            ),
        },
    ],
}


# --------------------------------------------------------------------------------------
# Page setup + theme
# --------------------------------------------------------------------------------------

st.set_page_config(
    page_title="Quran Study Companion",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri+Quran&family=Inter:wght@300;400;500;600&display=swap');

:root {
  --bg:        #121A22;
  --panel:     #0D141A;
  --card-a:    #16241F;
  --card-b:    #101A22;
  --gold:      #D4AF37;
  --gold-soft: rgba(212, 175, 55, 0.16);
  --emerald:   #1E4638;
  --ink:       #ECEAE4;
  --muted:     #9DAEB4;
  --line:      rgba(212, 175, 55, 0.14);
}

/* ---- shell ---- */
[data-testid="stAppViewContainer"] { background: var(--bg); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { right: 1rem; }
footer, #MainMenu { visibility: hidden; }

.block-container { padding: 1.6rem 2.4rem 4rem; max-width: 1180px; }

/* Scope this narrowly. A blanket [class*="st-"] rule also hits Streamlit's icon
   spans, which set their glyph via an emotion class — override their font and the
   ligature name ("arrow_drop_down") prints as literal text next to every expander
   and select. */
html, body, button, input, textarea,
[data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"],
div[data-baseweb="select"], [data-testid="stExpander"] summary {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
body, p, label, li { color: var(--ink); }

[data-testid="stIconMaterial"], [data-testid="stExpanderToggleIcon"],
.material-icons, .material-icons-outlined, [data-baseweb="icon"] i {
  font-family: 'Material Symbols Rounded', 'Material Icons' !important;
  font-size: 20px;
}
[data-testid="stExpander"] summary {
  font-size: 13px; color: var(--muted); padding: .5rem .85rem;
}
[data-testid="stExpander"] summary:hover { color: var(--ink); }

/* ---- sidebar ---- */
section[data-testid="stSidebar"] {
  background: var(--panel);
  border-right: 1px solid rgba(255,255,255,0.05);
}
section[data-testid="stSidebar"] > div { padding-top: 1.4rem; }

.brand { display: flex; gap: 12px; align-items: center; padding: 0 4px 22px; }
.brand-mark { font-size: 26px; line-height: 1; }
.brand-name { font-size: 15px; font-weight: 600; letter-spacing: .1px; line-height: 1.25; }
.brand-sub { font-size: 11.5px; color: var(--muted); margin-top: 2px; }

section[data-testid="stSidebar"] .stButton > button,
section[data-testid="stSidebar"] button[data-testid^="stBaseButton"] {
  width: 100%;
  text-align: left;
  justify-content: flex-start;
  background: transparent;
  border: 1px solid transparent;
  color: var(--muted);
  font-size: 13.5px;
  font-weight: 400;
  padding: .55rem .8rem;
  border-radius: 9px;
  transition: background .15s ease, color .15s ease;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(255,255,255,0.04);
  color: var(--ink);
  border-color: transparent;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {
  background: linear-gradient(90deg, rgba(30,70,56,.75), rgba(30,70,56,.25));
  border: 1px solid var(--gold-soft);
  color: var(--ink);
  font-weight: 500;
}
section[data-testid="stSidebar"] .stButton > button:focus-visible {
  outline: 2px solid var(--gold); outline-offset: 2px;
}

/* ---- header row ---- */
.page-title { font-size: 21px; font-weight: 500; margin: 2px 0 0; letter-spacing: .2px; }

/* ---- verse card ---- */
.card {
  background: linear-gradient(145deg, var(--card-a) 0%, #132019 45%, var(--card-b) 100%);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 22px 26px 18px;
  margin-bottom: 18px;
}
.card-head {
  display: flex; justify-content: space-between; align-items: baseline;
  font-size: 13.5px; color: var(--muted); margin-bottom: 20px;
}
.card-head .ref { color: var(--gold); }

.arabic {
  font-family: 'Amiri Quran', 'Scheherazade New', serif;
  direction: rtl;
  text-align: center;
  color: #F3EFE4;
  line-height: 2.25;
  max-width: 34ch;
  margin: 6px auto 22px;
}
.translit, .translation { margin-left: auto; margin-right: auto; }
.ayah-mark {
  color: var(--gold);
  font-size: .62em;
  padding: 0 .28em;
  opacity: .85;
}
.translit {
  font-size: 13.5px; color: var(--muted); line-height: 1.8;
  max-width: 68ch; font-style: italic; margin-bottom: 10px;
}
.translation { font-size: 14.5px; line-height: 1.75; max-width: 68ch; color: var(--ink); }

/* ---- ayah rows (Browse) ---- */
.ayah-row {
  border-bottom: 1px solid rgba(255,255,255,0.05);
  padding: 20px 2px 22px;
}
.ayah-row:last-child { border-bottom: none; }
.ayah-num {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 30px; height: 24px; padding: 0 8px;
  border: 1px solid var(--gold-soft); border-radius: 999px;
  font-size: 11.5px; color: var(--gold);
}

/* ---- stat tiles ---- */
.tile {
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.055);
  border-radius: 13px; padding: 15px 17px; height: 100%;
}
.tile-label { font-size: 12px; color: var(--muted); }
.tile-value { font-size: 21px; font-weight: 500; margin-top: 5px; }
.tile-note  { font-size: 11.5px; color: var(--muted); margin-top: 3px; }

/* ---- inputs ---- */
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
  background: rgba(255,255,255,0.035);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 999px;
  color: var(--ink);
  font-size: 13px;
  padding: .5rem 1rem;
}
[data-testid="stTextArea"] textarea { border-radius: 12px; }
[data-testid="stTextInput"] input:focus { border-color: var(--gold-soft); box-shadow: none; }
[data-testid="stTextInput"] input::placeholder { color: #7B8B92; }

div[data-baseweb="select"] > div {
  background: rgba(255,255,255,0.035);
  border-color: rgba(255,255,255,0.08);
  border-radius: 10px;
  font-size: 13px;
}
[data-testid="stSlider"] [role="slider"] { background: var(--gold); }

/* ---- main-area buttons ---- */
.block-container .stButton > button {
  background: rgba(255,255,255,0.035);
  border: 1px solid rgba(255,255,255,0.09);
  color: var(--ink);
  border-radius: 9px;
  font-size: 13px;
  padding: .4rem .9rem;
}
.block-container .stButton > button:hover {
  border-color: var(--gold-soft); color: var(--gold);
}
.block-container .stButton > button[kind="primary"] {
  background: var(--gold); border-color: var(--gold); color: #101A16; font-weight: 500;
}

/* ---- chat ---- */
[data-testid="stChatMessage"] {
  background: rgba(255,255,255,0.028);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 13px;
}
[data-testid="stExpander"] details {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 11px;
}

hr { border-color: rgba(255,255,255,0.06); }
.small-note { font-size: 12px; color: var(--muted); line-height: 1.6; }

@media (max-width: 760px) {
  .block-container { padding: 1rem 1rem 3rem; }
  .card { padding: 18px 16px 14px; }
}
@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# --------------------------------------------------------------------------------------
# Data layer
# --------------------------------------------------------------------------------------


@st.cache_data(ttl=86_400, show_spinner=False)
def fetch_surah_index() -> list[dict] | None:
    """The 114-surah table of contents."""
    try:
        r = requests.get(f"{API_BASE}/surah", timeout=12)
        r.raise_for_status()
        return r.json()["data"]
    except Exception:
        return None


@st.cache_data(ttl=86_400, show_spinner=False)
def fetch_surah(number: int, translation_id: str) -> dict | None:
    """Uthmani text + translation + transliteration for one surah."""
    editions = f"quran-uthmani,{translation_id},en.transliteration"
    try:
        r = requests.get(f"{API_BASE}/surah/{number}/editions/{editions}", timeout=15)
        r.raise_for_status()
        blocks = r.json()["data"]
    except Exception:
        return FATIHA_FALLBACK if number == 1 else None

    arabic, translated, translit = blocks[0], blocks[1], blocks[2]
    ayahs = []
    for i, a in enumerate(arabic["ayahs"]):
        ayahs.append(
            {
                "numberInSurah": a["numberInSurah"],
                "arabic": a["text"],
                "translation": translated["ayahs"][i]["text"],
                "transliteration": translit["ayahs"][i]["text"],
            }
        )
    return {
        "number": arabic["number"],
        "englishName": arabic["englishName"],
        "name": arabic["name"],
        "englishNameTranslation": arabic["englishNameTranslation"],
        "revelationType": arabic["revelationType"],
        "numberOfAyahs": arabic["numberOfAyahs"],
        "ayahs": ayahs,
    }


def audio_url(surah: int, ayah: int, reciter_key: str) -> str:
    return f"{AUDIO_BASE}/{reciter_key}/{surah:03d}{ayah:03d}.mp3"


def arabic_numeral(n: int) -> str:
    return str(n).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))


def verse_of_the_day() -> tuple[int, int, int]:
    idx = dt.date.today().toordinal() % len(DAILY_ROTATION)
    return DAILY_ROTATION[idx]


# --------------------------------------------------------------------------------------
# Custom audio player (styled to match the mockup; st.audio can't be restyled)
# --------------------------------------------------------------------------------------

PLAYER_TEMPLATE = """
<style>
* { box-sizing: border-box; }
body { margin: 0; background: transparent;
       font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.player {
  display: flex; align-items: center; gap: 14px;
  padding: 13px 18px; border-radius: 13px;
  background: rgba(8, 14, 12, 0.55);
  border: 1px solid rgba(212, 175, 55, 0.13);
}
button { cursor: pointer; border: none; background: none; color: #C3D1D4;
         display: flex; align-items: center; justify-content: center; padding: 0; }
button:focus-visible { outline: 2px solid #D4AF37; outline-offset: 3px; border-radius: 6px; }
.skip { width: 26px; height: 26px; }
.skip:hover { color: #ECEAE4; }
.skip svg { width: 17px; height: 17px; }
.play { width: 40px; height: 40px; border-radius: 50%; background: #D4AF37; color: #10190F;
        flex: 0 0 auto; }
.play svg { width: 17px; height: 17px; margin-left: 1px; }
.track { flex: 1; min-width: 80px; }
.meta { display: flex; justify-content: space-between; font-size: 11px;
        color: #93A5AB; margin-top: 6px; }
input[type=range] { -webkit-appearance: none; appearance: none; width: 100%;
                    height: 3px; border-radius: 3px; background: rgba(212,175,55,0.22);
                    outline: none; cursor: pointer; }
input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 11px; height: 11px;
  border-radius: 50%; background: #D4AF37; }
input[type=range]::-moz-range-thumb { width: 11px; height: 11px; border: none;
  border-radius: 50%; background: #D4AF37; }
.speed { display: flex; align-items: center; gap: 7px; font-size: 12px; color: #93A5AB; }
.chip { width: 25px; height: 25px; border-radius: 7px; font-size: 15px;
        border: 1px solid rgba(212,175,55,0.24); color: #D4AF37; }
.chip:hover { background: rgba(212,175,55,0.1); }
#rate { min-width: 26px; text-align: center; color: #ECEAE4; }
</style>

<div class="player">
  <button class="skip" id="prev" aria-label="Previous verse">
    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 6h2v12H7zM19 6v12l-9-6z"/></svg>
  </button>
  <button class="play" id="play" aria-label="Play">
    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
  </button>
  <button class="skip" id="next" aria-label="Next verse">
    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M15 6h2v12h-2zM5 6l9 6-9 6z"/></svg>
  </button>

  <div class="track">
    <input type="range" id="seek" min="0" max="1000" value="0" step="1" aria-label="Seek">
    <div class="meta"><span id="label"></span><span id="time">0:00 / 0:00</span></div>
  </div>

  <div class="speed">
    <span>Speed</span>
    <button class="chip" id="slower" aria-label="Slower">&minus;</button>
    <span id="rate">1</span>
    <button class="chip" id="faster" aria-label="Faster">+</button>
  </div>
</div>

<script>
const TRACKS = __TRACKS__;
const ICON_PLAY  = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
const ICON_PAUSE = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>';

const audio = new Audio();
let idx = 0, rate = 1;

const $ = id => document.getElementById(id);
const fmt = s => (!isFinite(s) ? "0:00"
  : Math.floor(s / 60) + ":" + String(Math.floor(s % 60)).padStart(2, "0"));

function load(i, autoplay) {
  idx = (i + TRACKS.length) % TRACKS.length;
  audio.src = TRACKS[idx].url;
  audio.playbackRate = rate;
  $("label").textContent = TRACKS[idx].label;
  if (autoplay) audio.play().catch(() => {});
}

$("play").onclick = () => audio.paused ? audio.play().catch(() => {}) : audio.pause();
$("prev").onclick = () => load(idx - 1, !audio.paused);
$("next").onclick = () => load(idx + 1, !audio.paused);

$("slower").onclick = () => setRate(Math.max(0.5, rate - 0.25));
$("faster").onclick = () => setRate(Math.min(2, rate + 0.25));
function setRate(v) { rate = v; audio.playbackRate = v; $("rate").textContent = String(v); }

audio.onplay  = () => { $("play").innerHTML = ICON_PAUSE; $("play").setAttribute("aria-label", "Pause"); };
audio.onpause = () => { $("play").innerHTML = ICON_PLAY;  $("play").setAttribute("aria-label", "Play"); };
audio.onended = () => { if (idx < TRACKS.length - 1) load(idx + 1, true); else audio.onpause(); };
audio.ontimeupdate = () => {
  if (audio.duration) $("seek").value = (audio.currentTime / audio.duration) * 1000;
  $("time").textContent = fmt(audio.currentTime) + " / " + fmt(audio.duration);
};
$("seek").oninput = e => { if (audio.duration) audio.currentTime = (e.target.value / 1000) * audio.duration; };

load(0, false);
</script>
"""


def render_player(tracks: list[dict], height: int = 118) -> None:
    components.html(PLAYER_TEMPLATE.replace("__TRACKS__", json.dumps(tracks)), height=height)


# --------------------------------------------------------------------------------------
# Rendering helpers
# --------------------------------------------------------------------------------------


def render_arabic_block(ayahs: list[dict], font_px: int) -> str:
    parts = [
        f'{a["arabic"]}<span class="ayah-mark">﴿{arabic_numeral(a["numberInSurah"])}﴾</span>'
        for a in ayahs
    ]
    return f'<div class="arabic" style="font-size:{font_px}px">{" ".join(parts)}</div>'


def tile(label: str, value: str, note: str) -> str:
    return (
        f'<div class="tile"><div class="tile-label">{label}</div>'
        f'<div class="tile-value">{value}</div>'
        f'<div class="tile-note">{note}</div></div>'
    )


# --------------------------------------------------------------------------------------
# State + sidebar
# --------------------------------------------------------------------------------------

NAV = [
    ("Home", "🏠"),
    ("Browse Quran", "📖"),
    ("AI Companion", "🧠"),
    ("Recitation Coach", "🎙️"),
]

defaults = {
    "page": "Home",
    "surah": 1,
    "messages": [],
    "coach_target": (1, 1),
    "seed_question": "",
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

with st.sidebar:
    st.markdown(
        '<div class="brand"><span class="brand-mark">📖</span>'
        '<div><div class="brand-name">Quran Study<br>Companion</div>'
        '<div class="brand-sub">Read · listen · reflect</div></div></div>',
        unsafe_allow_html=True,
    )

    for label, icon in NAV:
        active = st.session_state.page == label
        if st.button(
            f"{icon}  {label}",
            key=f"nav_{label}",
            type="primary" if active else "secondary",
        ):
            st.session_state.page = label
            st.rerun()

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    with st.expander("Settings"):
        reciter_name = st.selectbox("Reciter", list(RECITERS), index=0)
        translation_name = st.selectbox("Translation", list(TRANSLATIONS), index=0)
        font_px = st.slider("Arabic size", 22, 48, 28, step=2)
        show_translit = st.toggle("Show transliteration", value=True)

RECITER = RECITERS[reciter_name]
TRANSLATION = TRANSLATIONS[translation_name]

SURAHS = fetch_surah_index()
if SURAHS is None:
    st.warning(
        "Can't reach the Quran API, so only the offline copy of Al-Fatiha is available. "
        "Check your connection and reload."
    )
    SURAHS = [FATIHA_FALLBACK]

SURAH_LABELS = {
    s["number"]: f'{s["number"]}. {s["englishName"]} — {s["englishNameTranslation"]}'
    for s in SURAHS
}


def page_header(title: str) -> None:
    left, mid, right = st.columns([3, 5, 1.1])
    with left:
        st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    with mid:
        q = st.text_input(
            "Search",
            key=f"search_{title}",
            placeholder="Search or ask AI (e.g., 'Al-Fatiha tafsir')",
            label_visibility="collapsed",
        )
        if q:
            st.session_state.seed_question = q
            st.session_state.page = "AI Companion"
            st.rerun()
    with right:
        st.markdown(
            '<div style="text-align:right;font-size:17px;opacity:.75;padding-top:5px">🔔</div>',
            unsafe_allow_html=True,
        )


# --------------------------------------------------------------------------------------
# Page: Home
# --------------------------------------------------------------------------------------


def render_home() -> None:
    page_header("Dashboard")

    s_num, first, last = verse_of_the_day()
    surah = fetch_surah(s_num, TRANSLATION)
    if not surah:
        st.error("Couldn't load today's verse. Reload to try again.")
        return

    ayahs = [a for a in surah["ayahs"] if first <= a["numberInSurah"] <= last]
    ayahs = ayahs[:MAX_DAILY_AYAHS]
    last = ayahs[-1]["numberInSurah"]
    ref = (
        f'Surah {surah["englishName"]}, {first}'
        if first == last
        else f'Surah {surah["englishName"]}, {first}–{last}'
    )

    body = [
        '<div class="card">',
        f'<div class="card-head"><span>Verse of the day</span>'
        f'<span class="ref">{ref}</span></div>',
        render_arabic_block(ayahs, font_px),
    ]
    if show_translit:
        translit = " ".join(a["transliteration"] for a in ayahs)
        body.append(f'<div class="translit">{translit}</div>')
    body.append(
        '<div class="translation">'
        + " ".join(a["translation"] for a in ayahs)
        + "</div></div>"
    )
    st.markdown("".join(body), unsafe_allow_html=True)

    tracks = [
        {
            "url": audio_url(s_num, a["numberInSurah"], RECITER),
            "label": f'{surah["englishName"]} {a["numberInSurah"]}',
        }
        for a in ayahs
    ]
    render_player(tracks)

    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("🎙️ Practise this", key="home_practise"):
            st.session_state.coach_target = (s_num, first)
            st.session_state.page = "Recitation Coach"
            st.rerun()
    with c2:
        st.markdown(
            f'<div class="small-note" style="padding-top:9px">'
            f'Recited by {reciter_name} · {translation_name} translation</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3)
    t1.markdown(tile("Reading streak", "12 days", "Longest: 31"), unsafe_allow_html=True)
    t2.markdown(tile("Last read", "Al-Baqarah 142", "Resume where you stopped"), unsafe_allow_html=True)
    t3.markdown(tile("Memorising", "4 surahs", "Al-Mulk is 60% learned"), unsafe_allow_html=True)


# --------------------------------------------------------------------------------------
# Page: Browse Quran
# --------------------------------------------------------------------------------------


def render_browse() -> None:
    page_header("Browse Quran")

    numbers = list(SURAH_LABELS)
    picked = st.selectbox(
        "Surah",
        numbers,
        index=numbers.index(st.session_state.surah) if st.session_state.surah in numbers else 0,
        format_func=lambda n: SURAH_LABELS[n],
        label_visibility="collapsed",
    )
    st.session_state.surah = picked

    surah = fetch_surah(picked, TRANSLATION)
    if not surah:
        st.error("That surah didn't load. Check your connection and try again.")
        return

    total = len(surah["ayahs"])
    if total == 1:
        lo, hi = 1, 1
    else:
        lo, hi = st.slider(
            "Verses", 1, total, (1, min(10, total)), label_visibility="collapsed"
        )
    shown = [a for a in surah["ayahs"] if lo <= a["numberInSurah"] <= hi]

    st.markdown(
        f'<div class="card-head" style="margin:14px 0 8px">'
        f'<span>{surah["revelationType"]} · {total} verses</span>'
        f'<span class="ref" style="font-family:\'Amiri Quran\',serif;font-size:17px">'
        f'{surah["name"]}</span></div>',
        unsafe_allow_html=True,
    )

    render_player(
        [
            {
                "url": audio_url(picked, a["numberInSurah"], RECITER),
                "label": f'{surah["englishName"]} {a["numberInSurah"]}',
            }
            for a in shown
        ]
    )

    for a in shown:
        rows = [
            '<div class="ayah-row">',
            f'<div class="ayah-num">{a["numberInSurah"]}</div>',
            render_arabic_block([a], font_px),
        ]
        if show_translit:
            rows.append(f'<div class="translit">{a["transliteration"]}</div>')
        rows.append(f'<div class="translation">{a["translation"]}</div></div>')
        st.markdown("".join(rows), unsafe_allow_html=True)


# --------------------------------------------------------------------------------------
# Page: AI Companion
# --------------------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a study aid for readers of the Quran. Explain language, context of "
    "revelation, and classical scholarly positions, attributing views to the scholars "
    "who held them. Where scholars differ, present the range rather than one ruling. "
    "You are not a mufti: never issue fatwa. Point the reader to a qualified scholar "
    "for anything that requires a personal ruling, and say so plainly when you are "
    "unsure."
)


def ask_claude(history: list[dict]) -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        # st.secrets raises rather than returning a default when no secrets file exists.
        try:
            key = st.secrets["ANTHROPIC_API_KEY"]
        except Exception:
            key = ""
    if not key:
        return (
            "No API key found. Set `ANTHROPIC_API_KEY` in your environment or in "
            "`.streamlit/secrets.toml`, then ask again."
        )
    try:
        import anthropic
    except ImportError:
        return "The `anthropic` package isn't installed. Run `pip install anthropic`."

    try:
        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1200,
            system=SYSTEM_PROMPT,
            messages=[{"role": m["role"], "content": m["content"]} for m in history],
        )
        return "".join(b.text for b in resp.content if b.type == "text")
    except Exception as exc:
        return f"The request failed: {exc}"


def render_companion() -> None:
    page_header("AI Companion")

    st.markdown(
        '<div class="small-note" style="margin-bottom:14px">'
        "Answers come from a language model and can be wrong. Verify anything you act on "
        "against a published tafsir or a qualified scholar.</div>",
        unsafe_allow_html=True,
    )

    seeded = st.session_state.pop("seed_question", "")
    if seeded:
        st.session_state.messages.append({"role": "user", "content": seeded})

    if not st.session_state.messages:
        st.markdown(
            '<div class="card"><div class="translation">Ask about a word, a verse, or the '
            "setting a passage was revealed in. Try: what does <i>ṣirāṭ</i> carry that "
            "<i>ṭarīq</i> doesn't?</div></div>",
            unsafe_allow_html=True,
        )

    for m in st.session_state.messages:
        with st.chat_message(m["role"], avatar="🧠" if m["role"] == "assistant" else "🙂"):
            st.markdown(m["content"])

    prompt = st.chat_input("Ask about a verse, a word, or its context")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("Thinking"):
                answer = ask_claude(st.session_state.messages)
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.messages and st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------------------------------------------
# Page: Recitation Coach
# --------------------------------------------------------------------------------------


def render_coach() -> None:
    page_header("Recitation Coach")

    s_default, a_default = st.session_state.coach_target
    numbers = list(SURAH_LABELS)
    c1, c2 = st.columns([3, 1])
    with c1:
        s_num = st.selectbox(
            "Surah",
            numbers,
            index=numbers.index(s_default) if s_default in numbers else 0,
            format_func=lambda n: SURAH_LABELS[n],
        )
    surah = fetch_surah(s_num, TRANSLATION)
    if not surah:
        st.error("That surah didn't load. Check your connection and try again.")
        return
    with c2:
        a_num = st.number_input(
            "Verse", min_value=1, max_value=len(surah["ayahs"]),
            value=min(a_default, len(surah["ayahs"])), step=1,
        )

    ayah = surah["ayahs"][int(a_num) - 1]

    block = [
        '<div class="card">',
        f'<div class="card-head"><span>Recite along</span>'
        f'<span class="ref">{surah["englishName"]} {a_num}</span></div>',
        render_arabic_block([ayah], font_px + 4),
    ]
    if show_translit:
        block.append(f'<div class="translit">{ayah["transliteration"]}</div>')
    block.append(f'<div class="translation">{ayah["translation"]}</div></div>')
    st.markdown("".join(block), unsafe_allow_html=True)

    st.markdown('<div class="small-note">Reference recitation</div>', unsafe_allow_html=True)
    render_player(
        [{"url": audio_url(s_num, int(a_num), RECITER),
          "label": f'{surah["englishName"]} {a_num}'}]
    )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="small-note">Your recitation</div>', unsafe_allow_html=True)

    if hasattr(st, "audio_input"):
        clip = st.audio_input("Record", label_visibility="collapsed")
    else:
        clip = st.file_uploader(
            "Upload a recording", type=["wav", "mp3", "m4a"], label_visibility="collapsed"
        )

    if clip:
        st.audio(clip)
        st.info(
            "Recorded. Scoring isn't wired up yet — see the note below for what to plug in.",
            icon="🎧",
        )

    with st.expander("How to add real feedback"):
        st.markdown(
            "This page is the UI shell. To turn it into a working coach you need a "
            "backend that does three things:\n\n"
            "1. **Transcribe** the recording with an Arabic ASR model — Whisper "
            "large-v3 or Tarteel's `whisper-base-ar-quran` handle Quranic Arabic far "
            "better than general models.\n"
            "2. **Align** the transcript to the reference text so you can flag which "
            "words were dropped, added, or mispronounced. Levenshtein alignment over "
            "diacritic-stripped text is a reasonable first pass.\n"
            "3. **Score tajwīd** rules that alignment alone can't see — madd length, "
            "ghunnah, qalqalah — which needs forced alignment with phoneme timings "
            "(Montreal Forced Aligner) plus rule checks on the durations.\n\n"
            "Steps 1 and 2 give useful feedback on their own. Step 3 is a research "
            "project, and even a good model will disagree with a human teacher, so "
            "present its output as a prompt to check with one rather than a verdict."
        )


# --------------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------------

PAGES = {
    "Home": render_home,
    "Browse Quran": render_browse,
    "AI Companion": render_companion,
    "Recitation Coach": render_coach,
}
PAGES[st.session_state.page]()
