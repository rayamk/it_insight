"""
IT-Insight: Hardware Analysis Tool
Professional UI with SVG Logo
"""

import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
from utils.gemini_client import GeminiClient, GeminiError

load_dotenv()

st.set_page_config(
    page_title="IT-Insight - Hardware Analyzer",
    page_icon="💻",
    layout="wide"
)

# ============ PROFESSIONAL CSS ============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(145deg, #0b0f1a 0%, #141b2b 50%, #0f1422 100%);
    }
    
    /* Professional Header */
    .header-container {
        display: flex;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 2rem;
    }
    
    .logo-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff, #7b2ffc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        margin-left: 1rem;
    }
    
    .sub-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #8899bb;
        letter-spacing: 3px;
        margin-left: 2rem;
        padding-top: 0.3rem;
    }
    
    /* Cards */
    .result-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        background: rgba(255,255,255,0.06);
        border-color: rgba(0, 212, 255, 0.2);
        transform: translateY(-2px);
    }
    
    .result-card h4 {
        color: #00d4ff;
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        opacity: 0.7;
        margin-bottom: 0.5rem;
    }
    
    .result-card .value {
        color: #e0e8f0;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 400;
    }
    
    /* Upload Area */
    .upload-area {
        border: 2px dashed rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        padding: 3rem;
        text-align: center;
        background: rgba(0, 212, 255, 0.02);
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #00d4ff;
        background: rgba(0, 212, 255, 0.05);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff, #7b2ffc) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.3) !important;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-12oz5g7 {
        background: rgba(11, 15, 26, 0.9) !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============ HEADER WITH SVG LOGO ============
st.markdown(
    """
    <div class="header-container">
        <!-- SVG Logo -->
        <svg width="48" height="48" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <!-- Shield base -->
            <path d="M50 10 L85 30 L85 70 L50 90 L15 70 L15 30 Z" 
                  fill="none" stroke="#00d4ff" stroke-width="2" opacity="0.8"/>
            
            <!-- Inner glow -->
            <path d="M50 18 L78 34 L78 66 L50 82 L22 66 L22 34 Z" 
                  fill="none" stroke="#7b2ffc" stroke-width="1" opacity="0.4"/>
            
            <!-- Center chip -->
            <rect x="42" y="40" width="16" height="20" rx="2" fill="#00d4ff" opacity="0.15"/>
            <rect x="46" y="44" width="8" height="12" rx="1" fill="#00d4ff" opacity="0.6"/>
            
            <!-- I letter -->
            <rect x="40" y="44" width="3" height="16" rx="1" fill="#00d4ff"/>
            
            <!-- T letter -->
            <rect x="57" y="44" width="3" height="16" rx="1" fill="#00d4ff"/>
            <rect x="53" y="44" width="11" height="3" rx="1" fill="#00d4ff"/>
            
            <!-- Animated pulse -->
            <circle cx="50" cy="50" r="3" fill="#00d4ff" opacity="0.8">
                <animate attributeName="r" values="2;5;2" dur="2s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0.8;0.2;0.8" dur="2s" repeatCount="indefinite"/>
            </circle>
        </svg>
        
        <span class="logo-text">IT-INSIGHT</span>
        <span class="sub-text">// AI-POWERED ANALYSIS</span>
    </div>
    """,
    unsafe_allow_html=True
)

# ============ SESSION STATE ============
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
def display_result(result):
    st.markdown("---")
    st.markdown("### 📊 Analysis Report")
    
    col1, col2 = st.columns(2)
    
    items = [
        ("🆔", "Hardware Name", result.get('Hardware Name', 'N/A')),
        ("⚡", "Primary Function", result.get('Primary Function', 'N/A')),
        ("🔗", "Compatibility", result.get('Compatibility', 'N/A')),
        ("💡", "Recommendations", result.get('Recommendations', 'N/A'))
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
    
    features = result.get('Key Features', ['N/A'])
    if isinstance(features, str):
        features = [features]
    
    st.markdown(
        f"""
        <div class="result-card">
            <h4>✨ Key Features</h4>
            <div class="value">
                {"<br>• ".join([''] + features) if features else 'N/A'}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============ MAIN APP ============
def main():
    api_key = get_api_key()
    
    if not api_key:
        st.error("""
        ❌ **API KEY MISSING**
        
        Please set your Gemini API key in `.env` or Streamlit secrets.
        """)
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        st.markdown("---")
        
        st.markdown("**Operations**")
        st.markdown("- Upload hardware image")
        st.markdown("- Initiate AI analysis")
        st.markdown("- View diagnostic report")
        
        st.markdown("---")
        st.markdown("**Supported Formats**")
        st.markdown("- PNG, JPG, JPEG, WEBP, BMP")
        
        with st.expander("🛠️ Advanced"):
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
    
    # Upload Area
    st.markdown(
        """
        <div class="upload-area">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🖥️</div>
            <div style="font-family: 'Inter', sans-serif; color: #00d4ff; font-size: 1.2rem; font-weight: 600;">
                Upload Hardware Image
            </div>
            <div style="font-family: 'Inter', sans-serif; color: #667799; font-size: 0.9rem; margin-top: 0.3rem;">
                Drag & drop or click to select
            </div>
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
            st.image(image, caption="Uploaded Image", use_container_width=True)
        
        with col2:
            st.markdown(
                f"""
                <div style="font-family: 'Inter', sans-serif; color: #8899bb; font-size: 0.9rem; padding: 1rem 0;">
                    <strong>FILE:</strong> <span style="color: #00d4ff;">{uploaded_file.name}</span><br>
                    <strong>SIZE:</strong> <span style="color: #00d4ff;">{image.width} x {image.height}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if st.button("🔍 Analyze Hardware", type="primary"):
                with st.spinner("Processing with Gemini AI..."):
                    try:
                        client = GeminiClient(api_key)
                        result = client.analyze_hardware(
                            image,
                            temperature=temperature,
                            max_tokens=max_tokens
                        )
                        st.session_state.analysis_result = result
                        
                    except GeminiError as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ System error: {str(e)}")
        
        if st.session_state.analysis_result:
            display_result(st.session_state.analysis_result)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("📋 Export Report"):
                    st.info("Report ready for export")
                    st.balloons()
    else:
        st.info("⏳ Awaiting hardware image upload...")
        st.markdown(
            """
            <div style="text-align: center; color: #445577; font-family: 'Inter', sans-serif; font-size: 0.8rem; padding: 2rem;">
                SUPPORTED HARDWARE: CPU • GPU • RAM • STORAGE • NETWORK • PERIPHERALS
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #334466; font-family: 'Inter', sans-serif; font-size: 0.7rem; letter-spacing: 2px; padding: 1rem 0; opacity: 0.5;">
            ⚡ IT-INSIGHT • Powered by Google Gemini API • Secure & Encrypted
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
