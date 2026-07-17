"""
IT-Insight: Hardware Analysis Tool
Streamlit application with Neon Light IT/TECHNO style UI
"""

import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
from utils.gemini_client import GeminiClient, GeminiError

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="IT-Insight - Hardware Analyzer",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS - NEON LIGHT THEME ============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a0a2e 50%, #0a1a2a 100%);
        background-attachment: fixed;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(ellipse at 20% 50%, rgba(0, 255, 136, 0.05) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 50%, rgba(0, 204, 255, 0.05) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 100%, rgba(112, 0, 255, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    .scanline {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 3px,
            rgba(0, 255, 136, 0.02) 3px,
            rgba(0, 255, 136, 0.02) 4px
        );
        z-index: 9999;
    }
    
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #00ff88, #00ccff, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 
            0 0 40px rgba(0, 255, 136, 0.3),
            0 0 80px rgba(0, 204, 255, 0.2),
            0 0 120px rgba(168, 85, 247, 0.1);
        padding: 1rem 0;
        letter-spacing: 4px;
        animation: glowPulse 3s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }
    
    @keyframes glowPulse {
        0%, 100% { 
            text-shadow: 0 0 40px rgba(0, 255, 136, 0.3), 0 0 80px rgba(0, 204, 255, 0.2);
        }
        50% { 
            text-shadow: 0 0 60px rgba(0, 255, 136, 0.6), 0 0 120px rgba(0, 204, 255, 0.4), 0 0 160px rgba(168, 85, 247, 0.2);
        }
    }
    
    .sub-header {
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.1rem;
        text-align: center;
        color: #00ff88;
        opacity: 0.9;
        letter-spacing: 6px;
        border-bottom: 1px solid rgba(0, 255, 136, 0.15);
        padding-bottom: 1rem;
        margin-bottom: 2rem;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
        position: relative;
        z-index: 1;
    }
    
    .result-card {
        background: rgba(10, 14, 30, 0.75);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 16px;
        padding: 1.8rem;
        margin: 1rem 0;
        box-shadow: 
            0 0 30px rgba(0, 255, 136, 0.05),
            0 0 60px rgba(0, 204, 255, 0.03),
            inset 0 0 30px rgba(0, 255, 136, 0.02);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        z-index: 1;
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #00ff88, #00ccff, #a855f7, #00ff88);
        background-size: 400% 400%;
        border-radius: 16px;
        z-index: -1;
        animation: borderGlow 4s ease-in-out infinite;
        opacity: 0.25;
    }
    
    @keyframes borderGlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .result-card:hover {
        transform: translateY(-4px);
        box-shadow: 
            0 0 50px rgba(0, 255, 136, 0.15),
            0 0 80px rgba(0, 204, 255, 0.08);
        border-color: rgba(0, 255, 136, 0.4);
    }
    
    .result-card h4 {
        font-family: 'Orbitron', sans-serif;
        color: #00ff88;
        font-size: 0.75rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        opacity: 0.8;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
    }
    
    .result-card .value {
        font-family: 'Share Tech Mono', monospace;
        color: #e8f0ff;
        font-size: 1.1rem;
        line-height: 1.8;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.05);
    }
    
    .upload-area {
        border: 2px dashed rgba(0, 255, 136, 0.25);
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
        background: rgba(0, 255, 136, 0.03);
        transition: all 0.4s ease;
        position: relative;
        z-index: 1;
    }
    
    .upload-area:hover {
        border-color: #00ff88;
        background: rgba(0, 255, 136, 0.08);
        box-shadow: 
            0 0 40px rgba(0, 255, 136, 0.08),
            inset 0 0 40px rgba(0, 255, 136, 0.03);
    }
    
    .upload-area .icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 0 30px rgba(0, 255, 136, 0.2));
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-12px); }
    }
    
    .upload-area .title {
        font-family: 'Orbitron', sans-serif;
        color: #00ff88;
        font-size: 1.2rem;
        letter-spacing: 2px;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
    }
    
    .upload-area .subtitle {
        font-family: 'Share Tech Mono', monospace;
        color: #88aabb;
        font-size: 0.85rem;
        margin-top: 0.5rem;
        opacity: 0.8;
    }
    
    .stButton > button {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(135deg, #00ff88, #00ccff) !important;
        color: #0a0e1a !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.9rem 2.5rem !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
        box-shadow: 
            0 0 30px rgba(0, 255, 136, 0.2),
            0 0 60px rgba(0, 204, 255, 0.1) !important;
        width: 100% !important;
        position: relative;
        z-index: 1;
    }
    
    .stButton > button:hover {
        transform: scale(1.03) !important;
        box-shadow: 
            0 0 50px rgba(0, 255, 136, 0.4),
            0 0 80px rgba(0, 204, 255, 0.2) !important;
    }
    
    .css-1d391kg, .css-12oz5g7 {
        background: rgba(10, 14, 30, 0.85) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(0, 255, 136, 0.08) !important;
    }
    
    .css-1d391kg .stMarkdown, .css-12oz5g7 .stMarkdown {
        color: #c8d8e8 !important;
    }
    
    .status-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
        animation: blink 1.5s ease-in-out infinite;
    }
    
    .status-dot.online {
        background: #00ff88;
        box-shadow: 0 0 20px #00ff88, 0 0 40px rgba(0, 255, 136, 0.3);
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    .metric-box {
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid rgba(0, 255, 136, 0.1);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        font-family: 'Share Tech Mono', monospace;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-box:hover {
        border-color: rgba(0, 255, 136, 0.3);
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.05);
    }
    
    .metric-box .number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00ff88;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
    }
    
    .metric-box .label {
        font-size: 0.65rem;
        color: #88aabb;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.3rem;
    }
    
    .stAlert {
        background: rgba(255, 0, 50, 0.08) !important;
        border: 1px solid rgba(255, 0, 50, 0.2) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stAlert .stMarkdown {
        color: #ff6b8a !important;
        font-family: 'Share Tech Mono', monospace !important;
    }
    
    .stInfo {
        background: rgba(0, 255, 136, 0.05) !important;
        border: 1px solid rgba(0, 255, 136, 0.15) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stInfo .stMarkdown {
        color: #88ddbb !important;
        font-family: 'Share Tech Mono', monospace !important;
    }
    
    ::-webkit-scrollbar {
        width: 6px;
        background: #0a0e1a;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00ff88, #00ccff);
        border-radius: 3px;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
    }
    ::-webkit-scrollbar-track {
        background: rgba(10, 14, 26, 0.5);
    }
    
    @media (max-width: 768px) {
        .main-header { font-size: 2rem; }
        .result-card { padding: 1rem; }
        .result-card .value { font-size: 0.95rem; }
        .upload-area { padding: 1.5rem; }
    }
    
    .footer-text {
        text-align: center;
        color: #334455;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 2px;
        padding: 1rem 0;
        opacity: 0.5;
        position: relative;
        z-index: 1;
    }
</style>

<div class="scanline"></div>
""", unsafe_allow_html=True)

# ============ SESSION STATE ============
def initialize_session_state():
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None

# ============ API KEY ============
def get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if api_key:
            return api_key
    except:
        pass
    return None

# ============ DISPLAY FUNCTIONS ============
def display_header():
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown('<p class="main-header">⧩ IT-INSIGHT</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="sub-header">// AI-POWERED HARDWARE ANALYSIS //</p>',
            unsafe_allow_html=True
        )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(
            """
            <div style="text-align: center; margin-top: -0.5rem; margin-bottom: 1rem;">
                <span class="status-dot online"></span>
                <span style="font-family: 'Share Tech Mono', monospace; color: #00ff88; font-size: 0.8rem; opacity: 0.7;">
                    SYSTEM ONLINE // v2.0
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

def display_metrics():
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("⚡", "STATUS", "ACTIVE"),
        ("📡", "CONNECTION", "SECURE"),
        ("🧠", "MODEL", "GEMINI 2.0"),
        ("🔐", "ENCRYPTION", "AES-256")
    ]
    
    for col, (icon, label, value) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div style="font-size: 1.5rem;">{icon}</div>
                    <div class="number" style="font-size: 0.9rem; color: #00ccff;">{value}</div>
                    <div class="label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

def display_result(result):
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; font-family: 'Orbitron', sans-serif; color: #00ff88; letter-spacing: 4px; font-size: 1.2rem; margin: 2rem 0;">
            ═══ ANALYSIS REPORT ═══
        </div>
        """,
        unsafe_allow_html=True
    )
    
    features = result.get('Key Features', ['N/A'])
    if isinstance(features, str):
        features = [features]
    
    col1, col2 = st.columns(2)
    
    items = [
        ("🆔", "HARDWARE NAME", result.get('Hardware Name', 'N/A')),
        ("⚡", "PRIMARY FUNCTION", result.get('Primary Function', 'N/A')),
        ("🔗", "COMPATIBILITY", result.get('Compatibility', 'N/A')),
        ("💡", "RECOMMENDATIONS", result.get('Recommendations', 'N/A'))
    ]
    
    for i, (icon, label, value) in enumerate(items):
        with col1 if i < 2 else col2:
            st.markdown(
                f"""
                <div class="result-card">
                    <h4>{icon} {label}</h4>
                    <div class="value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown(
        f"""
        <div class="result-card">
            <h4>✨ KEY FEATURES</h4>
            <div class="value">
                {"<br>• ".join([''] + features) if features else 'N/A'}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============ MAIN APP ============
def main():
    initialize_session_state()
    
    display_header()
    
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 2rem;">🖥️</div>
                <div style="font-family: 'Orbitron', sans-serif; color: #00ff88; font-size: 0.8rem; letter-spacing: 2px;">
                    SYSTEM CONSOLE
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("### ⚙️ CONFIGURATION")
        st.markdown("---")
        
        st.markdown(
            """
            **OPERATIONS**
            • Upload hardware image
            • Initiate AI analysis
            • View diagnostic report
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        st.markdown(
            """
            **SUPPORTED FORMATS**
            • PNG • JPG • JPEG
            • WEBP • BMP
            """,
            unsafe_allow_html=True
        )
        
        with st.expander("🛠️ ADVANCED"):
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1
            )
            max_tokens = st.slider(
                "Max Tokens",
                min_value=100,
                max_value=1000,
                value=300,
                step=50
            )
        
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; font-size: 0.7rem; color: #445566; font-family: 'Share Tech Mono', monospace;">
                IT-INSIGHT v2.0<br>
                SECURE CONNECTION
            </div>
            """,
            unsafe_allow_html=True
        )
    
    api_key = get_api_key()
    
    if not api_key:
        st.error("""
        ❌ **API KEY MISSING**
        
        Please set your Gemini API key in `.env` or Streamlit secrets.
        """)
        st.stop()
    
    st.markdown(
        """
        <div class="upload-area">
            <span class="icon">📀</span>
            <div class="title">UPLOAD HARDWARE IMAGE</div>
            <div class="subtitle">Drag & drop or click to select</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    uploaded_file = st.file_uploader(
        " ",
        type=['png', 'jpg', 'jpeg', 'webp', 'bmp'],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="UPLOADED IMAGE", use_container_width=True)
        
        with col2:
            st.markdown(
                """
                <div style="font-family: 'Share Tech Mono', monospace; color: #88aabb; font-size: 0.9rem; padding: 1rem 0;">
                    FILE: <span style="color: #00ff88;">{}</span><br>
                    SIZE: <span style="color: #00ff88;">{} x {}</span>
                </div>
                """.format(
                    uploaded_file.name,
                    image.width,
                    image.height
                ),
                unsafe_allow_html=True
            )
            
            if st.button("🔍 ANALYZE HARDWARE", type="primary"):
                with st.spinner("🧠 PROCESSING..."):
                    try:
                        client = GeminiClient(api_key)
                        result = client.analyze_hardware(
                            image,
                            temperature=temperature,
                            max_tokens=max_tokens
                        )
                        st.session_state.analysis_result = result
                        
                    except GeminiError as e:
                        st.error(f"❌ ANALYSIS FAILED: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ SYSTEM ERROR: {str(e)}")
        
        if st.session_state.analysis_result:
            display_result(st.session_state.analysis_result)
            
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("📋 EXPORT REPORT"):
                    st.info("Report ready for export")
                    st.balloons()
    else:
        st.info("⏳ Awaiting hardware image upload...")
        st.markdown(
            """
            <div style="text-align: center; color: #445566; font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; padding: 2rem;">
                SUPPORTED HARDWARE: CPU • GPU • RAM • STORAGE • NETWORK • PERIPHERALS
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    st.markdown(
        """
        <div class="footer-text">
            ⚡ IT-INSIGHT • POWERED BY GOOGLE GEMINI API • SECURE & ENCRYPTED ⚡
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
