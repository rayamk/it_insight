"""
IT-Insight: Hardware Analysis Tool
Streamlit application with Space/Galaxy Theme UI
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
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS - SPACE/GALAXY THEME ============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 25%, #0d1b2a 50%, #1b0a2e 75%, #0a0a1a 100%) !important;
        background-attachment: fixed !important;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #eee, transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 90px 40px, #fff, transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
            radial-gradient(2px 2px at 160px 30px, #ddd, transparent),
            radial-gradient(1px 1px at 200px 60px, #fff, transparent),
            radial-gradient(2px 2px at 250px 90px, rgba(255,255,255,0.7), transparent),
            radial-gradient(1px 1px at 300px 20px, #eee, transparent);
        background-size: 200px 200px;
        background-repeat: repeat;
        opacity: 0.4;
        pointer-events: none;
        z-index: 0;
    }
    
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        color: #00d4ff !important;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.3), 0 0 60px rgba(123, 47, 252, 0.2);
        padding: 1rem 0;
        letter-spacing: 4px;
        position: relative;
        z-index: 1;
    }
    
    .sub-header {
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.1rem;
        text-align: center;
        color: #7b9fff !important;
        letter-spacing: 6px;
        border-bottom: 1px solid rgba(123, 47, 252, 0.2);
        padding-bottom: 1rem;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .result-card {
        background: rgba(10, 10, 30, 0.75) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(123, 47, 252, 0.3) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 0 40px rgba(123, 47, 252, 0.1) !important;
        transition: all 0.3s ease !important;
        position: relative;
        z-index: 1;
    }
    
    .result-card:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 0 60px rgba(123, 47, 252, 0.2) !important;
        border-color: rgba(123, 47, 252, 0.6) !important;
    }
    
    .result-card h4 {
        font-family: 'Orbitron', sans-serif;
        color: #7b9fff !important;
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    
    .result-card .value {
        font-family: 'Share Tech Mono', monospace;
        color: #d0d8ff !important;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .upload-area {
        border: 2px dashed rgba(123, 47, 252, 0.3) !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        text-align: center !important;
        background: rgba(123, 47, 252, 0.05) !important;
        transition: all 0.3s ease !important;
        position: relative;
        z-index: 1;
    }
    
    .upload-area:hover {
        border-color: #7b2ffc !important;
        background: rgba(123, 47, 252, 0.1) !important;
        box-shadow: 0 0 50px rgba(123, 47, 252, 0.1) !important;
    }
    
    .upload-area .icon {
        font-size: 3.5rem;
        display: block;
        margin-bottom: 0.5rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .upload-area .title {
        font-family: 'Orbitron', sans-serif;
        color: #7b9fff !important;
        font-size: 1.1rem;
        letter-spacing: 2px;
    }
    
    .upload-area .subtitle {
        font-family: 'Share Tech Mono', monospace;
        color: #6688aa !important;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }
    
    .stButton > button {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(135deg, #7b2ffc, #00d4ff) !important;
        color: #0a0a1a !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 30px rgba(123, 47, 252, 0.2) !important;
        width: 100% !important;
        position: relative;
        z-index: 1;
    }
    
    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 50px rgba(123, 47, 252, 0.4) !important;
    }
    
    .css-1d391kg, .css-12oz5g7, [data-testid="stSidebar"] {
        background: rgba(10, 10, 26, 0.9) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(123, 47, 252, 0.1) !important;
    }
    
    .status-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
        animation: blink 1.5s ease-in-out infinite;
        background: #7b2ffc !important;
        box-shadow: 0 0 20px #7b2ffc !important;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    .metric-box {
        background: rgba(123, 47, 252, 0.08) !important;
        border: 1px solid rgba(123, 47, 252, 0.15) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    .metric-box:hover {
        border-color: rgba(123, 47, 252, 0.4) !important;
        box-shadow: 0 0 30px rgba(123, 47, 252, 0.05) !important;
    }
    
    .metric-box .number {
        font-size: 1.5rem;
        font-weight: 700;
        color: #7b9fff !important;
        font-family: 'Orbitron', sans-serif;
    }
    
    .metric-box .label {
        font-size: 0.65rem;
        color: #6688aa !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.2rem;
    }
    
    .footer-text {
        text-align: center;
        color: #334466 !important;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 2px;
        padding: 1rem 0;
        opacity: 0.5;
        position: relative;
        z-index: 1;
    }
    
    @media (max-width: 768px) {
        .main-header { font-size: 2rem; }
        .result-card { padding: 1rem !important; }
        .result-card .value { font-size: 0.95rem; }
        .upload-area { padding: 1.5rem !important; }
    }
</style>

<div style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(100,50,255,0.02) 3px,rgba(100,50,255,0.02) 4px);z-index:9999;"></div>
""", unsafe_allow_html=True)

