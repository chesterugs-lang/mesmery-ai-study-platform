"""
═══════════════════════════════════════════════════════════════════════════════
 ██   ██ ███████ ███████ ██   ██ ███    ███ ███████ ██████  ██    ██
 ███ ███ ██      ██      ███ ███ ████  ████ ██      ██   ██  ██  ██
 ███████ █████   ███████ ███████ ██ ████ ██ █████   ██████    ████
 ██   ██ ██           ██ ██   ██ ██  ██  ██ ██      ██   ██    ██
 ██   ██ ███████ ███████ ██   ██ ██      ██ ███████ ██   ██    ██
═══════════════════════════════════════════════════════════════════════════════
 AI-Powered Study Platform
 Paste your lecture notes, textbook content, or any topic — and get
 summaries, flashcards, quizzes, study plans, and much more.
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as s
import re
import random
import math
import json
import urllib.request
from collections import Counter
import html

# ─── App Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mesmery - AI Study Platform | Summarize, Flashcards, Quizzes",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Theme State ─────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"


def get_theme_css(theme: str) -> str:
    if theme == "classic":
        bg = "#0d0d0d"
        bg_card = "#1a1a1a"
        bg_input = "#141414"
        bg_hover = "#222222"
        text = "#f5f5f5"
        text_muted = "#b0b0b0"
        text_faint = "#666666"
        border = "#333333"
        accent = "#e63946"
        accent_dim = "#b52d37"
        shadow = "rgba(230,57,70,0.08)"
        tag_bg = "#1f1f1f"
        tag_border = "#3d3d3d"
        sidebar_bg = "#111111"
        sidebar_border = "#2a2a2a"
        nav_active_bg = "#0d0d0d"
        nav_active_text = "#e63946"
        nav_border = "#e63946"
    elif theme == "light":
        bg = "#fafafa"
        bg_card = "#ffffff"
        bg_input = "#f4f4f4"
        bg_hover = "#eeeeee"
        text = "#1a1a1a"
        text_muted = "#777777"
        text_faint = "#aaaaaa"
        border = "#e0e0e0"
        accent = "#000000"
        accent_dim = "#888888"
        shadow = "rgba(0,0,0,0.06)"
        tag_bg = "#f0f0f0"
        tag_border = "#dcdcdc"
        sidebar_bg = "#f2f2f2"
        sidebar_border = "#e2e2e2"
        nav_active_bg = "#fafafa"
        nav_active_text = "#1a1a1a"
        nav_border = "#1a1a1a"
    else:  # dark
        bg = "#0a0a0a"
        bg_card = "#111111"
        bg_input = "#161616"
        bg_hover = "#1c1c1c"
        text = "#e8e8e8"
        text_muted = "#808080"
        text_faint = "#555555"
        border = "#252525"
        accent = "#ffffff"
        accent_dim = "#666666"
        shadow = "rgba(255,255,255,0.04)"
        tag_bg = "#1a1a1a"
        tag_border = "#2a2a2a"
        sidebar_bg = "#0e0e0e"
        sidebar_border = "#1a1a1a"
        nav_active_bg = "#0a0a0a"
        nav_active_text = "#e8e8e8"
        nav_border = "#e8e8e8"

    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* ── Override Streamlit theme variables ─────────────────── */
        :root {{
            --primary-color: {nav_active_bg};
            --primary-bg: {nav_active_bg};
            --primary-text: {nav_active_text};
            --text-color: {text};
            --background-color: {bg};
            --secondary-background-color: {bg_card};
            --font: 'Inter', sans-serif;
        }}
        .stApp {{
            background-color: {bg};
            color: {text};
        }}


        /* ── Sidebar ────────────────────────────────────────────── */
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            border-right: 1px solid {sidebar_border} !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown p,
        section[data-testid="stSidebar"] .stMarkdown li,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stCaption {{
            color: {text_muted} !important;
        }}

        /* ── Typography ─────────────────────────────────────────── */
        h1, h2, h3, h4, h5, h6 {{
            color: {text} !important;
            font-weight: 600 !important;
            letter-spacing: -0.02em !important;
        }}
        p, span, div, label, li, td, th {{
            color: {text};
        }}
        .stMarkdown h1 {{ border-bottom: 2px solid {border}; padding-bottom: 0.3em; }}
        .stMarkdown h2 {{ border-bottom: 1px solid {border}; padding-bottom: 0.2em; }}

        /* ── Inputs ─────────────────────────────────────────────── */
        .stTextArea textarea, .stTextInput input {{
            background-color: {bg_input} !important;
            color: {text} !important;
            border: 1px solid {border} !important;
            border-radius: 6px !important;
            font-family: 'Inter', sans-serif !important;
        }}
        .stTextArea textarea:focus, .stTextInput input:focus {{
            border-color: {accent} !important;
            box-shadow: 0 0 0 1px {accent} !important;
        }}

        /* ── Primary action buttons ────────────────────────────── */
        .stButton > button,
        div[data-testid="stButton"] > button {{
            background-color: {bg_card} !important;
            color: {text} !important;
            border: 1px solid {border} !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.85rem !important;
            padding: 0.5em 1.2em !important;
            transition: all 0.2s ease !important;
            letter-spacing: -0.01em !important;
            box-shadow: 0 1px 3px {shadow} !important;
            cursor: pointer !important;
        }}
        .stButton > button:hover,
        div[data-testid="stButton"] > button:hover {{
            background-color: {bg_hover} !important;
            color: {text} !important;
            border-color: {accent_dim} !important;
            box-shadow: 0 4px 12px {shadow} !important;
            transform: translateY(-2px) !important;
        }}
        .stButton > button:active,
        .stButton > button:focus {{
            background-color: {bg_hover} !important;
            color: {text} !important;
            border-color: {accent} !important;
            box-shadow: 0 1px 2px {shadow} !important;
            transform: translateY(0) !important;
            outline: none !important;
        }}
        /* Sidebar nav buttons — clean navigation style */
        section[data-testid="stSidebar"] .stButton > button {{
            text-align: left !important;
            padding: 0.5em 1em !important;
            font-size: 0.82rem !important;
            background-color: transparent !important;
            color: {text_muted} !important;
            border: 1px solid transparent !important;
            border-radius: 6px !important;
            font-weight: 500 !important;
            box-shadow: none !important;
        }}
        section[data-testid="stSidebar"] .stButton > button:hover {{
            color: {text} !important;
            border-color: {border} !important;
            background-color: {bg_hover} !important;
            box-shadow: none !important;
            transform: none !important;
        }}

        /* ── Selectbox & Slider ─────────────────────────────────── */
        .stSelectbox > div > div {{
            background-color: {bg_input} !important;
            color: {text} !important;
            border: 1px solid {border} !important;
            border-radius: 6px !important;
        }}
        .stSelectbox > div > div > div {{
            color: {text} !important;
        }}
        .stSelectbox span,
        .stSelectbox p,
        .stSelectbox label {{
            color: {text} !important;
        }}
        /* Dropdown menu options */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] li,
        div[data-baseweb="popover"] span,
        div[data-baseweb="popover"] div,
        div[data-baseweb="menu"],
        div[data-baseweb="menu"] li,
        div[data-baseweb="menu"] span,
        ul[data-baseweb="menu"] li {{
            background-color: {bg_card} !important;
            color: {text} !important;
        }}
        div[data-baseweb="popover"] li:hover,
        div[data-baseweb="menu"] li:hover,
        ul[data-baseweb="menu"] li:hover {{
            background-color: {bg_hover} !important;
            color: {text} !important;
        }}
        .stSlider > div > div > div {{ background: {border} !important; }}

        /* ── Tabs ───────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {{
            background: {bg_card};
            border-radius: 8px;
            padding: 3px;
            border: 1px solid {border};
            gap: 2px;
        }}
        .stTabs [data-baseweb="tab"] {{
            color: {text_muted} !important;
            border-radius: 6px;
            font-weight: 500;
            font-size: 0.85rem;
            padding: 8px 16px;
            transition: all 0.15s ease;
        }}
        .stTabs [aria-selected="true"] {{
            color: {text} !important;
            background: {bg_hover} !important;
            border-bottom: none !important;
            font-weight: 600 !important;
        }}

        /* ── Metric Cards ───────────────────────────────────────── */
        div[data-testid="stMetric"] {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 8px;
            padding: 14px;
        }}
        div[data-testid="stMetric"] label {{
            color: {text_muted} !important;
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }}

        /* ── Custom Cards ───────────────────────────────────────── */
        .mesmery-card {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 8px;
            padding: 20px;
            margin: 6px 0;
            transition: all 0.15s ease;
        }}
        .mesmery-card:hover {{
            border-color: {accent_dim};
            box-shadow: 0 2px 12px {shadow};
        }}
        .flashcard {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 12px;
            padding: 32px 24px;
            margin: 10px 0;
            text-align: center;
            min-height: 180px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1em;
            line-height: 1.6;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .flashcard:hover {{
            border-color: {accent};
            box-shadow: 0 4px 20px {shadow};
        }}
        .quiz-option {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 8px;
            padding: 14px 18px;
            margin: 5px 0;
            transition: all 0.15s ease;
            cursor: pointer;
        }}
        .quiz-option:hover {{
            border-color: {accent_dim};
            background: {bg_hover};
        }}
        .quiz-correct {{
            border-left: 3px solid {accent} !important;
            background: {bg_hover} !important;
        }}
        .quiz-wrong {{
            border-left: 3px solid {text_faint} !important;
            background: {bg_input} !important;
        }}
        .tag {{
            display: inline-block;
            background: {tag_bg};
            border: 1px solid {tag_border};
            border-radius: 4px;
            padding: 3px 10px;
            margin: 2px;
            font-size: 0.78em;
            font-weight: 500;
            color: {text_muted};
            letter-spacing: 0.02em;
        }}
        .progress-bar-bg {{
            background: {border};
            border-radius: 6px;
            height: 6px;
            overflow: hidden;
            margin: 8px 0;
        }}
        .progress-bar-fill {{
            background: {accent};
            height: 100%;
            border-radius: 6px;
            transition: width 0.6s ease;
        }}
        .study-tip {{
            background: {bg_card};
            border-left: 3px solid {accent};
            padding: 16px 20px;
            border-radius: 0 6px 6px 0;
            margin: 8px 0;
        }}
        .divider {{
            border-top: 1px solid {border};
            margin: 24px 0;
        }}
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: {text_muted};
        }}
        .empty-state h3 {{ margin-bottom: 12px; }}
        .hero-title {{
            font-size: 3em;
            font-weight: 800;
            letter-spacing: -0.04em;
            margin-bottom: 0.15em;
        }}
        .hero-sub {{
            font-size: 1.1em;
            color: {text_muted};
            margin-bottom: 2em;
            letter-spacing: -0.01em;
        }}

        /* ── Expander ────────────────────────────────────────────── */
        .streamlit-expanderHeader {{
            background: {bg_card} !important;
            border: 1px solid {border} !important;
            border-radius: 6px !important;
            color: {text} !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
        }}
        .streamlit-expanderContent {{
            background: {bg_card} !important;
            border: 1px solid {border} !important;
            border-top: none !important;
            border-radius: 0 0 6px 6px !important;
        }}

        /* ── Sidebar Nav ────────────────────────────────────────── */
        .sidebar-header {{
            font-size: 0.65rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: {text_faint};
            padding: 8px 0 4px;
            margin: 12px 0 4px;
            border-bottom: 1px solid {border};
        }}
        .sidebar-header:first-child {{
            margin-top: 0;
        }}

        /* ── Scrollbar ──────────────────────────────────────────── */
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: {bg}; }}
        ::-webkit-scrollbar-thumb {{
            background: {border};
            border-radius: 3px;
        }}
        ::-webkit-scrollbar-thumb:hover {{ background: {accent_dim}; }}

        /* ── Summary Section Cards ──────────────────────── */
        .summary-section {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 8px;
            padding: 20px 24px;
            margin: 10px 0;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }}
        .summary-section::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: {accent};
            border-radius: 3px 0 0 3px;
        }}
        .summary-section:hover {{
            border-color: {accent_dim};
            box-shadow: 0 2px 16px {shadow};
        }}
        .summary-section-header {{
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: {text_muted};
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .summary-section-header .dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: {accent};
            display: inline-block;
        }}
        .summary-content {{
            font-size: 0.95rem;
            line-height: 1.7;
            color: {text};
        }}

        /* ── Quality Analysis Dashboard ─────────────────── */
        .quality-bar-bg {{
            background: {border};
            border-radius: 4px;
            height: 6px;
            overflow: hidden;
            margin: 4px 0;
            flex: 1;
        }}
        .quality-bar-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.8s ease;
        }}
        .quality-bar-fill.high {{ background: {accent}; }}
        .quality-bar-fill.medium {{ background: {accent_dim}; }}
        .quality-bar-fill.low {{ background: {text_faint}; }}
        .quality-row {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 6px 0;
            font-size: 0.82rem;
        }}
        .quality-label {{
            color: {text_muted};
            min-width: 130px;
            font-weight: 500;
        }}
        .quality-value {{
            color: {text};
            font-weight: 600;
            min-width: 40px;
            text-align: right;
        }}
        .quality-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.03em;
        }}
        .quality-badge.pass {{
            background: {tag_bg};
            border: 1px solid {accent_dim};
            color: {text};
        }}
        .quality-badge.warn {{
            background: {tag_bg};
            border: 1px solid {text_faint};
            color: {text_muted};
        }}

        /* ── TL;DR Card ─────────────────────────────────── */
        .tldr-card {{
            background: {bg_card};
            border: 1px solid {border};
            border-left: 3px solid {accent};
            border-radius: 0 8px 8px 0;
            padding: 20px 24px;
            margin: 10px 0;
            font-style: italic;
            line-height: 1.7;
            color: {text};
        }}

        /* ── Analysis Metric Highlight ──────────────────── */
        .metric-highlight {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 8px;
            padding: 12px 16px;
            text-align: center;
            transition: all 0.15s ease;
        }}
        .metric-highlight:hover {{
            border-color: {accent_dim};
        }}
        .metric-highlight .metric-val {{
            font-size: 1.4em;
            font-weight: 700;
            color: {text};
            letter-spacing: -0.02em;
        }}
        .metric-highlight .metric-label {{
            font-size: 0.72rem;
            color: {text_muted};
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 2px;
        }}
    </style>
    """


# ─── NLP Utilities ───────────────────────────────────────────────────────────

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "was", "are", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "shall", "should", "may", "might", "must", "can", "could", "not",
    "no", "nor", "so", "yet", "both", "each", "few", "more", "most",
    "other", "some", "such", "than", "too", "very", "just", "also",
    "about", "above", "after", "again", "all", "am", "any", "as", "because",
    "before", "below", "between", "this", "that", "these", "those", "it",
    "its", "into", "if", "then", "else", "when", "up", "out", "only",
    "own", "same", "over", "under", "here", "there", "where", "how",
    "what", "which", "who", "whom", "while", "during", "through", "between",
    "he", "she", "they", "them", "his", "her", "my", "your", "our",
    "me", "you", "we", "i", "their", "your", "our",
    "get", "got", "make", "made", "take", "use", "used", "using",
    "one", "two", "three", "first", "second", "new", "old", "long",
    "many", "much", "well", "back", "even", "still", "way", "also",
    "however", "since", "now", "often", "already", "rather", "nearly",
    "every", "always", "never", "sometimes", "usually", "another",
    "example", "including", "like", "especially", "either", "neither",
    "whether", "upon", "per", "via", "etc", "eg", "ie",
}

# Common sentence starters — used to detect proper nouns vs. normal sentence beginnings
SENTENCE_STARTERS = {
    "the", "this", "that", "these", "those", "it", "its", "he", "she",
    "they", "his", "her", "their", "a", "an", "in", "on", "at", "for",
    "by", "with", "from", "however", "although", "because", "since",
    "when", "while", "after", "before", "if", "as", "but", "and",
    "or", "so", "yet", "not", "both", "each", "some", "most", "many",
    "all", "also", "even", "still", "just", "new", "old", "several",
    "another", "other", "such", "only", "very", "rather", "quite",
    "perhaps", "likely", "first", "second", "third", "one", "two",
    "three", "four", "five", "through", "during", "between",
}


