PREMIUM_CSS = """
<style>
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }

.main .block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

[data-testid="stSidebar"] {
    background: #0d0d14 !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    transition: border-color 0.25s, transform 0.2s;
}
[data-testid="metric-container"]:hover {
    border-color: rgba(124,92,252,0.45);
    transform: translateY(-2px);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(255,255,255,0.02);
    padding: 5px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 22px;
    font-weight: 500;
    font-size: 0.88rem;
    letter-spacing: 0.2px;
}
.stTabs [aria-selected="true"] {
    background: rgba(124,92,252,0.18) !important;
    border: 1px solid rgba(124,92,252,0.4) !important;
    color: #c4b0ff !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7C5CFC, #5C3FD4) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #8D70FF, #6D50E5) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(124,92,252,0.35) !important;
}

hr { border-color: rgba(255,255,255,0.06) !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(124,92,252,0.4); }

.stTextInput input, .stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(124,92,252,0.55) !important;
    box-shadow: 0 0 0 2px rgba(124,92,252,0.15) !important;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
}

.stAlert { border-radius: 10px !important; }

div[data-testid="stDownloadButton"] > button {
    border-radius: 8px !important;
    font-weight: 500 !important;
}

.vektor-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.8rem 2rem;
}
.vektor-badge {
    display: inline-block;
    background: rgba(124,92,252,0.15);
    border: 1px solid rgba(124,92,252,0.3);
    color: #c4b0ff;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.forecast-note {
    background: rgba(124,92,252,0.08);
    border-left: 3px solid rgba(124,92,252,0.5);
    border-radius: 0 8px 8px 0;
    padding: 0.7rem 1rem;
    font-size: 0.85rem;
    color: #aaa;
    margin-bottom: 1.2rem;
}
</style>
"""