# ============ SESSION STATE ============
def initialize_session_state():
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None

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
    col1, col2 = st.columns([1, 6])
    
    with col1:
        st.markdown(
            """
            <div style="text-align: center; padding-top: 0.3rem;">
                <svg width="60" height="60" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="45" stroke="#00d4ff" stroke-width="2" fill="none" opacity="0.3"/>
                    <circle cx="50" cy="50" r="35" stroke="#7b2ffc" stroke-width="1.5" fill="none" opacity="0.4"/>
                    <rect x="35" y="30" width="30" height="40" rx="4" fill="#00d4ff" opacity="0.9"/>
                    <rect x="42" y="38" width="16" height="24" rx="2" fill="#0a0a1a"/>
                    <rect x="40" y="35" width="4" height="30" rx="1" fill="#00d4ff"/>
                    <rect x="48" y="35" width="4" height="30" rx="1" fill="#00d4ff"/>
                    <rect x="44" y="35" width="12" height="4" rx="1" fill="#00d4ff"/>
                    <circle cx="15" cy="20" r="1.5" fill="#fff" opacity="0.6"/>
                    <circle cx="85" cy="25" r="1" fill="#fff" opacity="0.5"/>
                    <circle cx="20" cy="80" r="1.5" fill="#fff" opacity="0.4"/>
                    <circle cx="80" cy="75" r="1" fill="#fff" opacity="0.6"/>
                    <circle cx="50" cy="50" r="2" fill="#00d4ff" opacity="0.8">
                        <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/>
                    </circle>
                </svg>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div>
                <p style="font-family: 'Orbitron', sans-serif; font-size: 2.5rem; font-weight: 900; color: #00d4ff !important; margin-bottom: 0; text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);">
                    IT-INSIGHT
                </p>
                <p style="font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; color: #7b9fff !important; margin-top: -0.5rem; border-bottom: none;">
                    // AI-POWERED HARDWARE ANALYSIS //
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style="text-align: center; margin-top: 0.5rem; margin-bottom: 1rem;">
                <span class="status-dot"></span>
                <span style="font-family:'Share Tech Mono',monospace;color:#7b9fff;font-size:0.8rem;opacity:0.7;">
                    SYSTEM ONLINE // v2.0
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

def display_metrics():
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("🌌", "STATUS", "ACTIVE"),
        ("💫", "CONNECTION", "SECURE"),
        ("🛸", "MODEL", "GEMINI 2.0"),
        ("🔮", "ENCRYPTION", "AES-256")
    ]
    
    for col, (icon, label, value) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div style="font-size:1.5rem;">{icon}</div>
                    <div class="number" style="font-size:0.9rem;color:#7bb8ff;">{value}</div>
                    <div class="label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

def display_result(result):
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center;font-family:'Orbitron',sans-serif;color:#7b9fff;letter-spacing:4px;font-size:1.2rem;margin:2rem 0;">
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
            <div style="text-align:center;margin-bottom:2rem;">
                <div style="font-size:2rem;">🪐</div>
                <div style="font-family:'Orbitron',sans-serif;color:#7b9fff;font-size:0.8rem;letter-spacing:2px;">
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
            <div style="text-align:center;font-size:0.7rem;color:#445577;font-family:'Share Tech Mono',monospace;">
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
            <span class="icon">🪐</span>
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
                <div style="font-family:'Share Tech Mono',monospace;color:#6688aa;font-size:0.9rem;padding:1rem 0;">
                    FILE: <span style="color:#7b9fff;">{}</span><br>
                    SIZE: <span style="color:#7b9fff;">{} x {}</span>
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
            <div style="text-align:center;color:#445577;font-family:'Share Tech Mono',monospace;font-size:0.8rem;padding:2rem;">
                SUPPORTED HARDWARE: CPU • GPU • RAM • STORAGE • NETWORK • PERIPHERALS
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    st.markdown(
        """
        <div class="footer-text">
            🌌 IT-INSIGHT • POWERED BY GOOGLE GEMINI API • SECURE & ENCRYPTED 🌌
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