def tokenize(text: str) -> list[str]:
    """Split text into lowercase word tokens."""
    return re.findall(r"\b[a-z]{2,}\b", text.lower())


def split_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 15]


def extract_keywords(text: str, top_n: int = 20) -> list[str]:
    """Extract top keywords by frequency, excluding stop words."""
    tokens = tokenize(text)
    filtered = [w for w in tokens if w not in STOP_WORDS and len(w) > 2]
    counts = Counter(filtered)
    return [word for word, _ in counts.most_common(top_n)]


def extract_keyphrases(text: str, top_n: int = 10) -> list[str]:
    """Extract bigram and trigram key phrases."""
    tokens = tokenize(text)
    filtered = [w for w in tokens if w not in STOP_WORDS and len(w) > 2]

    bigrams = [f"{filtered[i]} {filtered[i+1]}" for i in range(len(filtered) - 1)]
    trigrams = [f"{filtered[i]} {filtered[i+1]} {filtered[i+2]}" for i in range(len(filtered) - 2)]

    all_phrases = bigrams + trigrams
    counts = Counter(all_phrases)
    return [phrase for phrase, count in counts.most_common(top_n) if count >= 2]


def score_sentences(text: str) -> list[tuple[str, float]]:
    """Score sentences by keyword density and position."""
    sentences = split_sentences(text)
    if not sentences:
        return []

    keywords = set(extract_keywords(text, 30))
    scored = []

    for i, sent in enumerate(sentences):
        tokens = tokenize(sent)
        if not tokens:
            continue
        keyword_hits = sum(1 for t in tokens if t in keywords)
        keyword_density = keyword_hits / len(tokens)

        # Position bonus (intro and conclusion sentences rank higher)
        position_bonus = 0
        if i < 3:
            position_bonus = 0.15
        elif i >= len(sentences) - 3:
            position_bonus = 0.1

        # Length penalty for very short or very long sentences
        length_score = 1.0
        if len(tokens) < 5:
            length_score = 0.5
        elif len(tokens) > 40:
            length_score = 0.8

        score = (keyword_density * 0.6 + position_bonus) * length_score
        scored.append((sent, score))

    return scored


def extract_numbers_and_dates(text: str) -> list[str]:
    """Extract notable numbers, percentages, dates from text."""
    patterns = [
        r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?%',          # percentages
        r'\b\d{4}\b',                                    # years
        r'\b\d+(?:\.\d+)?\s*(?:million|billion|trillion|thousand)\b',
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d+(?:\.\d+)?\s*(?:kg|m|km|lbs|miles|degrees|Hz|MHz|GHz|MB|GB|TB)\b',
    ]
    results = []
    for p in patterns:
        results.extend(re.findall(p, text, re.IGNORECASE))
    return list(set(results))


def find_definitions_in_text(text: str) -> dict[str, str]:
    """Enhanced definition extraction with multiple patterns."""
    defs = {}

    # "X is/means/refers to Y" patterns
    for m in re.finditer(
        r'((?:[A-Z][a-zA-Z]+\s?){1,4})(?:\s+(?:is|are|means|refers to|is defined as|can be defined as|describes|denotes)\s+)(.{15,300}?)(?:\.(?:\s|$)|;\s|$)',
        text
    ):
        term = m.group(1).strip()
        defn = m.group(2).strip()
        if 2 < len(term) < 50:
            defs[term] = defn

    # "X: Y" at start of line or after newline
    for m in re.finditer(r'(?:^|\n)\s*((?:[A-Z][a-zA-Z]+\s?){1,4}):\s+([^\n]{15,300})', text):
        term = m.group(1).strip()
        defn = m.group(2).strip()
        if 2 < len(term) < 50 and term not in defs:
            defs[term] = defn

    return defs


# ─── Feature 1: Summarizer ──────────────────────────────────────────────────

def _extract_named_entities(text: str) -> list[str]:
    """Extract named entities (proper nouns, events, organizations) from text.
    Works for any subject — not domain-specific."""
    # Multi-word proper nouns (consecutive capitalized words, 2-4 words)
    multi_word = re.findall(
        r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b',
        text
    )
    # Filter out common sentence-starting phrases
    # Use title-cased version of the module-level SENTENCE_STARTERS
    starters_title = {w.title() for w in SENTENCE_STARTERS}
    filtered_multi = [
        phrase for phrase in multi_word
        if phrase.split()[0] not in starters_title
        and len(phrase) > 4
    ]
    # Single important proper nouns (appear 2+ times, not sentence starters)
    single_nouns = re.findall(r'\b([A-Z][a-z]{3,})\b', text)
    filtered_single = [n for n in single_nouns if n not in starters_title]
    noun_counts = Counter(filtered_single)
    significant_singles = [noun for noun, count in noun_counts.items() if count >= 2]
    # Multi-word phrases that appear 2+ times are very significant
    phrase_counts = Counter(filtered_multi)
    significant_phrases = [p for p, c in phrase_counts.items() if c >= 2]
    # Also include multi-word phrases from context (sentences with key terms)
    keywords = set(extract_keywords(text, 10))
    context_phrases = []
    for phrase in set(filtered_multi):
        phrase_lower = phrase.lower()
        if any(re.search(rf'\b{re.escape(kw)}\b', phrase_lower) for kw in keywords):
            context_phrases.append(phrase)
    # Combine: significant phrases first, then context phrases, then single nouns
    all_entities = list(dict.fromkeys(
        significant_phrases + context_phrases + significant_singles
    ))
    return all_entities[:25]



# Known abbreviations that should not be treated as numbered section headers
KNOWN_ABBREVIATIONS = {
    'Dr.', 'Mr.', 'Mrs.', 'Ms.', 'Prof.', 'St.', 'Rev.', 'Gen.',
    'Sen.', 'Rep.', 'Gov.', 'Lt.', 'Sgt.', 'Cpl.', 'Pvt.',
    'U.S.', 'U.K.', 'E.U.', 'U.N.', 'U.S.S.R.', 'Ph.D.',
    'A.M.', 'P.M.', 'B.C.', 'A.D.', 'vs.', 'etc.', 'e.g.', 'i.e.',
    'Inc.', 'Ltd.', 'Jr.', 'Sr.', 'Dept.', 'Vol.', 'No.', 'Fig.',
}

# Words indicating outcomes/conclusions (shared by summary and transition logic)
OUTCOME_WORDS = {
    'ultimately', 'eventually', 'finally', 'resulted', 'consequence',
    'legacy', 'impact', 'outcome', 'aftermath', 'resolution', 'concluded',
    'ended', 'led to',
}

# Words indicating origins/causes (shared by summary and transition logic)
ORIGIN_WORDS = {
    'began', 'started', 'originated', 'rooted', 'stemmed', 'arose',
    'founded', 'established', 'triggered', 'sparked', 'fueled', 'caused',
    'motivated', 'driven', 'prompted', 'led to the',
}

# Words commonly found in document headings/section labels
HEADING_INDICATOR_WORDS = {
    'background', 'origins', 'introduction', 'overview', 'conclusion',
    'summary', 'chapter', 'section', 'unit', 'part', 'methodology',
    'results', 'discussion', 'findings', 'analysis', 'implications',
    'recommendations', 'objectives', 'goals', 'agenda', 'timeline',
    'abstract', 'appendix', 'references', 'bibliography', 'glossary',
    'data', 'limitations', 'hypothesis', 'literature review', 'acknowledgments',
    'outline', 'index', 'preface', 'foreword', 'prologue', 'epilogue',
}


def _is_heading(text: str) -> bool:
    """Detect if a piece of text is a heading, title, section label, or formatting artifact.
    Returns True if the text should be treated as structure, not content."""
    text = text.strip()
    if not text:
        return False
    # ── Markdown headings (#, ##, ###, etc.) ──
    if re.match(r'^#{1,6}\s+', text):
        return True
    # ── Numbered section headers (I., II., 1., 2.) — exclude common abbreviations ──
    first_token = text.split()[0] if text.split() else ''
    # Skip if first token is a known abbreviation
    if first_token not in KNOWN_ABBREVIATIONS:
        # Also skip multi-letter abbreviations like U.S., U.K.
        if re.match(r'^[A-Z](?:\.[A-Z])+$', first_token.rstrip('.')):
            pass
        elif re.match(r'^(?:[IVXLC]+\.\s+[A-Z]|\d+(?:\.\d+)*\.\s+[A-Z])', text):
            return True
    # ── Ends with colon (section label pattern) ──
    if text.endswith(':') and len(text.split()) <= 8 and len(text) < 60:
        text_lower = text.lower().rstrip(':').strip()
        if text_lower in HEADING_INDICATOR_WORDS or any(text_lower.startswith(hw) for hw in HEADING_INDICATOR_WORDS):
            return True
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.5:
            return True
    # ── All-caps text (common for chapter/unit names) ──
    words = text.split()
    if len(words) >= 2 and len(words) <= 10:
        all_caps = sum(1 for w in words if w.isupper() and len(w) > 1)
        if all_caps / len(words) > 0.7:
            return True
    # ── Decorative/separators (lines of symbols) ──
    if re.match(r'^[─═\-=*#~_]{3,}$', text):
        return True
    # ── Very short standalone labels (< 6 words, no verb) ──
    tokens = tokenize(text)
    word_count = len(text.split())
    if word_count <= 6 and len(tokens) <= 5:
        # Check for heading-indicator patterns
        heading_words = {'background', 'origins', 'introduction', 'overview', 'conclusion',
                         'summary', 'chapter', 'section', 'unit', 'part', 'appendix',
                         'references', 'bibliography', 'glossary', 'index', 'abstract',
                         'methodology', 'results', 'discussion', 'acknowledgments',
                         'objectives', 'goals', 'agenda', 'timeline', 'outline'}
        text_lower = text.lower().rstrip(':').strip()
        if text_lower in heading_words or any(text_lower.startswith(hw) for hw in heading_words):
            return True
    # ── Unit/Chapter/Section prefix labels ──
    if re.match(r'^(?:unit|chapter|section|part|module|lesson|topic)\s*[:#\d]', text, re.IGNORECASE):
        return True
    # ── Separator lines with decorative symbols ──
    if re.match(r'^[\s─═\-=*#~|/\\_]{3,}$', text):
        return True
    # ── Heading words as standalone labels (no colon) ──
    word_count = len(text.split())
    tokens = tokenize(text)
    if word_count <= 6 and len(tokens) <= 5:
        text_lower = text.lower().rstrip(':').strip()
        if text_lower in HEADING_INDICATOR_WORDS:
            return True
    # ── Lecture note artifacts: titles, special symbols, formatting ──
    # Lines that are mostly special characters, symbols, or formatting
    alpha_chars = sum(1 for c in text if c.isalpha())
    special_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
    total_chars = max(len(text), 1)
    # Lines that are mostly symbols/formatting (borders, decorative lines)
    if special_chars / total_chars > 0.4 and alpha_chars < 10:
        return True
    # LaTeX-like patterns: \frac, \sum, \int, \sqrt
    if re.search(r'\\(?:frac|sum|int|sqrt|text|begin|end|left|right|alpha|beta|gamma|delta|theta|lambda|sigma|pi|omega|nabla|partial|infty)', text):
        return True
    # Dollar-sign math mode: $...$
    if re.search(r'\$[^$]+\$', text) and alpha_chars < 20:
        return True
    # Lines that are just bullet symbols, arrows, or decorative characters
    stripped = text.strip()
    bullet_chars = set('•·∙○●◦‣⁃←↑→↓►▶◀◄–—-=*#~_…|/\\')
    if stripped and all(c in bullet_chars for c in stripped):
        return True
    # Lines that are just a number or letter label (like "1.", "a)", "(I)", "A.")
    if re.match(r'^\s*(?:\d+[.)\]]|[a-z][.)\]]|[A-Z][.)\]]|\([ivxlcIVXLC]+\)|\([A-Z]\)|\(\d+\))\s*$', text):
        return True
    # Page numbers, footers, headers (e.g., "Page 5 of 10")
    if re.match(r'^\s*(?:page|p\.?)\s*\d+\s*(?:of\s*\d+)?\s*$', text, re.IGNORECASE):
        return True
    return False
    return False

def _parse_document_structure(text: str) -> tuple[list[dict], list[str]]:
    """Parse document structure: extract headings and topic boundaries.
    Returns (headings, content_sentences) where headings are metadata and
    content_sentences are actual content for summarization.
    Uses split_sentences internally for consistent sentence boundaries."""
    raw_sentences = split_sentences(text)
    headings = []       # Structure metadata: [{text, position, topic}]
    content = []        # Actual content sentences
    for i, sent in enumerate(raw_sentences):
        if _is_heading(sent):
            headings.append({
                'text': sent.rstrip(':').strip(),
                'position': i,
                'topic': sent.rstrip(':').strip(),
            })
        else:
            content.append(sent)
    return headings, content


def _detect_causal_sentences(sent: str) -> float:
    """Detect cause-effect and high-value language in a sentence.
    Returns a score 0-1 indicating how much causal/analytical content the sentence has."""
    sent_lower = sent.lower()
    score = 0.0
    # Causal language markers (cause → effect)
    causal_markers = [
        'because', 'therefore', 'thus', 'consequently', 'as a result',
        'led to', 'resulted in', 'caused', 'forced', 'triggered',
        'meant that', 'shaped', 'influenced', 'produced',
        'demonstrated', 'established', 'revealed',
        'contributed to', 'gave rise to', 'stemmed from',
        'enabled', 'compelled', 'prompted',
    ]
    for marker in causal_markers:
        if marker in sent_lower:
            score += 0.3
    # High-value analytical language
    analytical_markers = [
        'however', 'although', 'despite', 'in contrast',
        'on the other hand', 'nevertheless', 'whereas',
        'significance', 'implication', 'consequence',
        'transformed', 'revolutionized', 'fundamental',
        'critical', 'defining', 'decisive',
    ]
    for marker in analytical_markers:
        if marker in sent_lower:
            score += 0.15
    # Definition / explanation markers
    definition_markers = [
        'is defined as', 'refers to', 'means that',
        'can be described as', 'is characterized by',
        'the idea that', 'the concept of',
    ]
    for marker in definition_markers:
        if marker in sent_lower:
            score += 0.2
    return min(score, 1.0)


def _score_sentence_for_summary(sent: str, keywords: set[str], entities: list[str], position: int, total: int) -> float:
    """Score a sentence for inclusion in a summary with multiple factors."""
    tokens = tokenize(sent)
    if not tokens:
        return 0.0
    # Keyword density
    keyword_hits = sum(1 for t in tokens if t in keywords)
    keyword_score = keyword_hits / len(tokens)
    # Named entity presence (events, people, organizations)
    entity_score = 0
    for ent in entities:
        if ent.lower() in sent.lower():
            entity_score += 0.3
    entity_score = min(entity_score, 1.0)
    # Position score (intro and conclusion get bonus)
    position_ratio = position / max(total, 1)
    position_score = 0
    if position_ratio < 0.15:
        position_score = 0.15  # First 15% of text
    elif position_ratio > 0.85:
        position_score = 0.1  # Last 15% of text
    # Length score (prefer medium-length sentences)
    word_count = len(tokens)
    if word_count < 8:
        length_score = 0.3
    elif 8 <= word_count <= 30:
        length_score = 1.0
    elif 30 < word_count <= 50:
        length_score = 0.7
    else:
        length_score = 0.4
    # Proper noun density (sentences with names, dates, events are more informative)
    proper_nouns = len(re.findall(r'\b[A-Z][a-z]{2,}\b', sent))
    proper_score = min(proper_nouns / max(len(tokens), 1) * 3, 1.0)
    # Causal / analytical language bonus
    causal_score = _detect_causal_sentences(sent)
    # Weighted combination
    total_score = (
        keyword_score * 0.25 +
        entity_score * 0.20 +
        position_score * 0.10 +
        length_score * 0.08 +
        proper_score * 0.15 +
        causal_score * 0.22
    )
    return total_score


