import streamlit as st

def inject_css():
    css = """<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;600&display=swap');

:root {
    --bg-primary: #050810;
    --bg-secondary: #0a0f1e;
    --bg-card: #0d1526;
    --bg-card-hover: #121d35;
    --accent-green: #00ff88;
    --accent-red: #ff2d55;
    --accent-orange: #ff9500;
    --accent-blue: #0a84ff;
    --accent-cyan: #00d4ff;
    --text-primary: #e8eaf6;
    --text-secondary: #8892b0;
    --text-mono: #64ffda;
    --border-subtle: rgba(0, 255, 136, 0.12);
    --border-active: rgba(0, 255, 136, 0.4);
    --glow-green: 0 0 20px rgba(0, 255, 136, 0.3);
    --glow-red: 0 0 20px rgba(255, 45, 85, 0.4);
    --glow-blue: 0 0 15px rgba(10, 132, 255, 0.3);
}

.stApp {
    background: var(--bg-primary) !important;
    background-image: 
        radial-gradient(ellipse at 20% 20%, rgba(0, 255, 136, 0.03) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(10, 132, 255, 0.04) 0%, transparent 50%),
        linear-gradient(180deg, #050810 0%, #07091a 100%) !important;
    font-family: 'Exo 2', sans-serif !important;
    color: var(--text-primary) !important;
}

/* Animated scan-line overlay */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 255, 136, 0.008) 2px,
        rgba(0, 255, 136, 0.008) 4px
    );
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
.block-container {
    padding-top: 2rem !important;
    max-width: 860px !important;
}

[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-secondary) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.82rem !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--accent-cyan) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

h1 {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 2.8rem !important;
    letter-spacing: 4px !important;
    text-transform: uppercase !important;
    color: var(--text-primary) !important;
    text-shadow: 0 0 30px rgba(0, 212, 255, 0.4) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    padding-bottom: 0.5rem !important;
}
h2 {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    color: var(--accent-cyan) !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    font-size: 1.4rem !important;
}
h3 {
    font-family: 'Share Tech Mono', monospace !important;
    color: var(--text-mono) !important;
    font-size: 1rem !important;
    letter-spacing: 1px !important;
}
p, li, span, label {
    font-family: 'Exo 2', sans-serif !important;
    color: var(--text-secondary) !important;
}

.stButton > button {
    background: transparent !important;
    border: 1px solid var(--accent-green) !important;
    color: var(--accent-green) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding: 0.7rem 2rem !important;
    border-radius: 2px !important;
    transition: all 0.2s ease !important;
    box-shadow: inset 0 0 0 0 var(--accent-green) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    background: rgba(0, 255, 136, 0.08) !important;
    box-shadow: var(--glow-green) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"] {
    border-color: var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
    box-shadow: var(--glow-blue) !important;
}

[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border-active) !important;
    border-radius: 4px !important;
    padding: 1.5rem !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-cyan) !important;
    box-shadow: var(--glow-blue) !important;
}
[data-testid="stFileUploader"] * {
    color: var(--text-secondary) !important;
    font-family: 'Share Tech Mono', monospace !important;
}

[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 4px !important;
    padding: 1rem !important;
    position: relative !important;
    overflow: hidden !important;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-green), var(--accent-cyan));
}
[data-testid="stMetricLabel"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--accent-green) !important;
    text-shadow: var(--glow-green) !important;
}

[data-testid="stAlert"] {
    border-radius: 2px !important;
    border-left-width: 3px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    font-size: 1rem !important;
}
/* Success = green glow */
[data-testid="stAlert"][data-baseweb="notification"]:has(.success),
div[data-testid="stAlert"].st-success,
.element-container div[class*="success"] {
    background: rgba(0, 255, 136, 0.06) !important;
    border-left-color: var(--accent-green) !important;
    box-shadow: var(--glow-green) !important;
}
/* Error = red glow */
div[class*="error"], [class*="stAlert"][class*="error"] {
    background: rgba(255, 45, 85, 0.08) !important;
    border-left-color: var(--accent-red) !important;
    box-shadow: var(--glow-red) !important;
}

[data-testid="stProgress"] > div {
    background: rgba(0, 255, 136, 0.1) !important;
    border-radius: 0 !important;
    height: 6px !important;
}
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--accent-green), var(--accent-cyan)) !important;
    border-radius: 0 !important;
    box-shadow: var(--glow-green) !important;
}

[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 2px !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stExpander"]:hover {
    border-color: var(--border-active) !important;
}
[data-testid="stExpander"] summary {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--accent-cyan) !important;
    font-size: 0.85rem !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border-subtle) !important;
    border-radius: 2px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
}

[data-testid="stRadio"] label {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
}
[data-testid="stRadio"] [data-checked="true"] + label {
    color: var(--accent-green) !important;
}

hr {
    border-color: var(--border-subtle) !important;
    margin: 1.5rem 0 !important;
}

[data-testid="stSpinner"] * {
    color: var(--accent-cyan) !important;
    font-family: 'Share Tech Mono', monospace !important;
}

[data-testid="stImage"] {
    border: 1px solid var(--border-subtle) !important;
    border-radius: 4px !important;
    overflow: hidden !important;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.5) !important;
}

/* Verdict card — FAKE */
.verdict-fake {
    background: linear-gradient(135deg, rgba(255,45,85,0.12), rgba(255,45,85,0.04));
    border: 1px solid rgba(255,45,85,0.5);
    border-left: 4px solid var(--accent-red);
    border-radius: 4px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
    box-shadow: var(--glow-red), inset 0 0 40px rgba(255,45,85,0.03);
}
.verdict-fake .verdict-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent-red);
    letter-spacing: 4px;
    text-transform: uppercase;
    text-shadow: var(--glow-red);
    margin: 0;
}
.verdict-fake .verdict-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: rgba(255,45,85,0.7);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* Verdict card — REAL */
.verdict-real {
    background: linear-gradient(135deg, rgba(0,255,136,0.08), rgba(0,255,136,0.02));
    border: 1px solid rgba(0,255,136,0.4);
    border-left: 4px solid var(--accent-green);
    border-radius: 4px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
    box-shadow: var(--glow-green), inset 0 0 40px rgba(0,255,136,0.02);
}
.verdict-real .verdict-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent-green);
    letter-spacing: 4px;
    text-transform: uppercase;
    text-shadow: var(--glow-green);
    margin: 0;
}
.verdict-real .verdict-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: rgba(0,255,136,0.6);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* Section header with line */
.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--accent-cyan);
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1.5rem 0 1rem 0;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-active), transparent);
}

/* Model result row */
.model-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 1.2rem;
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 2px;
    margin-bottom: 0.4rem;
    transition: border-color 0.2s;
}
.model-row:hover { border-color: var(--border-active); }
.model-name {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-secondary);
    letter-spacing: 1px;
}
.model-badge-fake {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    color: var(--accent-red);
    letter-spacing: 2px;
    padding: 0.2rem 0.8rem;
    border: 1px solid rgba(255,45,85,0.4);
    border-radius: 2px;
    background: rgba(255,45,85,0.08);
}
.model-badge-real {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    color: var(--accent-green);
    letter-spacing: 2px;
    padding: 0.2rem 0.8rem;
    border: 1px solid rgba(0,255,136,0.3);
    border-radius: 2px;
    background: rgba(0,255,136,0.06);
}
.model-conf {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text-mono);
    min-width: 60px;
    text-align: right;
}

/* Scan animation for header */
@keyframes scan {
    0% { transform: translateY(-100%); opacity: 0.6; }
    100% { transform: translateY(100vh); opacity: 0; }
}
.scan-line {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
    animation: scan 4s linear infinite;
    pointer-events: none;
    z-index: 9999;
}

/* FFT meter bar */
.fft-bar-wrap {
    background: rgba(0,255,136,0.06);
    border: 1px solid var(--border-subtle);
    border-radius: 2px;
    height: 8px;
    overflow: hidden;
    margin: 0.5rem 0;
}
.fft-bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 1s ease;
    box-shadow: var(--glow-green);
}

/* Step cards (bottom section) */
.step-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-top: 2px solid var(--accent-cyan);
    border-radius: 2px;
    padding: 1.2rem;
    height: 100%;
    transition: all 0.2s;
}
.step-card:hover {
    border-color: var(--accent-green);
    box-shadow: var(--glow-green);
    transform: translateY(-2px);
}
.step-number {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--border-active);
    line-height: 1;
    margin-bottom: 0.5rem;
}
.step-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: var(--accent-cyan);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.step-desc {
    font-family: 'Exo 2', sans-serif;
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

/* Caption / footer */
.stCaption, caption, small {
    font-family: 'Share Tech Mono', monospace !important;
    color: rgba(136, 146, 176, 0.5) !important;
    font-size: 0.7rem !important;
    letter-spacing: 1px !important;
}
</style>"""
    st.markdown(css, unsafe_allow_html=True)