def _trim_sentence(sent: str, keywords: set[str]) -> str:
    """Trim minor details from a sentence while preserving essential information.
    Removes parentheticals, 'for example' clauses, and non-essential modifiers."""
    # Remove parenthetical insertions: (like this)
    trimmed = re.sub(r'\s*\([^)]{10,}\)', '', sent)
    # Remove 'for example/instance' clauses
    trimmed = re.sub(r',\s*(?:for example|for instance|such as|including)[^,.;]*?[.,;]', '.', trimmed, flags=re.IGNORECASE)
    # Remove 'which/that' relative clauses that don't contain keywords
    def _should_keep_relative(match):
        clause = match.group(0).lower()
        if any(kw in clause for kw in keywords):
            return match.group(0)
        # Preserve the ending punctuation if the match ended with one
        matched = match.group(0)
        if matched.rstrip().endswith('.'):
            return '.'
        return ','
    trimmed = re.sub(r',\s*which\s+[^,.;]{10,}[.,;]', _should_keep_relative, trimmed, flags=re.IGNORECASE)
    # Clean up double punctuation (including with spaces between)
    trimmed = re.sub(r'\.{2,}', '.', trimmed)
    trimmed = re.sub(r'\.\s+\.', '.', trimmed)
    trimmed = re.sub(r',\s*,', ',', trimmed)
    # Clean up dangling commas before periods
    trimmed = re.sub(r',\s*\.', '.', trimmed)
    # Ensure sentence ends with a period
    if trimmed and not trimmed.rstrip().endswith(('.', '!', '?')):
        trimmed = trimmed.rstrip() + '.'
    return trimmed.strip()


def _extract_key_phrase(sent: str, keywords: set[str]) -> str:
    """Extract the most information-bearing part of a sentence.
    Strips leading subordinate clauses and trailing modifiers to get the core info."""
    cleaned = sent.strip()
    # Remove leading subordinate clauses: "Although ..., " "Because ..., " etc.
    cleaned = re.sub(
        r'^(?:Although|While|Because|Since|When|After|Before|If|Though|Despite|As)\s+[^,]+,\s*',
        '', cleaned, count=1, flags=re.IGNORECASE
    )
    # Remove leading prepositional phrases: "In the ..., " "During the ..., " etc.
    cleaned = re.sub(
        r'^(?:In|During|After|Before|Through|With|By|For|On|At)\s+(?:the|this|that|a|an)\s+\w+(?:\s+\w+){0,3},\s*',
        '', cleaned, count=1, flags=re.IGNORECASE
    )
    # Remove trailing non-essential relative clauses without keywords
    def _strip_trailing_rel(match):
        clause = match.group(0).lower()
        if any(kw in clause for kw in keywords):
            return match.group(0)
        return '.'
    cleaned = re.sub(r',\s*(?:which|that|who|where)\s+[^,.;]{10,}[.;]?', _strip_trailing_rel, cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip()
    if not cleaned or len(tokenize(cleaned)) < 3:
        return sent.strip()
    return cleaned


def _compress_final_sentence(sent: str) -> str:
    """Aggressively compress a combined sentence by removing low-value filler phrases."""
    compressed = sent
    # Remove filler phrases
    filler_patterns = [
        r'\bit\s+is\s+(?:important|worth|notable)\s+to\s+(?:note|mention|observe)\s+that\s*',
        r'\bit\s+should\s+be\s+(?:noted|mentioned|observed)\s+that\s*',
        r'\bin\s+(?:addition|fact|reality|essence|general|particular)\s*,?\s*',
        r'\b(?:Basically|Essentially|Fundamentally)\s*,?\s*',
    ]
    for pattern in filler_patterns:
        compressed = re.sub(pattern, '', compressed, flags=re.IGNORECASE)
    # Compress verbose phrases
    compressed = re.sub(r'\bin order to\b', 'to', compressed, flags=re.IGNORECASE)
    compressed = re.sub(r'\bdue to the fact that\b', 'because', compressed, flags=re.IGNORECASE)
    compressed = re.sub(r'\bat this point in time\b', 'now', compressed, flags=re.IGNORECASE)
    compressed = re.sub(r'\bin the event that\b', 'if', compressed, flags=re.IGNORECASE)
    compressed = re.sub(r'\bfor the purpose of\b', 'to', compressed, flags=re.IGNORECASE)
    # Remove unnecessary "that" after reporting verbs
    compressed = re.sub(
        r'\b(found|showed|demonstrated|indicated|revealed|suggested|confirmed)\s+that\s+',
        r'\1 ',
        compressed, flags=re.IGNORECASE
    )
    # Clean up whitespace and punctuation
    compressed = re.sub(r'\s{2,}', ' ', compressed)
    compressed = re.sub(r',\s*,', ',', compressed)
    compressed = re.sub(r',\s*\.', '.', compressed)
    compressed = re.sub(r'\.\s*\.', '.', compressed)
    return compressed.strip()


def _combine_related_sentences(sents: list[str], keywords: set[str]) -> str:
    """Combine 2-3 related sentences into one denser sentence.
    Extracts core information from each, removes overlap, merges using short connectives."""
    if len(sents) == 1:
        return _trim_sentence(sents[0], keywords)
    # Trim and filter
    infos = []
    for s in sents:
        trimmed = _trim_sentence(s, keywords)
        tokens = tokenize(trimmed)
        if len(tokens) >= 4:
            infos.append(trimmed)
    if not infos:
        return _trim_sentence(sents[0], keywords)
    if len(infos) == 1:
        return infos[0]
    # Use first sentence as base
    main = infos[0].rstrip('.')
    used_tokens = set(tokenize(main))
    for extra in infos[1:]:
        extra_clean = extra.rstrip('.').strip()
        # Extract just the key phrase (strip subordinate clauses already covered)
        extra_key = _extract_key_phrase(extra_clean, keywords)
        extra_tokens = set(tokenize(extra_key))
        # Skip if mostly overlapping with what's already combined
        new_info = extra_tokens - used_tokens - STOP_WORDS
        if len(new_info) < 3:
            continue
        # Choose shorter connective
        extra_lower = extra_key.lower()
        if any(w in extra_lower for w in ['however', 'although', 'despite', 'but', 'whereas']):
            connector = ', while '
        elif any(w in extra_lower for w in ['led to', 'resulted', 'caused', 'produced']):
            connector = ', which '
        else:
            connector = '; '
        if len(main) + len(extra_key) > 300:
            break
        # Handle casing
        first_word = extra_key.split()[0] if extra_key.split() else ''
        if first_word.lower() in SENTENCE_STARTERS:
            main = main + connector + extra_key[0].lower() + extra_key[1:]
        else:
            main = main + connector + extra_key
        used_tokens |= extra_tokens
    result = main + '.'
    # Post-combination compression
    result = _compress_final_sentence(result)
    return result


def _check_narrative_arc(selected_sents: list[str], keywords: set[str]) -> dict:
    """Verify the summary covers the full narrative arc: origins, developments, and outcomes.
    Returns coverage metrics for each arc segment."""
    summary_text = ' '.join(selected_sents).lower()
    # Origin/causes language
    origin_markers = ['began', 'started', 'originated', 'rooted', 'stemmed', 'arose',
                      'founded', 'established', 'triggered', 'sparked', 'fueled', 'caused',
                      'motivated', 'driven', 'prompted', 'led to the']
    has_origin = any(m in summary_text for m in origin_markers)
    # Development/turning point language
    development_markers = ['however', 'escalated', 'intensified', 'shifted', 'transformed',
                           'evolved', 'expanded', 'grew', 'emerged', 'developed', 'changed',
                           'turned', 'pivotal', 'critical', 'decisive', 'significant']
    has_development = any(m in summary_text for m in development_markers)
    # Outcome/consequence language
    outcome_markers = ['ultimately', 'eventually', 'finally', 'resulted', 'consequence',
                       'legacy', 'impact', 'outcome', 'aftermath', 'resolution', 'concluded',
                       'ended', 'led to']
    has_outcome = any(m in summary_text for m in outcome_markers)
    # Check for coverage of beginning, middle, and end concepts
    all_kws = list(keywords)[:20]
    covered = [kw for kw in all_kws if re.search(rf'\b{re.escape(kw)}\b', summary_text)]
    kw_coverage = len(covered) / max(len(all_kws), 1)
    return {
        'has_origin': has_origin,
        'has_development': has_development,
        'has_outcome': has_outcome,
        'kw_coverage': kw_coverage,
        'arc_score': (1.0 if has_origin else 0.0) + (1.0 if has_development else 0.0) + (1.0 if has_outcome else 0.0),
        'missing_arc': [name for name, present in [('origin', has_origin), ('development', has_development), ('outcome', has_outcome)] if not present],
    }


def _check_topic_coverage(selected_sents: list[str], keywords: set[str], entities: list[str]) -> dict:
    """Quality check: verify the summary covers main topics, causes, effects, outcomes.
    Returns a dict with coverage metrics and missing items."""
    summary_text = ' '.join(selected_sents).lower()
    # Check keyword coverage (word-boundary matching to avoid false positives)
    top_kws = list(keywords)[:15]
    covered_kws = [kw for kw in top_kws if re.search(rf'\b{re.escape(kw)}\b', summary_text)]
    kw_coverage = len(covered_kws) / max(len(top_kws), 1)
    # Check entity coverage (word-boundary matching)
    top_entities = entities[:10]
    covered_entities = [e for e in top_entities if re.search(rf'\b{re.escape(e.lower())}\b', summary_text)]
    entity_coverage = len(covered_entities) / max(len(top_entities), 1)
    # Check cause-effect language
    cause_effect_markers = ['because', 'led to', 'resulted in', 'caused', 'therefore', 'thus', 'as a result', 'consequence']
    has_cause_effect = any(m in summary_text for m in cause_effect_markers)
    # Check conclusion/outcome language
    outcome_markers = ['ultimately', 'eventually', 'as a result', 'outcome', 'consequence', 'legacy', 'impact', 'significance']
    has_outcome = any(m in summary_text for m in outcome_markers)
    missing_kws = [kw for kw in top_kws[:10] if not re.search(rf'\b{re.escape(kw)}\b', summary_text)]
    return {
        'keyword_coverage': kw_coverage,
        'entity_coverage': entity_coverage,
        'has_cause_effect': has_cause_effect,
        'has_outcome': has_outcome,
        'missing_keywords': missing_kws,
        'overall_score': (kw_coverage * 0.4 + entity_coverage * 0.3 + (1.0 if has_cause_effect else 0.0) * 0.15 + (1.0 if has_outcome else 0.0) * 0.15),
    }


def generate_summary(text: str, num_sentences: int = 5, style: str = "Key Points") -> str:
    """Generate an abstractive-style summary that reads as a coherent explanation.

    Pipeline:
    0. Parse document structure (detect headings, separate structure from content)
    1. Score and select top sentences with topic diversity
    2. Trim minor details (parentheticals, examples, filler)
    3. Remove redundancy (skip sentences that repeat already-covered info)
    4. Combine related sentences into denser statements
    5. Enforce conclusion/outcome coverage
    6. Gap-fill missing critical concepts
    7. Add transitional phrases for coherent flow
    8. Quality check before returning (including heading contamination check)
    """
    # ── Step 0: Parse document structure ──
    headings, content_sentences = _parse_document_structure(text)
    sentences = content_sentences if content_sentences else split_sentences(text)
    if not sentences:
        return "Unable to generate summary — text may be too short."
    keywords = set(extract_keywords(text, 30))
    entities = _extract_named_entities(text)
    total = len(sentences)
    # ── Step 1: Score all sentences ──
    scored = []
    for i, sent in enumerate(sentences):
        score = _score_sentence_for_summary(sent, keywords, entities, i, total)
        scored.append((sent, score, i))
    # ── Step 2: Select with topic diversity + proportional section allocation ──
    # Divide text into sections and allocate picks proportionally
    num_sections = max(3, min(6, num_sentences))
    section_size = max(1, total // num_sections)
    sections = []
    for s in range(0, total, section_size):
        sections.append(scored[s:s + section_size])
    # Allocate picks per section weighted by information density (not just size)
    section_densities = []
    for section in sections:
        if not section:
            section_densities.append(0)
            continue
        section_text = ' '.join(s for s, _, _ in section)
        ent_hits = sum(1 for e in entities[:10] if e.lower() in section_text.lower())
        kw_hits = sum(1 for kw in list(keywords)[:15] if kw in section_text.lower())
        density = (ent_hits * 2 + kw_hits) / max(len(section), 1)
        section_densities.append(density)
    total_density = sum(section_densities) or 1
    selected = []
    for si, section in enumerate(sections):
        if not section:
            continue
        # Allocate proportionally by density, at least 1 pick per section
        n_picks = max(1, round(num_sentences * 2 * section_densities[si] / total_density))
        n_picks = max(1, min(n_picks, len(section)))
        # Sort section by score
        section_sorted = sorted(section, key=lambda x: x[1], reverse=True)
        for pick in section_sorted[:n_picks]:
            if len(selected) < num_sentences * 2:  # Over-select for redundancy filtering later
                selected.append(pick)
    # ── Step 3: Remove redundancy ──
    # If two sentences share >60% keyword overlap, keep only the higher-scored one
    def _keyword_overlap(s1: str, s2: str) -> float:
        t1 = set(tokenize(s1)) & keywords
        t2 = set(tokenize(s2)) & keywords
        if not t1 or not t2:
            return 0.0
        return len(t1 & t2) / min(len(t1), len(t2))
    filtered = []
    selected.sort(key=lambda x: x[1], reverse=True)
    for item in selected:
        sent = item[0]
        is_redundant = False
        for kept in filtered:
            if _keyword_overlap(sent, kept[0]) > 0.5:
                is_redundant = True
                break
        if not is_redundant:
            filtered.append(item)
    selected = filtered
    # ── Step 4: Enforce narrative arc (origin + conclusion coverage) ──
    last_20_idx = int(total * 0.8)
    first_20_idx = int(total * 0.2)
    # Ensure conclusion is covered
    has_conclusion = any(idx >= last_20_idx for _, _, idx in selected)
    if not has_conclusion and total > 5:
        conclusion_candidates = [s for s in scored if s[2] >= last_20_idx]
        if conclusion_candidates:
            conclusion_candidates.sort(key=lambda x: x[1], reverse=True)
            best_conclusion = conclusion_candidates[0]
            selected.sort(key=lambda x: x[1])
            selected[0] = best_conclusion
    # Ensure origin/causes are covered
    has_origin = any(idx <= first_20_idx for _, _, idx in selected)
    if not has_origin and total > 5:
        origin_candidates = [s for s in scored if s[2] <= first_20_idx]
        if origin_candidates:
            origin_candidates.sort(key=lambda x: x[1], reverse=True)
            best_origin = origin_candidates[0]
            selected.sort(key=lambda x: x[1])
            selected[0] = best_origin
    # ── Step 5: Gap-fill missing critical concepts ──
    selected_texts = ' '.join(s for s, _, _ in selected).lower()
    missing_entities = [e for e in entities[:8] if e.lower() not in selected_texts]
    if missing_entities:
        remaining_pool = [s for s in scored if s not in selected]
        for entity in missing_entities[:2]:
            candidates = [s for s in remaining_pool if entity.lower() in s[0].lower()]
            if candidates:
                candidates.sort(key=lambda x: x[1], reverse=True)
                best = candidates[0]
                selected.sort(key=lambda x: x[1])
                if best[1] > selected[0][1] * 0.6:
                    selected[0] = best
                    remaining_pool = [s for s in remaining_pool if s != best]
    # ── Step 6: Trim and combine ──
    # Sort by position for coherent reading
    selected.sort(key=lambda x: x[2])
    # Group nearby sentences for combination
    trimmed_sents = []
    i = 0
    selected_limited = selected[:num_sentences + 2]  # slight over-select for combining
    while i < len(selected_limited):
        sent, score, idx = selected_limited[i]
        # Group by proximity OR topic similarity (keyword overlap)
        group = [sent]
        group_tokens = set(tokenize(sent)) & keywords
        while (i + 1 < len(selected_limited) and len(group) < 3):
            next_sent, next_score, next_idx = selected_limited[i + 1]
            next_tokens = set(tokenize(next_sent)) & keywords
            # Group if position-proximate OR high topic overlap
            is_proximate = abs(next_idx - idx) < 4
            overlap = next_tokens & group_tokens
            has_overlap = bool(overlap) and len(overlap) / max(len(next_tokens), 1) > 0.3
            if is_proximate or has_overlap:
                i += 1
                group.append(selected_limited[i][0])
                group_tokens |= next_tokens
            else:
                break
        # Combine the group into one dense sentence
        if len(group) > 1:
            combined = _combine_related_sentences(group, keywords)
        else:
            combined = _trim_sentence(sent, keywords)
        if not combined or len(tokenize(combined)) < 4:
            combined = sent
        trimmed_sents.append((combined, idx))
        i += 1
    # Limit to requested count
    trimmed_sents = trimmed_sents[:num_sentences]
    # ── Step 7: Add transitional phrases for flow ──
    # ── Transitions: only add when genuinely justified by sentence content ──
    transition_map = {
        'origin': ['Initially, ', 'At the outset, '],
        'cause': ['As a result, ', 'This led to ', 'Consequently, '],
        'contrast': ['However, ', 'Despite this, ', 'Nevertheless, '],
        'development': ['Over time, ', 'As events unfolded, '],
        'outcome': ['Ultimately, ', 'In the end, '],
    }
    origin_words = {'began', 'started', 'originated', 'rooted', 'arose', 'founded', 'established'}
    cause_words = {'because', 'led', 'resulted', 'caused', 'forced', 'triggered', 'produced', 'shaped'}
    outcome_words = {'ultimately', 'eventually', 'consequence', 'legacy', 'impact', 'outcome', 'aftermath', 'resolution'}
    contrast_words = {'however', 'although', 'despite', 'nevertheless', 'but', 'whereas'}
    development_words = {'escalated', 'intensified', 'shifted', 'transformed', 'evolved', 'expanded', 'emerged', 'developed', 'grew', 'changed', 'turned'}
    all_transitions = {'however', 'although', 'despite', 'therefore', 'thus', 'meanwhile',
                       'consequently', 'furthermore', 'moreover', 'additionally',
                       'ultimately', 'eventually', 'nevertheless', 'initially', 'subsequently'}
    total_sents_count = len(trimmed_sents)
    final_sents = []
    for si, (sent, idx) in enumerate(trimmed_sents):
        sent_tokens = set(tokenize(sent))
        first_word = sent.split()[0].lower() if sent.split() else ''
        already_has_transition = first_word in all_transitions
        transition = ''
        if si > 0 and not already_has_transition:
            # Only add a transition when sentence content genuinely matches
            position_ratio = si / max(total_sents_count - 1, 1)
            if position_ratio < 0.25 and sent_tokens & origin_words:
                transition = random.choice(transition_map['origin'])
            elif sent_tokens & cause_words:
                transition = random.choice(transition_map['cause'])
            elif sent_tokens & outcome_words:
                transition = random.choice(transition_map['outcome'])
            elif sent_tokens & contrast_words:
                transition = random.choice(transition_map['contrast'])
            elif sent_tokens & development_words:
                transition = random.choice(transition_map['development'])
            # No generic fallback — if no category matches, no transition is added
        if transition:
            first_word_actual = sent.split()[0] if sent.split() else ''
            if first_word_actual.lower() in SENTENCE_STARTERS:
                sent = transition + sent[0].lower() + sent[1:]
            else:
                sent = transition + sent
        final_sents.append(sent)
    # ── Step 8: Quality check ──
    # 8a: Remove any headings that accidentally ended up in the summary
    heading_texts = {h['text'].lower().rstrip('.') for h in headings}
    final_sents = [s for s in final_sents if s.lower().rstrip('.') not in heading_texts]
    # 8b: Check topic coverage
    coverage = _check_topic_coverage(final_sents, keywords, entities)
    # If coverage is very low, try to add one more sentence for missing keywords
    if coverage['overall_score'] < 0.5 and coverage['missing_keywords'] and len(final_sents) < num_sentences:
        for mk in coverage['missing_keywords'][:2]:
            for sent, score, idx in scored:
                if re.search(rf'\b{re.escape(mk)}\b', sent.lower()) and sent not in ' '.join(final_sents):
                    trimmed = _trim_sentence(sent, keywords)
                    trimmed = _extract_key_phrase(trimmed, keywords)
                    trimmed = _compress_final_sentence(trimmed)
                    if not trimmed or len(tokenize(trimmed)) < 4:
                        trimmed = sent
                    final_sents.append(trimmed)
                    break
    # ── Step 8c: Narrative arc quality check ──
    # Verify the summary covers origin, developments, and outcomes
    if len(final_sents) >= 3:
        arc_check = _check_narrative_arc(final_sents, keywords)
        missing_arc = arc_check['missing_arc']
        selected_texts = {s[0] for s in selected}
        for arc_type in missing_arc[:1]:  # Try to fill at most 1 missing arc segment
            arc_pool = [s for s in scored if s[0] not in selected_texts]
            if arc_type == 'origin':
                first_15_idx = int(total * 0.15)
                candidates = [s for s in arc_pool if s[2] <= first_15_idx and any(w in s[0].lower() for w in ['began', 'started', 'originated', 'rooted', 'caused', 'triggered', 'sparked', 'founded'])]
            elif arc_type == 'outcome':
                last_20_idx = int(total * 0.8)
                candidates = [s for s in arc_pool if s[2] >= last_20_idx and any(w in s[0].lower() for w in ['ultimately', 'resulted', 'consequence', 'legacy', 'ended', 'concluded'])]
            else:  # development
                mid_start = int(total * 0.25)
                mid_end = int(total * 0.75)
                candidates = [s for s in arc_pool if mid_start <= s[2] <= mid_end and any(w in s[0].lower() for w in ['escalated', 'shifted', 'transformed', 'evolved', 'expanded', 'emerged', 'changed'])]
            if candidates:
                candidates.sort(key=lambda x: x[1], reverse=True)
                best_arc = candidates[0]
                trimmed_arc = _trim_sentence(best_arc[0], keywords)
                trimmed_arc = _extract_key_phrase(trimmed_arc, keywords)
                trimmed_arc = _compress_final_sentence(trimmed_arc)
                if trimmed_arc and len(tokenize(trimmed_arc)) >= 4:
                    final_sents.append(trimmed_arc)
    # ── Step 9: Minimum word count enforcement ──
    # Ensure summary meets minimum density: ~65 words per key sentence
    min_words = num_sentences * 65
    total_words = sum(len(tokenize(s)) for s in final_sents)
    if total_words < min_words and len(final_sents) < num_sentences + 3:
        # Expand by finding sentences from scored pool that add new information
        existing_text = ' '.join(final_sents).lower()
        existing_tokens = set(tokenize(existing_text)) & keywords
        expansion_pool = [s for s in scored if s[0] not in set(final_sents)]
        expansion_pool.sort(key=lambda x: x[1], reverse=True)
        for sent, score, idx in expansion_pool:
            if total_words >= min_words or len(final_sents) >= num_sentences + 3:
                break
            # Only add if it brings new keywords not already in the summary
            sent_tokens = set(tokenize(sent)) & keywords
            new_info = sent_tokens - existing_tokens
            if len(new_info) >= 2:
                trimmed = _trim_sentence(sent, keywords)
                trimmed = _extract_key_phrase(trimmed, keywords)
                trimmed = _compress_final_sentence(trimmed)
                if trimmed and len(tokenize(trimmed)) >= 6:
                    final_sents.append(trimmed)
                    existing_tokens |= set(tokenize(trimmed)) & keywords
                    total_words += len(tokenize(trimmed))
    # ── Format output ──
    if style == "Structured":
        # Partition sentences into Introduction, Main Body, and Conclusion
        # using position and content markers
        total_final = len(final_sents)
        intro_sents = []
        body_sents = []
        conclusion_sents = []
        outcome_words_local = OUTCOME_WORDS
        origin_words_local = ORIGIN_WORDS
        for si, sent in enumerate(final_sents):
            sent_tokens = set(tokenize(sent))
            pos_ratio = si / max(total_final - 1, 1)
            # Always put first sentence in introduction
            if si == 0:
                intro_sents.append(sent)
            # Last sentence goes to conclusion if we have none yet
            elif si == total_final - 1 and not conclusion_sents:
                conclusion_sents.append(sent)
            # Strong outcome language in later portion -> Conclusion
            elif pos_ratio >= 0.6 and (sent_tokens & outcome_words_local):
                conclusion_sents.append(sent)
            # Strong origin language in early portion -> Introduction
            elif pos_ratio <= 0.35 and (sent_tokens & origin_words_local):
                intro_sents.append(sent)
            # Position-based fallback
            elif pos_ratio <= 0.25:
                intro_sents.append(sent)
            elif pos_ratio >= 0.75:
                conclusion_sents.append(sent)
            else:
                body_sents.append(sent)
        # Ensure each section has at least one sentence
        if not intro_sents and body_sents:
            intro_sents.append(body_sents.pop(0))
        if not conclusion_sents and body_sents:
            conclusion_sents.append(body_sents.pop(-1))
        if not body_sents and intro_sents:
            body_sents = intro_sents[1:]
            intro_sents = intro_sents[:1]
        # Format structured output
        parts = []
        if intro_sents:
            parts.append("### Introduction\n")
            for s in intro_sents:
                parts.append(s.rstrip('.') + '.')
        if body_sents:
            parts.append("\n### Key Developments\n")
            for s in body_sents:
                parts.append(s.rstrip('.') + '.')
        if conclusion_sents:
            parts.append("\n### Conclusion & Significance\n")
            for s in conclusion_sents:
                parts.append(s.rstrip('.') + '.')
        return "\n\n".join(parts)
    elif style == "Key Points":
        lines = [f"**{i+1}.** {s.rstrip('.')}" for i, s in enumerate(final_sents)]
        return "\n\n".join(lines)
    elif style == "Paragraph":
        # Join sentences into a coherent paragraph, handling all sentence-ending punctuation
        paragraph_parts = []
        for s in final_sents:
            clean = s.rstrip('.!? ')
            if clean:
                paragraph_parts.append(clean)
        return '. '.join(paragraph_parts) + '.'
    else:  # Bullet Points
        lines = [f"- {s.rstrip('.')}" for s in final_sents]
        return "\n".join(lines)


def generate_brief_summary(text: str) -> str:
    """Generate a 2-3 sentence TL;DR that reads as a coherent explanation covering the full arc."""
    headings, content_sentences = _parse_document_structure(text)
    sentences = content_sentences if content_sentences else split_sentences(text)
    if not sentences:
        return "Text too short to summarize."
    keywords = set(extract_keywords(text, 20))
    entities = _extract_named_entities(text)
    total = len(sentences)
    # Divide into 4 sections for full arc coverage
    quarter = max(1, total // 4)
    sections = [
        sentences[:quarter],
        sentences[quarter: 2 * quarter],
        sentences[2 * quarter: 3 * quarter],
        sentences[3 * quarter:],
    ]
    best_sentences = []
    origin_words = {'began', 'started', 'originated', 'rooted', 'arose', 'founded', 'established'}
    outcome_words = {'ultimately', 'eventually', 'resulted', 'consequence', 'legacy', 'ended', 'concluded', 'aftermath', 'resolution'}
    start_idx = 0
    for qi, section in enumerate(sections):
        scored_section = []
        if not section:
            start_idx += quarter
            continue
        for i, sent in enumerate(section):
            orig_idx = start_idx + i
            score = _score_sentence_for_summary(sent, keywords, entities, orig_idx, total)
            # Bias first quarter toward origin/causes language
            if qi == 0 and any(w in sent.lower() for w in origin_words):
                score += 0.08
            # Bias last quarter toward outcome/consequence language
            if qi == len(sections) - 1 and any(w in sent.lower() for w in outcome_words):
                score += 0.08
            scored_section.append((sent, score))
        scored_section.sort(key=lambda x: x[1], reverse=True)
        # Pick best sentence and trim it
        best = scored_section[0][0]
        trimmed = _trim_sentence(best, keywords)
        trimmed = _extract_key_phrase(trimmed, keywords)
        best_sentences.append(trimmed if len(tokenize(trimmed)) >= 4 else best)
        start_idx += len(section)
    # Ensure at least 2 sentences; prefer 3
    if len(best_sentences) < 2:
        all_scored = []
        for i, sent in enumerate(sentences):
            score = _score_sentence_for_summary(sent, keywords, entities, i, total)
            all_scored.append((sent, score))
        all_scored.sort(key=lambda x: x[1], reverse=True)
        best_sentences = [_trim_sentence(s, keywords) for s, _ in all_scored[:3]]
    # Add transitional connectors for flow
    transitions = ['This led to ', 'As a result, ', 'Ultimately, ']
    result = [best_sentences[0]]
    for i, sent in enumerate(best_sentences[1:], 1):
        if i < len(transitions) and not any(sent.lower().startswith(t.lower().strip()) for t in transitions):
            sent_lower = sent.lower()
            if any(w in sent_lower for w in ['led', 'resulted', 'caused', 'because']):
                result.append('This led to ' + sent[0].lower() + sent[1:])
            elif any(w in sent_lower for w in ['ultimately', 'final', 'end', 'legacy', 'consequence']):
                result.append('Ultimately, ' + sent[0].lower() + sent[1:])
            else:
                result.append(sent)
        else:
            result.append(sent)
    final = ' '.join(result)
    return _compress_final_sentence(final)



# ─── Feature 2: Flashcard Maker ─────────────────────────────────────────────

def generate_flashcards(text: str, num_cards: int = 10) -> list[dict[str, str]]:
    """Generate challenging Q&A flashcards from text."""
    cards = []
    keywords = extract_keywords(text, 15)
    scored = score_sentences(text)
    sentences = split_sentences(text)

    # Strategy 1: Definition-based "Why" and "How" cards (harder than "What")
    defs = find_definitions_in_text(text)
    for term, defn in list(defs.items())[:num_cards // 2]:
        # Find context around this term
        context = [s for s in sentences if term.lower() in s.lower() and s != defn][:2]
        context_text = " ".join(context) if context else ""

        # Create harder prompts that require understanding, not just recall
        prompts = [
            f"Explain **why** {term} is important in this context. What role does it play?",
            f"Describe {term} and explain **how** it relates to the broader topic.",
            f"Define {term}. Then give an example from the text that illustrates it.",
            f"What would change if {term} did not exist? Explain using the text.",
        ]
        prompt = random.choice(prompts)
        cards.append({
            "front": prompt,
            "back": f"**Definition:** {defn}" + (f"\n\n**Context:** {context_text}" if context_text else ""),
            "type": "deep-definition"
        })

    # Strategy 2: Multi-concept relationship cards
    if len(keywords) >= 3:
        pairs = [(keywords[i], keywords[j]) for i in range(min(5, len(keywords))) for j in range(i+1, min(6, len(keywords)))]
        random.shuffle(pairs)
        for kw1, kw2 in pairs[:3]:
            # Find sentences mentioning both
            shared = [s for s in sentences if kw1 in s.lower() and kw2 in s.lower()][:1]
            if shared:
                cards.append({
                    "front": f"Explain the relationship between **{kw1.title()}** and **{kw2.title()}**. How do they connect?",
                    "back": f"From the text: {shared[0]}",
                    "type": "relationship"
                })

    # Strategy 3: Scenario/application cards (much harder than fill-in-blank)
    for sent, score in scored:
        if len(cards) >= num_cards:
            break
        sent_tokens = tokenize(sent)
        matched_kw = [kw for kw in keywords[:8] if kw in sent_tokens]
        if matched_kw and len(sent) > 40:
            keyword = matched_kw[0]
            cards.append({
                "front": f"The text discusses **{keyword.title()}**. Without looking at your notes, explain the key concept in your own words and why it matters.",
                "back": f"**From the text:** {sent}",
                "type": "recall"
            })

    # Strategy 4: "What's wrong?" challenge cards
    for sent, score in scored:
        if len(cards) >= num_cards:
            break
        if len(sent) > 50:
            sent_kws = [w for w in tokenize(sent) if w in keywords[:8]]
            if sent_kws:
                keyword = sent_kws[0]
                # Create a subtly wrong version
                wrong_keyword = random.choice([kw for kw in keywords if kw != keyword][:5] or ["concept"])
                wrong_sent = re.sub(rf'\b{re.escape(keyword)}\b', wrong_keyword, sent, count=1, flags=re.IGNORECASE)
                cards.append({
                    "front": f"What's wrong with this statement?\n\n\"{wrong_sent}\"",
                    "back": f"**Incorrect:** '{wrong_keyword}' should be '**{keyword}**'.\n\n**Original:** {sent}",
                    "type": "error-detection"
                })

    return cards[:num_cards]


# ─── Feature 3: Quiz Generator ──────────────────────────────────────────────

def generate_quiz(text: str, num_questions: int = 8) -> list[dict]:
    """Generate challenging multiple-choice quiz questions."""
    questions = []
    sentences = split_sentences(text)
    keywords = extract_keywords(text, 20)
    keywords_in_text = [kw for kw in keywords if kw.lower() in text.lower()]

    if not sentences or len(keywords_in_text) < 3:
        return []

    used_sentences = set()
    used_keywords = set()
    question_types = ['fill_blank', 'negative', 'inference', 'detail']
    random.shuffle(question_types)

    for sent in sentences:
        if len(questions) >= num_questions:
            break
        if sent in used_sentences or len(sent) < 30:
            continue

        sent_tokens = tokenize(sent)
        matched = [kw for kw in keywords_in_text[:15] if kw in sent_tokens and kw not in used_keywords]

        if not matched:
            continue

        answer = random.choice(matched)
        used_sentences.add(sent)
        used_keywords.add(answer)

        # Pick question type (rotate through types for variety)
        q_type = question_types[len(questions) % len(question_types)]

        if q_type == 'fill_blank':
            # Fill-in-the-blank with more plausible distractors
            question_text = re.sub(
                rf'\b{re.escape(answer)}\b', "______", sent, flags=re.IGNORECASE
            )
            if "______" not in question_text:
                continue
            # Use keywords from DIFFERENT sentences as distractors (harder to eliminate)
            other_sents = [s for s in sentences if s != sent and answer not in s.lower()]
            distractor_pool = []
            for s in other_sents:
                distractor_pool.extend([w for w in tokenize(s) if w in keywords_in_text and w != answer])
            distractor_pool = list(set(distractor_pool))
            random.shuffle(distractor_pool)
            wrong_answers = distractor_pool[:3]
            if len(wrong_answers) < 3:
                extra = [kw for kw in keywords_in_text if kw != answer and kw not in wrong_answers]
                wrong_answers.extend(extra[:3 - len(wrong_answers)])
            wrong_answers = wrong_answers[:3]
            options = wrong_answers + [answer]
            random.shuffle(options)
            questions.append({
                "question": question_text,
                "options": options,
                "answer": answer,
                "explanation": sent,
            })

        elif q_type == 'negative' and len(questions) < num_questions:
            # "Which is NOT..." questions (much harder)
            # Find 3 things that ARE mentioned and 1 that is NOT
            mentioned = [kw for kw in keywords_in_text[:10] if kw in sent.lower()]
            not_mentioned = [kw for kw in keywords_in_text if kw not in sent.lower()]
            if len(mentioned) >= 2 and len(not_mentioned) >= 1:
                correct = random.choice(not_mentioned)
                wrong = random.sample(mentioned, min(3, len(mentioned)))
                if len(wrong) < 3:
                    extra = [kw for kw in keywords_in_text if kw != correct and kw not in wrong]
                    wrong.extend(extra[:3 - len(wrong)])
                options = wrong[:3] + [correct]
                random.shuffle(options)
                questions.append({
                    "question": f"Which of the following is NOT mentioned in the context of: \"{sent[:80]}...\"",
                    "options": options,
                    "answer": correct,
                    "explanation": f"'{correct}' is not mentioned in this context. The text discusses: {', '.join(mentioned[:3])}",
                })

        elif q_type == 'inference' and len(questions) < num_questions:
            # Inference questions that require understanding, not just recall
            related = [s for s in sentences if s != sent and any(kw in s.lower() for kw in [answer])][:2]
            if related:
                wrong_pool = [kw for kw in keywords_in_text if kw != answer and kw not in sent.lower()]
                random.shuffle(wrong_pool)
                wrong_answers = wrong_pool[:3]
                if len(wrong_answers) < 3:
                    extra = [kw for kw in keywords_in_text if kw not in wrong_answers and kw != answer]
                    wrong_answers.extend(extra[:3 - len(wrong_answers)])
                options = wrong_answers[:3] + [answer]
                random.shuffle(options)
                questions.append({
                    "question": f"Based on the text, what concept best completes this idea: {sent[:100]}...",
                    "options": options,
                    "answer": answer,
                    "explanation": sent,
                })

        elif q_type == 'detail' and len(questions) < num_questions:
            # Detail-focused questions requiring specific knowledge
            question_text = re.sub(
                rf'\b{re.escape(answer)}\b', "______", sent, flags=re.IGNORECASE
            )
            if "______" not in question_text:
                continue
            # Make distractors come from the same part of the text (contextual distractors)
            sent_idx = sentences.index(sent) if sent in sentences else 0
            nearby_sents = sentences[max(0, sent_idx-2):sent_idx+3]
            nearby_kws = []
            for s in nearby_sents:
                nearby_kws.extend([w for w in tokenize(s) if w in keywords_in_text and w != answer])
            nearby_kws = list(set(nearby_kws))
            random.shuffle(nearby_kws)
            wrong_answers = nearby_kws[:3]
            if len(wrong_answers) < 3:
                extra = [kw for kw in keywords_in_text if kw != answer and kw not in wrong_answers]
                wrong_answers.extend(extra[:3 - len(wrong_answers)])
            options = wrong_answers[:3] + [answer]
            random.shuffle(options)
            questions.append({
                "question": question_text,
                "options": options,
                "answer": answer,
                "explanation": sent,
            })

    return questions


# ─── Feature 4: Key Concepts Extractor ──────────────────────────────────────

def extract_concepts(text: str) -> list[dict]:
    """Extract key concepts with context and importance."""
    keywords = extract_keywords(text, 15)
    keyphrases = extract_keyphrases(text, 8)
    sentences = split_sentences(text)

    concepts = []

    for i, kw in enumerate(keywords[:12]):
        # Find sentences containing this keyword
        context_sents = [s for s in sentences if kw.lower() in s.lower()][:2]
        importance = "High" if i < 4 else ("Medium" if i < 8 else "Notable")
        frequency = tokenize(text.lower()).count(kw)

        concepts.append({
            "name": kw.title(),
            "importance": importance,
            "frequency": frequency,
            "context": context_sents,
        })

    # Add key phrases
    for phrase in keyphrases[:5]:
        if not any(phrase.split()[0] == c["name"].lower() for c in concepts):
            context_sents = [s for s in sentences if phrase in s.lower()][:2]
            concepts.append({
                "name": phrase.title(),
                "importance": "Key Phrase",
                "frequency": text.lower().count(phrase),
                "context": context_sents,
            })

    concepts.sort(key=lambda x: x["frequency"], reverse=True)
    return concepts


# ─── Feature 5: Study Plan Generator ────────────────────────────────────────

def generate_study_plan(text: str, days: int = 7, hours_per_day: float = 2.0) -> dict:
    """Generate a structured study plan based on content."""
    concepts = extract_concepts(text)
    keywords = extract_keywords(text, 20)
    sentences = split_sentences(text)
    total_sections = max(3, len(concepts) // 2)

    # Divide content into study chunks
    chunk_size = max(1, len(sentences) // total_sections)
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = sentences[i:i + chunk_size]
        chunk_text = " ".join(chunk)
        chunk_keywords = [kw for kw in keywords if kw in " ".join(chunk).lower()]
        chunks.append({
            "content_preview": chunk_text[:150] + "...",
            "keywords": chunk_keywords[:5],
            "sentence_count": len(chunk),
        })

    # Distribute chunks across days
    plan = {}
    chunks_per_day = max(1, math.ceil(len(chunks) / days))

    for day in range(1, days + 1):
        start_idx = (day - 1) * chunks_per_day
        end_idx = min(start_idx + chunks_per_day, len(chunks))
        day_chunks = chunks[start_idx:end_idx]

        if not day_chunks:
            break

        all_kws = []
        for c in day_chunks:
            all_kws.extend(c["keywords"])

        # Vary study activities by day
        activities = []
        minutes_per_chunk = int((hours_per_day * 60) / len(day_chunks))

        for j, chunk in enumerate(day_chunks):
            if day == 1:
                activity = "Read & highlight key terms"
            elif day <= days // 2:
                activities_list = ["Take notes & summarize", "Create flashcards", "Draw concept map"]
                activity = activities_list[j % len(activities_list)]
            elif day <= days * 0.8:
                activities_list = ["Practice recall from memory", "Teach concepts aloud", "Self-quiz"]
                activity = activities_list[j % len(activities_list)]
            else:
                activities_list = ["Full review", "Practice test", "Fill knowledge gaps"]
                activity = activities_list[j % len(activities_list)]

            activities.append({
                "topic": ", ".join(all_kws[:3]) if all_kws else f"Section {start_idx + j + 1}",
                "activity": activity,
                "minutes": minutes_per_chunk,
                "preview": chunk["content_preview"],
            })

        plan[f"Day {day}"] = {
            "theme": "Learn & Absorb" if day <= 2 else
                     "Deepen Understanding" if day <= days * 0.6 else
                     "Practice & Recall" if day <= days * 0.85 else
                     "Review & Master",
            "total_minutes": int(hours_per_day * 60),
            "activities": activities,
            "keywords_to_review": list(set(all_kws))[:8],
        }

    return plan


# ─── Feature 6: Mnemonic Generator ──────────────────────────────────────────

def generate_mnemonics(text: str) -> list[dict]:
    """Generate mnemonic devices for key concepts."""
    keywords = extract_keywords(text, 10)
    mnemonics = []

    for kw in keywords[:8]:
        first_letter = kw[0].upper()

        # Acronym-based mnemonic
        related = [w for w in keywords if w != kw][:4]
        if related:
            letters = "".join(w[0].upper() for w in related[:5])
            words_for_letters = []
            for letter in letters:
                matching = [w for w in keywords if w.startswith(letter.lower()) and w != kw]
                if matching:
                    words_for_letters.append(matching[0].title())
                else:
                    common = {"A": "Always", "B": "Be", "C": "Creating",
                              "D": "Detailed", "E": "Effective", "F": "Focused",
                              "G": "Great", "H": "Helpful", "I": "Important",
                              "K": "Key", "L": "Learning", "M": "Meaningful",
                              "N": "New", "O": "Organized", "P": "Powerful",
                              "R": "Remember", "S": "Study", "T": "Thorough",
                              "U": "Useful", "V": "Very", "W": "Well"}
                    words_for_letters.append(common.get(letter.upper(), letter.upper()))

            acronym_word = "".join(w[0] for w in words_for_letters)
            mnemonics.append({
                "concept": kw.title(),
                "type": "Acronym",
                "mnemonic": f"Remember **{', '.join(r.title() for r in related[:4])}** → Think: **{acronym_word}**",
                "detail": " + ".join(words_for_letters),
            })

        # Visual association mnemonic
        associations = {
            "cell": "Picture a tiny room (cell) with organelles as furniture",
            "energy": "Imagine a battery powering a lightbulb",
            "force": "Think of pushing a door — force = push or pull",
            "water": "Visualize H₂O as two hands (H) holding a ball (O)",
            "heat": "Picture steam rising from a hot cup",
            "light": "Imagine a beam cutting through darkness",
            "acid": "Think of sour lemon juice dissolving metal",
            "growth": "Picture a seed sprouting into a tree",
            "blood": "Red rivers flowing through your body",
            "oxygen": "Think of fresh air in a forest",
        }
        for key, assoc in associations.items():
            if key in kw.lower():
                mnemonics.append({
                    "concept": kw.title(),
                    "type": "Visual",
                    "mnemonic": assoc,
                    "detail": "Create a vivid mental image for stronger recall",
                })
                break

    return mnemonics


# ─── Feature 7: Glossary Builder ────────────────────────────────────────────

def build_glossary(text: str) -> list[dict]:
    """Build an alphabetical glossary of terms."""
    defs = find_definitions_in_text(text)
    keywords = extract_keywords(text, 25)
    sentences = split_sentences(text)

    glossary = []

    for term, defn in defs.items():
        glossary.append({"term": term, "definition": defn, "source": "explicit"})

    # For top keywords without explicit definitions, find best context sentence
    for kw in keywords:
        if any(kw.lower() == g["term"].lower() for g in glossary):
            continue
        context = [s for s in sentences if kw in s.lower() and len(s) > 30]
        if context:
            glossary.append({
                "term": kw.title(),
                "definition": context[0],
                "source": "inferred"
            })

    glossary.sort(key=lambda x: x["term"].lower())
    return glossary


# ─── Feature 8: Difficulty Analyzer ─────────────────────────────────────────

def analyze_difficulty(text: str) -> dict:
    """Analyze text complexity and reading difficulty."""
    sentences = split_sentences(text)
    tokens = tokenize(text)

    if not sentences or not tokens:
        return {"level": "Unknown", "score": 0}

    # Average sentence length
    avg_sent_len = sum(len(tokenize(s)) for s in sentences) / len(sentences)

    # Average word length
    avg_word_len = sum(len(t) for t in tokens) / len(tokens)

    # Vocabulary richness (unique words / total words)
    vocab_richness = len(set(tokens)) / len(tokens)

    # Technical term density (words > 8 chars or with specific suffixes)
    technical = [t for t in tokens if len(t) > 8 or t.endswith(('tion', 'ment', 'ness', 'ity', 'ism', 'ology', 'ography'))]
    tech_density = len(technical) / len(tokens) if tokens else 0

    # Flesch-Kincaid approximation
    syllable_count = sum(max(1, len(re.findall(r'[aeiouy]+', t))) for t in tokens)
    flesch_kincaid = (0.39 * avg_sent_len) + (11.8 * (syllable_count / len(tokens))) - 15.59

    # Composite difficulty score (0-100)
    score = min(100, max(0, int(
        (avg_sent_len / 30) * 25 +
        (avg_word_len / 10) * 20 +
        vocab_richness * 25 +
        tech_density * 30
    )))

    if score < 25:
        level = "Beginner"
        color = "Easy"
        tip = "This text is straightforward. Good for introductory learning."
    elif score < 50:
        level = "Intermediate"
        color = "Moderate"
        tip = "Moderate complexity. Take notes on technical terms."
    elif score < 75:
        level = "Advanced"
        color = "Challenging"
        tip = "Complex material. Consider breaking it into smaller sections."
    else:
        level = "Expert"
        color = "Very Challenging"
        tip = "Highly complex. Use flashcards and repeated review."

    return {
        "level": level,
        "color": color,
        "score": score,
        "tip": tip,
        "stats": {
            "sentences": len(sentences),
            "words": len(tokens),
            "unique_words": len(set(tokens)),
            "avg_sentence_length": round(avg_sent_len, 1),
            "avg_word_length": round(avg_word_len, 1),
            "vocabulary_richness": round(vocab_richness * 100, 1),
            "technical_density": round(tech_density * 100, 1),
            "reading_level": f"Grade {max(1, round(flesch_kincaid))}",
        }
    }


# ─── Feature 9: Outline / Structure Generator ──────────────────────────────

def generate_outline(text: str) -> list[dict]:
    """Generate a hierarchical outline of the text."""
    sentences = split_sentences(text)
    keywords = extract_keywords(text, 15)
    keyphrases = extract_keyphrases(text, 5)

    if not sentences:
        return []

    # Cluster sentences by keyword overlap
    sections = []
    used = set()

    # Find section-like sentences (often contain colons, are shorter, or have specific patterns)
    heading_candidates = [s for s in sentences if (
        s.endswith(':') or
        (len(s) < 80 and any(s.lower().startswith(w) for w in
         ['the', 'a', 'an', 'how', 'what', 'why', 'when', 'introduction',
          'overview', 'summary', 'conclusion', 'first', 'second', 'third']))
    )]

    if heading_candidates:
        for heading in heading_candidates[:6]:
            # Find related sentences (ones that share keywords with the heading)
            heading_kws = set(tokenize(heading)) & set(keywords)
            related = []
            for s in sentences:
                if s != heading and s not in used:
                    s_kws = set(tokenize(s)) & set(keywords)
                    if heading_kws & s_kws:
                        related.append(s)
                        used.add(s)
                        if len(related) >= 4:
                            break

            sections.append({
                "heading": heading.rstrip(':'),
                "points": related,
                "keywords": list(heading_kws)[:3],
            })
            used.add(heading)

    # Fill remaining sentences into sections based on keyword clusters
    remaining = [s for s in sentences if s not in used]
    if remaining and len(sections) < 3:
        chunk_size = max(1, len(remaining) // max(1, 5 - len(sections)))
        for i in range(0, len(remaining), chunk_size):
            chunk = remaining[i:i + chunk_size]
            chunk_text = " ".join(chunk)
            chunk_kws = [kw for kw in keywords if kw in chunk_text.lower()][:3]
            topic = " & ".join(kw.title() for kw in chunk_kws) if chunk_kws else f"Topic {len(sections) + 1}"
            sections.append({
                "heading": topic,
                "points": chunk,
                "keywords": chunk_kws,
            })

    return sections


# ─── Feature 10: Concept Map Generator ──────────────────────────────────────

def generate_concept_map(text: str) -> dict:
    """Generate a concept relationship map."""
    keywords = extract_keywords(text, 12)
    sentences = split_sentences(text)

    nodes = []
    edges = []

    for i, kw in enumerate(keywords[:10]):
        frequency = tokenize(text.lower()).count(kw)
        connections = []
        for other_kw in keywords:
            if other_kw != kw:
                # Check if both keywords appear in the same sentence
                for s in sentences:
                    if kw in s.lower() and other_kw in s.lower():
                        connections.append(other_kw)
                        break

        nodes.append({
            "id": i,
            "label": kw.title(),
            "size": frequency,
            "connections": len(connections),
        })

        for conn in connections:
            target_idx = keywords.index(conn) if conn in keywords else -1
            if target_idx >= 0:
                edge = (min(i, target_idx), max(i, target_idx))
                if edge not in edges:
                    edges.append(edge)

    return {"nodes": nodes, "edges": edges}


# ─── Feature 11: Practice Questions (Open-Ended) ────────────────────────────

def generate_practice_questions(text: str, num_q: int = 6) -> list[dict]:
    """Generate open-ended practice questions for deeper understanding."""
    keywords = extract_keywords(text, 15)
    sentences = split_sentences(text)

    question_templates = [
        ("Explain the relationship between {0} and {1}.", "analysis"),
        ("Compare and contrast {0} with {1}.", "comparison"),
        ("What would happen if {0} were removed from {1}?", "critical"),
        ("How does {0} contribute to the overall understanding of {1}?", "synthesis"),
        ("Why is {0} important in the context of {1}?", "evaluation"),
        ("Provide an example that illustrates {0}.", "application"),
        ("What are the implications of {0}?", "evaluation"),
        ("How might {0} be applied in a real-world scenario?", "application"),
        ("What evidence supports the idea that {0}?", "analysis"),
        ("Summarize the main argument about {0} in your own words.", "comprehension"),
    ]

    questions = []
    used_combos = set()

    for template, bloom_level in question_templates:
        if len(questions) >= num_q:
            break

        if "{1}" in template:
            # Two-concept question
            if len(keywords) >= 2:
                pair = tuple(sorted(random.sample(keywords[:8], 2)))
                if pair not in used_combos:
                    q = template.format(pair[0].title(), pair[1].title())
                    questions.append({
                        "question": q,
                        "bloom_level": bloom_level,
                        "hints": [f"Think about how {pair[0]} relates to {pair[1]}",
                                  f"Review sentences mentioning both terms"],
                    })
                    used_combos.add(pair)
        else:
            # Single-concept question
            if keywords:
                kw = random.choice(keywords[:8])
                q = template.format(kw.title())
                if not any(kw in qu["question"].lower() for qu in questions):
                    context = [s for s in sentences if kw in s.lower()][:1]
                    questions.append({
                        "question": q,
                        "bloom_level": bloom_level,
                        "hints": [f"Focus on: {kw.title()}",
                                  f"Context: {context[0][:100]}..." if context else "Review relevant sections"],
                    })

    return questions


# ─── Feature 12: Study Tips & Techniques ────────────────────────────────────

def generate_study_tips(text: str, difficulty: dict) -> list[dict]:
    """Generate personalized study tips based on content analysis."""
    keywords = extract_keywords(text, 10)
    stats = difficulty.get("stats", {})
    level = difficulty.get("level", "Intermediate")

    tips = []

    # Tip 1: Based on difficulty
    if level in ("Expert", "Advanced"):
        tips.append({
            "icon": "CHUNK",
            "title": "Chunk the Material",
            "tip": "This is complex material. Break it into 15-20 minute study chunks with 5-minute breaks between them. Focus on understanding one concept before moving to the next.",
            "technique": "Pomodoro + Chunking"
        })
    else:
        tips.append({
            "icon": "READ",
            "title": "Active Reading",
            "tip": "Read through once quickly for overview, then re-read slowly while highlighting key terms. Summarize each section in your own words.",
            "technique": "SQ3R Method"
        })

    # Tip 2: Based on vocabulary richness
    vocab_richness = stats.get("vocabulary_richness", 50)
    if vocab_richness > 60:
        tips.append({
            "icon": "VOCAB",
            "title": "Build a Vocabulary Sheet",
            "tip": f"This text has rich vocabulary ({vocab_richness}% unique words). Create a dedicated vocabulary sheet with terms and definitions. Review it daily.",
            "technique": "Spaced Repetition"
        })

    # Tip 3: Based on content density
    word_count = stats.get("words", 0)
    if word_count > 500:
        tips.append({
            "icon": "RECALL",
            "title": "Use Active Recall",
            "tip": "After reading each section, close your notes and try to recall the main points. Use the flashcards and quizzes generated by Mesmery to test yourself.",
            "technique": "Active Recall Testing"
        })

    # Tip 4: General but high-impact
    tips.append({
        "icon": "SPACED",
        "title": "Spaced Repetition Schedule",
        "tip": "Review the material at increasing intervals: 1 day after learning, then 3 days, then 7 days, then 14 days. This dramatically improves long-term retention.",
        "technique": "Ebbinghaus Forgetting Curve"
    })

    # Tip 5: Feynman Technique
    top_concepts = [kw.title() for kw in keywords[:3]]
    tips.append({
        "icon": "FEYNMAN",
        "title": "The Feynman Technique",
        "tip": f"Try explaining {', '.join(top_concepts)} to someone with no background in the subject. If you can't explain it simply, you don't understand it well enough.",
        "technique": "Feynman Technique"
    })

    # Tip 6: Elaborative Interrogation
    tips.append({
        "icon": "ASK WHY",
        "title": "Ask 'Why' and 'How'",
        "tip": "For every fact you learn, ask yourself 'Why is this true?' and 'How do I know?' This deepens understanding and creates stronger memory traces.",
        "technique": "Elaborative Interrogation"
    })

    # Tip 7: Based on numbers/dates in text
    numbers = extract_numbers_and_dates(text)
    if numbers:
        tips.append({
            "icon": "NUMBERS",
            "title": "Numbers Need Stories",
            "tip": f"This text contains {len(numbers)} specific numbers/dates. Convert these into stories or visual associations. Example: link years to personal events or create number rhymes.",
            "technique": "Narrative Encoding"
        })

    # Tip 8: Interleaving
    tips.append({
        "icon": "MIX",
        "title": "Interleave Your Practice",
        "tip": "Don't just study one topic at a time. Mix practice questions from different sections. This feels harder but builds stronger connections and better transfer of knowledge.",
        "technique": "Interleaving"
    })

    return tips


# ─── AI Engine ───────────────────────────────────────────────────────────────

def ai_generate_all(text: str) -> dict | None:
    """
    Send text to a real AI model and get ALL 12 features back in one call.
    Tries OVHcloud (free, no API key) first, then Gemini if key provided.
    Results are cached so only 1 API call is made per text.
    """
    # Cache key: hash of text + provider
    cache_key = f"ai_{hash(text)}_{st.session_state.get('ai_provider', 'ovhcloud')}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    provider = st.session_state.get("ai_provider", "ovhcloud")

    system_prompt = (
        "You are an expert content curator specializing in summarization and document analysis. "
        "Given the user's study material, generate all 12 features. "
        "Respond with ONLY a JSON object (no markdown, no explanation). "
        "The JSON must have these exact keys: "
        "summary (string, a structured summary of 6-10 sentences that MUST follow this format: "
        "'\n### Introduction\n[introductory context and background]\n\n### Key Developments\n[main body covering causes, policies, turning points, and developments in chronological order]\n\n### Conclusion & Significance\n[final outcomes and historical significance]'. "
        "The summary MUST: maintain chronological order throughout; identify and eliminate "
        "duplicate information by merging related concepts; ensure transitions reflect true "
        "relationships between ideas; prioritize foundational causes, major policies, turning "
        "points, and long-term consequences over secondary details; cover the beginning, middle, "
        "and conclusion of the document; and explain final outcomes and historical significance), "
        "brief_summary (string, 2-3 sentence TL;DR covering the full arc from beginning to end), "
        "flashcards (array of {front, back, type} objects, 8-10 cards), "
        "quiz (array of {question, options (array of 4), answer, explanation} objects, 6-8 questions), "
        "key_concepts (array of {name, importance, context} objects, 8-10 concepts), "
        "study_plan (object with day1-day5 keys, each having theme and activities array of {topic, activity, minutes}), "
        "mnemonics (array of {concept, type, mnemonic, detail} objects, 5-6 mnemonics), "
        "glossary (array of {term, definition} objects, 8-12 terms), "
        "outline (array of {heading, points (array of strings)} objects, 4-6 sections), "
        "concept_map (object with nodes array of {label, connections} and edges array of [from, to]), "
        "practice_questions (array of {question, bloom_level, hints (array of strings)} objects, 5-6 questions), "
        "study_tips (array of {icon (text label), title, tip, technique} objects, 6-8 tips). "
        "Make quiz questions genuinely challenging with plausible wrong answers. "
        "Make flashcards test real understanding, not just definitions. "
        "All content must come from the provided text."
    )

    # Truncate very long texts to fit in context
    max_chars = 8000
    truncated = text[:max_chars] + ("..." if len(text) > max_chars else "")

    result = None
    error_msg = ""

    # Try OVHcloud (free, no API key)
    if provider == "ovhcloud":
        try:
            client_body = json.dumps({
                "model": "Meta-Llama-3_3-70B-Instruct",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate all study features for this text:\n\n{truncated}"},
                ],
                "max_tokens": 8000,
                "temperature": 0.3,
                "stream": False,
            }).encode("utf-8")

            req = urllib.request.Request(
                "https://oai.endpoints.kepler.ai.cloud.ovh.net/v1/chat/completions",
                data=client_body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer not-needed",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
                content = resp_data["choices"][0]["message"]["content"]
                result = _parse_ai_json(content)
        except Exception as e:
            error_msg = f"OVHcloud error: {e}"

    # Try Gemini (free tier)
    if provider == "gemini":
        api_key = st.session_state.get("gemini_key", "")
        if not api_key:
            error_msg = "No Gemini API key provided."
        else:
            try:
                payload = json.dumps({
                    "contents": [{
                        "parts": [{
                            "text": f"{system_prompt}\n\nStudy material:\n{truncated}"
                        }]
                    }],
                    "generationConfig": {
                        "maxOutputTokens": 8000,
                        "temperature": 0.3,
                    }
                }).encode("utf-8")

                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
                req = urllib.request.Request(
                    url,
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    content = resp_data["candidates"][0]["content"]["parts"][0]["text"]
                    result = _parse_ai_json(content)
            except Exception as e:
                error_msg = f"Gemini error: {e}"

    if result and isinstance(result, dict) and "summary" in result:
        st.session_state[cache_key] = result
        st.session_state.pop("ai_error", None)
        return result

    # Store error for display
    if error_msg:
        st.session_state["ai_error"] = error_msg
    return None


def _parse_ai_json(content: str) -> dict | None:
    """Parse JSON from AI response, handling markdown code blocks."""
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Try to extract JSON from markdown code blocks
    for pattern in [r"```(?:json)?\s*\n?([\s\S]*?)\n?```"]:
        match = re.search(pattern, content)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except json.JSONDecodeError:
                continue

    # Find outermost { ... } by locating first { and last }
    first_brace = content.find("{")
    last_brace = content.rfind("}")
    if first_brace != -1 and last_brace > first_brace:
        try:
            return json.loads(content[first_brace:last_brace + 1])
        except json.JSONDecodeError:
            pass

    return None


def get_ai_results() -> dict | None:
    """Get cached AI results if available."""
    return st.session_state.get("ai_results")


# ─── Main App ────────────────────────────────────────────────────────────────

def main():
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

    # ── Initialize session state ─────────────────────────────────────────
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
    if "active_page" not in st.session_state:
        st.session_state.active_page = "home"
    if "flashcard_idx" not in st.session_state:
        st.session_state.flashcard_idx = 0
    if "flashcard_show_back" not in st.session_state:
        st.session_state.flashcard_show_back = False
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    # ── Sidebar ──────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown('<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;"><svg width="32" height="32" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="80" height="80" rx="16" fill="none"/><path d="M16 56V24L28 44L40 24L52 44L64 24V56" stroke="#e63946" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><line x1="16" y1="56" x2="64" y2="56" stroke="#f5f5f5" stroke-width="3" stroke-linecap="round"/></svg><span style="font-weight:700;font-size:1.1em;letter-spacing:-0.03em;">MESMERY</span></div>', unsafe_allow_html=True)

# ── Theme Dropdown ────────────────────────────────────────────
        theme_options = ["Dark", "Light", "Classic"]
        current_idx = {"dark": 0, "light": 1, "classic": 2}.get(st.session_state.theme, 0)
        new_theme = st.selectbox(
            "Theme",
            theme_options,
            index=current_idx,
            key="theme_select",
        )
        new_theme_key = new_theme.lower()
        if new_theme_key != st.session_state.theme:
            st.session_state.theme = new_theme_key
            st.rerun()

        # ── AI Engine Section ─────────────────────────────────────────
        st.markdown('<div class="sidebar-header">AI Engine</div>', unsafe_allow_html=True)

        ai_provider = st.selectbox(
            "Provider",
            ["ovhcloud", "gemini"],
            format_func=lambda x: "OVHcloud (Free)" if x == "ovhcloud" else "Google Gemini (Free Tier)",
            key="ai_provider_select",
            index=0 if st.session_state.get("ai_provider", "ovhcloud") == "ovhcloud" else 1,
        )
        st.session_state.ai_provider = ai_provider

        if ai_provider == "gemini":
            gemini_key = st.text_input(
                "Gemini API Key",
                value=st.session_state.get("gemini_key", ""),
                type="password",
                placeholder="Paste your free key from aistudio.google.com",
                key="gemini_key_input",
            )
            st.session_state.gemini_key = gemini_key
            st.markdown("[Get a free key ->](https://aistudio.google.com/apikey)")

        # AI Generate button
        ai_results = get_ai_results()
        if ai_results:
            st.success("AI results ready — all features enhanced.")
            if st.button("Clear AI Results", key="clear_ai", use_container_width=True):
                keys_to_remove = [k for k in st.session_state if k.startswith("ai_")]
                for k in keys_to_remove:
                    del st.session_state[k]
                st.rerun()
        else:
            if st.button("Generate with AI", key="gen_ai", use_container_width=True):
                if not text:
                    st.warning("Paste study material first!")
                else:
                    with st.spinner(f"Sending to {'OVHcloud AI' if ai_provider == 'ovhcloud' else 'Gemini'} (may take 15-30s)..."):
                        result = ai_generate_all(text)
                    if result:
                        st.session_state.ai_results = result
                        st.rerun()
                    else:
                        err = st.session_state.get("ai_error", "Unknown error")
                        st.error(f"AI failed: {err}. Using local NLP instead.")

        # ── Navigation ───────────────────────────────────────────────
        # Define all nav pages in one place
        all_pages = [
            ("Home", "home"), ("Summarizer", "summarizer"),
            ("Flashcards", "flashcards"), ("Quiz", "quiz"),
            ("Key Concepts", "concepts"), ("Study Plan", "study_plan"),
            ("Mnemonics", "mnemonics"), ("Glossary", "glossary"),
            ("Difficulty", "difficulty"), ("Outline", "outline"),
            ("Concept Map", "concept_map"), ("Practice Qs", "practice"),
            ("Study Tips", "study_tips"),
        ]

        # Study Tools section
        st.markdown('<div class="sidebar-header">Study Tools</div>', unsafe_allow_html=True)
        for label, page_id in all_pages[:7]:
            if st.button(label, key=f"nav_{page_id}", use_container_width=True):
                st.session_state.active_page = page_id
                st.rerun()

        # Analysis section
        st.markdown('<div class="sidebar-header">Analysis</div>', unsafe_allow_html=True)
        for label, page_id in all_pages[7:]:
            if st.button(label, key=f"nav_{page_id}", use_container_width=True):
                st.session_state.active_page = page_id
                st.rerun()

        st.markdown("---")

        # Input section
        st.markdown('<div class="sidebar-header">Study Material</div>', unsafe_allow_html=True)

        input_text = st.text_area(
            "Study Material",
            value=st.session_state.input_text,
            height=200,
            placeholder="Paste your lecture notes, textbook chapter, article, or any study material here...\n\nThe more text you provide, the better the AI features work!",
            label_visibility="collapsed",
        )

        if input_text != st.session_state.input_text:
            st.session_state.input_text = input_text

        word_count = len(input_text.split()) if input_text else 0
        st.caption(f"{word_count:,} words / {len(input_text):,} characters")

        if input_text and word_count < 20:
            st.warning("Add more text for better results (100+ words recommended)")

        st.markdown("---")
        st.caption("Mesmery — Study smarter, not harder.")

    # ── Page Content ─────────────────────────────────────────────────────
    text = st.session_state.input_text.strip()

    if st.session_state.active_page == "home":
        render_home(text)
    elif not text:
        render_empty_state()
    elif st.session_state.active_page == "summarizer":
        render_summarizer(text)
    elif st.session_state.active_page == "flashcards":
        render_flashcards(text)
    elif st.session_state.active_page == "quiz":
        render_quiz(text)
    elif st.session_state.active_page == "concepts":
        render_concepts(text)
    elif st.session_state.active_page == "study_plan":
        render_study_plan(text)
    elif st.session_state.active_page == "mnemonics":
        render_mnemonics(text)
    elif st.session_state.active_page == "glossary":
        render_glossary(text)
    elif st.session_state.active_page == "difficulty":
        render_difficulty(text)
    elif st.session_state.active_page == "outline":
        render_outline(text)
    elif st.session_state.active_page == "concept_map":
        render_concept_map(text)
    elif st.session_state.active_page == "practice":
        render_practice(text)
    elif st.session_state.active_page == "study_tips":
        render_study_tips_page(text)


# ─── Page Renderers ──────────────────────────────────────────────────────────

def render_home(text: str):
    """Render the home page."""
    st.markdown("""
    <div style="text-align:center; padding: 40px 0 20px;">
        <div style="text-align:center;margin-bottom:8px"><svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="80" height="80" rx="16" fill="none"/><path d="M16 56V24L28 44L40 24L52 44L64 24V56" stroke="#e63946" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><line x1="16" y1="56" x2="64" y2="56" stroke="#f5f5f5" stroke-width="3" stroke-linecap="round"/></svg></div><div class="hero-title">MESMERY</div>
        <div class="hero-sub">AI-Powered Study Platform · Paste · Learn · Master</div>
    </div>
    """, unsafe_allow_html=True)

    if not text:
        st.markdown("""
        <div class="empty-state">
            <h3>Welcome to Mesmery</h3>
            <p>Paste your lecture notes, textbook content, or study material in the sidebar to get started.</p>
            <p>Mesmery will analyze your content and generate:</p>
            <p>Summaries · Flashcards · Quizzes · Study Plans · Mnemonics · and more</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Features")

        features = [
            ("01", "Smart Summarizer", "Abstractive summarization that paraphrases, combines related ideas, and removes redundancy — key points, bullet, or paragraph"),
            ("02", "Flashcard Maker", "Auto-generated Q&A cards from your content with fill-in-the-blank and definition cards"),
            ("03", "Quiz Generator", "Multiple-choice questions generated from your material with instant grading"),
            ("04", "Key Concepts", "Identifies and ranks the most important concepts with context"),
            ("05", "Study Plan", "Structured day-by-day study schedule based on content complexity"),
            ("06", "Mnemonic Generator", "Creates memory aids — acronyms, visual associations, and memory tricks"),
            ("07", "Glossary Builder", "Auto-builds an alphabetical glossary of terms and definitions"),
            ("08", "Difficulty Analyzer", "Readability analysis with Flesch-Kincaid scoring and vocabulary metrics"),
            ("09", "Outline Generator", "Creates a structured hierarchical outline of your content"),
            ("10", "Concept Map", "Visualizes relationships between key concepts"),
            ("11", "Practice Questions", "Open-ended questions at various Bloom's taxonomy levels"),
            ("12", "Study Tips", "Personalized techniques based on your content's difficulty and structure"),
        ]

        cols = st.columns(3)
        for i, (icon, title, desc) in enumerate(features):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="mesmery-card">
                    <div style="font-size:0.7em; font-weight:600; letter-spacing:0.1em; opacity:0.4; margin-bottom:8px;">{icon}</div>
                    <div style="font-weight:700; font-size:1.05em; margin-bottom:6px;">{title}</div>
                    <div style="font-size:0.85em; opacity:0.6;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

    else:
        # Quick overview when text is loaded
        ai = get_ai_results()
        difficulty = analyze_difficulty(text)
        keywords = extract_keywords(text, 5)
        word_count = len(text.split())
        brief = ai.get("brief_summary", generate_brief_summary(text)) if ai else generate_brief_summary(text)

        st.markdown("### Content Overview")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Words", f"{word_count:,}")
        with c2:
            st.metric("Difficulty", difficulty["level"])
        with c3:
            st.metric("Reading Level", difficulty["stats"]["reading_level"])
        with c4:
            st.metric("Vocabulary", f"{difficulty['stats']['vocabulary_richness']}%")

        st.markdown("---")

        st.markdown("### TL;DR")
        st.markdown(f"*{brief}*")

        st.markdown("### Top Keywords")
        tags_html = "".join(f'<span class="tag">{kw.title()}</span>' for kw in keywords)
        st.markdown(tags_html, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Quick Actions")
        cols = st.columns(4)
        quick_pages = [
            ("Summarize", "summarizer"),
            ("Flashcards", "flashcards"),
            ("Take Quiz", "quiz"),
            ("Study Plan", "study_plan"),
        ]
        for i, (label, page_id) in enumerate(quick_pages):
            with cols[i]:
                if st.button(label, key=f"quick_{page_id}", use_container_width=True):
                    st.session_state.active_page = page_id
                    st.rerun()


def render_empty_state():
    st.markdown("""
    <div class="empty-state">
        <h3>No Content Loaded</h3>
        <p>Paste your study material in the sidebar to use this feature.</p>
        <p>Tip: The more text you provide, the better the results!</p>
    </div>
    """, unsafe_allow_html=True)


def render_summarizer(text: str):
    ai = get_ai_results()

    # ── Header ──────────────────────────────────────────────
    st.markdown("## \u2699\ufe0f Summarizer")
    if ai:
        st.markdown("*AI-enhanced structured summarization with chronological analysis and quality metrics.*")
    else:
        st.markdown("*Abstractive summarization engine \u2014 paraphrases, combines related ideas, removes redundancy, and enforces narrative arc coverage.*")

    # ── Controls ────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        num_sentences = st.slider("Detail level (key sentences)", 3, 15, 7, key="sum_slider")
    with col2:
        style = st.selectbox(
            "Summary format",
            ["Structured", "Key Points", "Bullet Points", "Paragraph"],
            key="sum_style",
            index=0,
        )

    # Style descriptions
    style_desc = {
        "Structured": "Organized into Introduction, Key Developments, and Conclusion sections.",
        "Key Points": "Numbered list of the most important points.",
        "Bullet Points": "Concise bullet-point format.",
        "Paragraph": "Flowing paragraph for reading comprehension.",
    }
    st.caption(style_desc.get(style, ""))

    # ── Generate Button ─────────────────────────────────────
    if st.button("Generate Summary", key="sum_btn", use_container_width=True, type="primary"):
        with st.spinner("Analyzing structure, scoring sentences, and enforcing narrative arc..." if ai else "Analyzing text structure and extracting key information..."):
            if ai:
                raw_ai_summary = ai.get("summary", "")
                # If AI summary doesn't have our structured headers, use local
                if style == "Structured" and "### Introduction" not in raw_ai_summary:
                    summary = generate_summary(text, num_sentences, style)
                else:
                    summary = raw_ai_summary if style == "Paragraph" or "###" in raw_ai_summary else generate_summary(text, num_sentences, style)
            else:
                summary = generate_summary(text, num_sentences, style)

        st.markdown("---")

        # ── Summary Display ─────────────────────────────────
        if style == "Structured" and "###" in summary:
            # Parse structured sections and render as styled cards
            sections = re.split(r'\n###\s+', summary)
            for section in sections:
                section = section.strip()
                if not section:
                    continue
                lines = section.split('\n', 1)
                header = lines[0].strip()
                body = lines[1].strip() if len(lines) > 1 else ""
                if not body:
                    body = header
                    header = "Summary"
                safe_body = html.escape(body)
                st.markdown(f"""
                <div class="summary-section">
                    <div class="summary-section-header">
                        <span class="dot"></span>{header}
                    </div>
                    <div class="summary-content">{safe_body}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("### Summary")
            st.markdown(summary)

        # ── Analysis Dashboard ───────────────────────────────
        st.markdown("---")
        st.markdown("#### \U0001f4ca Analysis")

        original_words = len(text.split())
        summary_words = len(summary.split())
        ratio = max(1, int((1 - summary_words / max(original_words, 1)) * 100))

        # Top metrics row
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-highlight">
                <div class="metric-val">{original_words:,}</div>
                <div class="metric-label">Original Words</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-highlight">
                <div class="metric-val">{summary_words:,}</div>
                <div class="metric-label">Summary Words</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-highlight">
                <div class="metric-val">{ratio}%</div>
                <div class="metric-label">Compression</div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            actual_sents = len([s for s in re.split(r'(?<=[.!?])\s+', summary) if len(s.strip()) > 10])
            st.markdown(f"""
            <div class="metric-highlight">
                <div class="metric-val">{actual_sents}</div>
                <div class="metric-label">Sentences</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Quality Indicators ───────────────────────────────
        keywords = set(extract_keywords(text, 30))
        entities = _extract_named_entities(text)
        sentences_for_check = split_sentences(summary.replace('###', '').strip())
        coverage = _check_topic_coverage(sentences_for_check, keywords, entities)
        arc = _check_narrative_arc(sentences_for_check, keywords)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Quality Indicators**")

        metrics_data = [
            ("Topic Coverage", f"{int(coverage['keyword_coverage'] * 100)}%", coverage['keyword_coverage']),
            ("Entity Coverage", f"{int(coverage['entity_coverage'] * 100)}%", coverage['entity_coverage']),
            ("Cause & Effect", "Present" if coverage['has_cause_effect'] else "Missing", 1.0 if coverage['has_cause_effect'] else 0.0),
            ("Narrative Arc", f"{int(arc['arc_score'] / 3 * 100)}%", arc['arc_score'] / 3),
        ]

        for label, value, pct in metrics_data:
            pct_clamped = max(0.0, min(1.0, pct))
            level = "high" if pct_clamped >= 0.6 else ("medium" if pct_clamped >= 0.3 else "low")
            badge_class = "pass" if pct_clamped >= 0.5 else "warn"
            badge_text = "Good" if pct_clamped >= 0.6 else ("OK" if pct_clamped >= 0.3 else "Low")
            st.markdown(f"""
            <div class="quality-row">
                <span class="quality-label">{label}</span>
                <div class="quality-bar-bg">
                    <div class="quality-bar-fill {level}" style="width: {pct_clamped * 100:.0f}%"></div>
                </div>
                <span class="quality-value">{value}</span>
                <span class="quality-badge {badge_class}">{badge_text}</span>
            </div>
            """, unsafe_allow_html=True)

        # Narrative arc indicators
        arc_items = []
        for name, present in [("Origins/Causes", arc['has_origin']), ("Key Developments", arc['has_development']), ("Outcomes", arc['has_outcome'])]:
            badge = "pass" if present else "warn"
            icon = "\u2714" if present else "\u2718"
            arc_items.append(f"{icon} {name}")
        st.markdown(f"*Narrative arc:* {' | '.join(arc_items)}")

        # ── TL;DR ────────────────────────────────────────────
        st.markdown("---")
        st.markdown("#### TL;DR")
        brief = ai.get("brief_summary", generate_brief_summary(text)) if ai else generate_brief_summary(text)
        # Render TL;DR as styled card with markdown converted to HTML
        brief_html = html.escape(brief)
        brief_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', brief_html)
        brief_html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', brief_html)
        st.markdown(f'<div class="tldr-card"><em>{brief_html}</em></div>', unsafe_allow_html=True)

        # ── Key Terms in Summary ─────────────────────────────
        summary_kws = [kw for kw in extract_keywords(summary, 8) if kw not in STOP_WORDS]
        if summary_kws:
            tags_html = " ".join(f'<span class="tag">{kw.title()}</span>' for kw in summary_kws[:10])
            st.markdown(f"*Key terms:* {tags_html}", unsafe_allow_html=True)


def render_flashcards(text: str):
    ai = get_ai_results()
    st.markdown("## Flashcards")
    if ai:
        st.markdown("*AI-powered flashcards*")
    else:
        st.markdown("Auto-generated flashcards from your content. Click a card to flip it!")

    num_cards = st.slider("Number of cards", 5, 20, 10, key="fc_slider")

    if st.button("Generate Flashcards", key="fc_btn", use_container_width=True):
        with st.spinner("Creating AI flashcards..." if ai else "Creating flashcards from your content..."):
            if ai and "flashcards" in ai:
                cards = ai["flashcards"][:num_cards]
            else:
                cards = generate_flashcards(text, num_cards)
            st.session_state.flashcards = cards
            st.session_state.flashcard_idx = 0
            st.session_state.flashcard_show_back = False

    if "flashcards" in st.session_state and st.session_state.flashcards:
        cards = st.session_state.flashcards
        idx = st.session_state.flashcard_idx

        st.markdown(f"**Card {idx + 1} of {len(cards)}**")

        # Progress bar
        progress = (idx + 1) / len(cards)
        st.markdown(f"""
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: {progress * 100}%"></div>
        </div>
        """, unsafe_allow_html=True)

        card = cards[idx]
        card_type = card.get("type", "general")
        type_label = {
            "definition": "Definition", "fill-blank": "Fill in the Blank",
            "explain": "Explain", "general": "General",
            "deep-definition": "Deep Understanding", "relationship": "Relationship",
            "recall": "Active Recall", "error-detection": "Error Detection",
        }.get(card_type, "General")

        st.markdown(f'<span class="tag">{type_label}</span>', unsafe_allow_html=True)

        if not st.session_state.flashcard_show_back:
            st.markdown(f"""
            <div class="flashcard">
                <div>{card['front']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Flip Card", key="flip_btn", use_container_width=True):
                st.session_state.flashcard_show_back = True
                st.rerun()
        else:
            st.markdown(f"""
            <div class="flashcard">
                <div>{card['back']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Show Question", key="flip_back_btn", use_container_width=True):
                st.session_state.flashcard_show_back = False
                st.rerun()

        # Navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("Previous", key="fc_prev", disabled=(idx == 0)):
                st.session_state.flashcard_idx = max(0, idx - 1)
                st.session_state.flashcard_show_back = False
                st.rerun()
        with col2:
            if st.button("Shuffle", key="fc_shuffle"):
                random.shuffle(st.session_state.flashcards)
                st.session_state.flashcard_idx = 0
                st.session_state.flashcard_show_back = False
                st.rerun()
        with col3:
            if st.button("Next", key="fc_next", disabled=(idx >= len(cards) - 1)):
                st.session_state.flashcard_idx = min(len(cards) - 1, idx + 1)
                st.session_state.flashcard_show_back = False
                st.rerun()


def render_quiz(text: str):
    ai = get_ai_results()
    st.markdown("## Quiz")
    if ai:
        st.markdown("*AI-powered quiz questions*")
    else:
        st.markdown("Test your knowledge with auto-generated multiple-choice questions!")

    num_q = st.slider("Number of questions", 3, 15, 8, key="quiz_slider")

    if st.button("Generate Quiz", key="quiz_gen_btn", use_container_width=True):
        with st.spinner("Building AI quiz..." if ai else "Building quiz questions..."):
            if ai and "quiz" in ai:
                questions = ai["quiz"][:num_q]
            else:
                questions = generate_quiz(text, num_q)
            st.session_state.quiz_questions = questions
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False

    if "quiz_questions" in st.session_state and st.session_state.quiz_questions:
        questions = st.session_state.quiz_questions

        if not st.session_state.quiz_submitted:
            for i, q in enumerate(questions):
                st.markdown(f"""
                <div class="mesmery-card">
                    <div style="font-weight:700; margin-bottom:8px;">Q{i+1}. {q['question']}</div>
                </div>
                """, unsafe_allow_html=True)

                selected = st.radio(
                    f"Select answer for Q{i+1}",
                    q["options"],
                    key=f"quiz_q_{i}",
                    label_visibility="collapsed",
                )
                st.session_state.quiz_answers[i] = selected

            if st.button("Submit Quiz", key="quiz_submit", use_container_width=True):
                st.session_state.quiz_submitted = True
                st.rerun()

        else:
            # Show results
            correct = 0
            for i, q in enumerate(questions):
                user_answer = st.session_state.quiz_answers.get(i, "")
                is_correct = user_answer == q["answer"]
                if is_correct:
                    correct += 1

                icon = "CORRECT" if is_correct else "INCORRECT"
                st.markdown(f"""
                <div class="mesmery-card {'quiz-correct' if is_correct else 'quiz-wrong'}">
                    <div style="font-weight:700;">{icon} Q{i+1}. {q['question']}</div>
                    <div style="margin-top:8px;">
                        Your answer: <strong>{user_answer}</strong>
                        {"" if is_correct else f" · Correct: <strong>{q['answer']}</strong>"}
                    </div>
                    <div style="margin-top:6px; font-size:0.9em; opacity:0.8;">
                        {q['explanation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Score
            score_pct = int((correct / len(questions)) * 100)
            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Score", f"{correct}/{len(questions)}")
            with c2:
                st.metric("Percentage", f"{score_pct}%")
            with c3:
                grade = "A+" if score_pct >= 95 else "A" if score_pct >= 90 else "B" if score_pct >= 80 else "C" if score_pct >= 70 else "D" if score_pct >= 60 else "F"
                st.metric("Grade", grade)

            if st.button("Retake Quiz", key="quiz_retake"):
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()


def render_concepts(text: str):
    ai = get_ai_results()
    st.markdown("## Key Concepts")
    if ai:
        st.markdown("*AI-identified key concepts*")
    else:
        st.markdown("The most important concepts extracted from your content, ranked by relevance.")

    if st.button("Extract Concepts", key="concepts_btn", use_container_width=True):
        with st.spinner("AI analyzing concepts..." if ai else "Identifying key concepts..."):
            if ai and "key_concepts" in ai:
                concepts = ai["key_concepts"]
            else:
                concepts = extract_concepts(text)

        for i, concept in enumerate(concepts):
            importance_color = {
                "High": "HIGH", "Medium": "MED", "Notable": "NOTE", "Key Phrase": "KEY"
            }.get(concept.get("importance", "Notable"), "NOTE")
            freq = concept.get("frequency", concept.get("mentions", ""))
            freq_str = f" (mentioned {freq}×)" if freq else ""

            with st.expander(
                f"{importance_color} {concept['name']} — {concept.get('importance', 'Key')}{freq_str}",
                expanded=(i < 3),
            ):
                ctx = concept.get("context", [])
                if isinstance(ctx, list):
                    for c in ctx:
                        st.markdown(f"> {c}")
                elif isinstance(ctx, str):
                    st.markdown(f"> {ctx}")
                if freq:
                    st.markdown(f"**Frequency:** {freq}")
                st.markdown(f"**Importance:** {concept.get('importance', 'Key')}")


def render_study_plan(text: str):
    ai = get_ai_results()
    st.markdown("## Study Plan")
    if ai:
        st.markdown("*AI-generated study schedule*")
    else:
        st.markdown("A personalized study schedule based on your content's structure and complexity.")

    col1, col2 = st.columns(2)
    with col1:
        days = st.slider("Study period (days)", 3, 14, 7, key="plan_days")
    with col2:
        hours = st.slider("Hours per day", 0.5, 4.0, 2.0, 0.5, key="plan_hours")

    if st.button("Generate Study Plan", key="plan_btn", use_container_width=True):
        with st.spinner("Creating AI study plan..." if ai else "Creating your personalized study plan..."):
            if ai and "study_plan" in ai:
                plan = ai["study_plan"]
            else:
                plan = generate_study_plan(text, days, hours)

        for day, details in plan.items():
            if isinstance(details, str):
                continue
            theme = details.get("theme", "Study")
            total_min = details.get("total_minutes", int(hours * 60))

            with st.expander(f"{day} — {theme} ({total_min} min)", expanded=("1" in day or "day 1" in day.lower())):
                activities = details.get("activities", [])
                for activity in activities:
                    if isinstance(activity, str):
                        st.markdown(f"- {activity}")
                        continue
                    st.markdown(f"""
                    <div class="mesmery-card">
                        <div style="font-weight:600;">{activity.get('activity', '')}</div>
                        <div style="font-size:0.9em; margin:6px 0; opacity:0.7;">Topic: {activity.get('topic', '')}</div>
                        <div style="font-size:0.85em; opacity:0.7;">{activity.get('minutes', '')} min</div>
                    </div>
                    """, unsafe_allow_html=True)

                kw_review = details.get("keywords_to_review", [])
                if kw_review:
                    st.markdown("**Keywords to review:**")
                    tags = "".join(f'<span class="tag">{kw.title()}</span>' for kw in kw_review)
                    st.markdown(tags, unsafe_allow_html=True)


def render_mnemonics(text: str):
    ai = get_ai_results()
    st.markdown("## Mnemonics")
    if ai:
        st.markdown("*AI-crafted memory aids*")
    else:
        st.markdown("Memory aids and techniques to help you remember key concepts.")

    if st.button("Generate Mnemonics", key="mnemonic_btn", use_container_width=True):
        with st.spinner("AI creating memory aids..." if ai else "Creating memory aids..."):
            if ai and "mnemonics" in ai:
                mnemonics = ai["mnemonics"]
            else:
                mnemonics = generate_mnemonics(text)

        if mnemonics:
            for m in mnemonics:
                st.markdown(f"""
                <div class="mesmery-card">
                    <div style="font-weight:700; font-size:1.1em;">{m['concept']}</div>
                    <div class="tag" style="margin:8px 0;">{m['type']}</div>
                    <div style="margin-top:8px;">{m['mnemonic']}</div>
                    <div style="font-size:0.85em; opacity:0.7; margin-top:4px;">{m['detail']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Not enough distinct concepts found for mnemonic generation. Try adding more text!")


def render_glossary(text: str):
    ai = get_ai_results()
    st.markdown("## Glossary")
    if ai:
        st.markdown("*AI-generated glossary*")
    else:
        st.markdown("An auto-generated glossary of terms and definitions from your content.")

    if st.button("Build Glossary", key="glossary_btn", use_container_width=True):
        with st.spinner("AI building glossary..." if ai else "Building glossary..."):
            if ai and "glossary" in ai:
                glossary = [{"term": g["term"], "definition": g["definition"], "source": "ai"} for g in ai["glossary"]]
            else:
                glossary = build_glossary(text)

        if glossary:
            st.markdown(f"**{len(glossary)} terms found**")

            search = st.text_input("Filter glossary", key="glossary_search", placeholder="Type to search...")

            filtered = glossary
            if search:
                filtered = [g for g in glossary if search.lower() in g["term"].lower() or search.lower() in g["definition"].lower()]

            for entry in filtered:
                source_badge = "[AI]" if entry.get("source") == "ai" else ("[Defined]" if entry.get("source") == "explicit" else "[Inferred]")
                st.markdown(f"""
                <div class="mesmery-card">
                    <div style="font-weight:700; font-size:1.05em;">{source_badge} {entry['term']}</div>
                    <div style="margin-top:6px;">{entry['definition']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No terms could be extracted. Try adding more detailed text with definitions.")


def render_difficulty(text: str):
    st.markdown("## Difficulty Analyzer")
    st.markdown("Detailed readability and complexity analysis of your study material.")

    if st.button("Analyze Difficulty", key="diff_btn", use_container_width=True):
        with st.spinner("Analyzing text complexity..."):
            result = analyze_difficulty(text)

        # Main score
        score = result["score"]
        level = result["level"]
        color = result["color"]

        st.markdown(f"""
        <div style="text-align:center; padding:20px;">
            <div style="font-size:3em; font-weight:800;">{score}/100</div>
            <div style="font-size:1.5em; font-weight:600;">{level} ({color})</div>
            <div style="margin-top:12px; font-size:1em; opacity:0.8;">{result['tip']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Progress bar for score
        st.markdown(f"""
        <div class="progress-bar-bg" style="height:16px;">
            <div class="progress-bar-fill" style="width:{score}%;"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Detailed stats
        stats = result["stats"]
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Sentences", f"{stats['sentences']:,}")
            st.metric("Avg Sentence Length", f"{stats['avg_sentence_length']} words")
            st.metric("Vocabulary Richness", f"{stats['vocabulary_richness']}%")

        with col2:
            st.metric("Total Words", f"{stats['words']:,}")
            st.metric("Avg Word Length", f"{stats['avg_word_length']} chars")
            st.metric("Technical Density", f"{stats['technical_density']}%")

        st.markdown(f"**Reading Level:** {stats['reading_level']}")

        # Recommendations
        st.markdown("---")
        st.markdown("### Recommendations")
        recommendations = []
        if score > 60:
            recommendations.append("Break content into smaller, focused study sessions")
            recommendations.append("Use flashcards to tackle technical vocabulary")
        if stats["vocabulary_richness"] > 50:
            recommendations.append("Build a glossary of unfamiliar terms")
        if stats["avg_sentence_length"] > 25:
            recommendations.append("Rewrite complex sentences in your own words")
        if stats["technical_density"] > 15:
            recommendations.append("Create mnemonics for technical terms")

        recommendations.append("Use the Study Plan feature to pace your learning")
        recommendations.append("Test yourself with quizzes after each study session")

        for rec in recommendations:
            st.markdown(rec)


def render_outline(text: str):
    ai = get_ai_results()
    st.markdown("## Outline")
    if ai:
        st.markdown("*AI-structured outline*")
    else:
        st.markdown("A structured hierarchical outline showing the organization of your content.")

    if st.button("Generate Outline", key="outline_btn", use_container_width=True):
        with st.spinner("AI analyzing structure..." if ai else "Analyzing content structure..."):
            if ai and "outline" in ai:
                outline = ai["outline"]
            else:
                outline = generate_outline(text)

        if outline:
            for i, section in enumerate(outline, 1):
                st.markdown(f"### {i}. {section['heading']}")

                kws = section.get("keywords", [])
                if kws:
                    tags = "".join(f'<span class="tag">{kw.title()}</span>' for kw in kws)
                    st.markdown(tags, unsafe_allow_html=True)

                for point in section.get("points", []):
                    st.markdown(f"- {point}")

                st.markdown("")
        else:
            st.info("Could not generate a clear outline. Try adding more structured content.")


def render_concept_map(text: str):
    ai = get_ai_results()
    st.markdown("## Concept Map")
    if ai:
        st.markdown("*AI-mapped concept relationships*")
    else:
        st.markdown("Visual representation of how key concepts in your content are connected.")

    if st.button("Generate Concept Map", key="cmap_btn", use_container_width=True):
        with st.spinner("AI mapping concepts..." if ai else "Mapping concept relationships..."):
            if ai and "concept_map" in ai:
                cmap = ai["concept_map"]
            else:
                cmap = generate_concept_map(text)

        nodes = cmap.get("nodes", [])
        edges = cmap.get("edges", [])
        # Normalize edge types for consistent comparison
        normalized = []
        for e in edges:
            if isinstance(e, (list, tuple)) and len(e) >= 2:
                try:
                    normalized.append((int(e[0]), int(e[1])))
                except (ValueError, TypeError):
                    pass
        edges = normalized

        if nodes:
            st.markdown("### Concept Network")
            st.markdown("*Lines connect concepts that appear in the same sentences*")

            # Visual representation
            for node in sorted(nodes, key=lambda x: x["connections"], reverse=True):
                connected = []
                for e in edges:
                    if e[0] == node["id"]:
                        target = next((n for n in nodes if n["id"] == e[1]), None)
                        if target:
                            connected.append(target["label"])
                    elif e[1] == node["id"]:
                        target = next((n for n in nodes if n["id"] == e[0]), None)
                        if target:
                            connected.append(target["label"])

                conn_text = ", ".join(connected) if connected else "No direct connections"

                max_size = max((n.get("size", n.get("connections", 1)) or 1) for n in nodes)
                node_size = node.get("size", node.get("connections", 1)) or 1
                bar_width = min(100, (node_size / max_size) * 100)

                st.markdown(f"""
                <div class="mesmery-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="font-weight:700; font-size:1.1em;">{node['label']}</div>
                        <div class="tag">{node.get('size', node.get('connections', ''))} mentions</div>
                    </div>
                    <div class="progress-bar-bg" style="margin:8px 0;">
                        <div class="progress-bar-fill" style="width:{bar_width}%;"></div>
                    </div>
                    <div style="font-size:0.9em; opacity:0.7;">
                        Connected to: {conn_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Not enough interconnected concepts found. Try adding more content.")


def render_practice(text: str):
    ai = get_ai_results()
    st.markdown("## Practice Questions")
    if ai:
        st.markdown("*AI-generated practice questions*")
    else:
        st.markdown("Open-ended questions designed to deepen your understanding at various levels of Bloom's Taxonomy.")

    num_q = st.slider("Number of questions", 3, 12, 6, key="pq_slider")

    if st.button("Generate Questions", key="pq_btn", use_container_width=True):
        with st.spinner("AI creating practice questions..." if ai else "Creating practice questions..."):
            if ai and "practice_questions" in ai:
                questions = ai["practice_questions"][:num_q]
            else:
                questions = generate_practice_questions(text, num_q)

        bloom_colors = {
            "comprehension": "Remember",
            "application": "Apply",
            "analysis": "Analyze",
            "comparison": "Analyze",
            "synthesis": "Evaluate",
            "evaluation": "Evaluate",
            "critical": "Create",
        }

        for i, q in enumerate(questions, 1):
            bloom = q.get("bloom_level", "analysis")
            color = bloom_colors.get(bloom, "Think")

            with st.expander(f"{color} Q{i}. {q['question']}", expanded=False):
                st.markdown(f"**Bloom's Level:** {bloom.title()}")
                st.markdown("**Hints:**")
                for hint in q.get("hints", []):
                    st.markdown(f"- {hint}")
                st.markdown("---")
                st.markdown("*Write your answer below, then check your understanding by reviewing the relevant sections.*")
                st.text_area("Your answer", key=f"pq_answer_{i}", height=100, label_visibility="collapsed")


def render_study_tips_page(text: str):
    ai = get_ai_results()
    st.markdown("## Study Tips")
    if ai:
        st.markdown("*AI-personalized study strategies*")
    else:
        st.markdown("Personalized study strategies based on your content's difficulty and structure.")

    if st.button("Get Study Tips", key="tips_btn", use_container_width=True):
        with st.spinner("AI generating personalized tips..." if ai else "Analyzing your content for personalized tips..."):
            if ai and "study_tips" in ai:
                tips = ai["study_tips"]
            else:
                difficulty = analyze_difficulty(text)
                tips = generate_study_tips(text, difficulty)

        for tip in tips:
            st.markdown(f"""
            <div class="study-tip">
                <div style="font-size:0.7em; font-weight:600; letter-spacing:0.1em; opacity:0.4; margin-bottom:6px;">{tip.get('icon', '')}</div>
                <div style="font-weight:700; font-size:1.1em; margin-bottom:4px;">{tip['title']}</div>
                <div style="margin-bottom:6px;">{tip['tip']}</div>
                <span class="tag">Technique: {tip['technique']}</span>
            </div>
            """, unsafe_allow_html=True)


# ─── Run ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
