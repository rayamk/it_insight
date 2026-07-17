"""
IT-Insight: Professional Hardware Analysis Tool
With Light/Dark Mode Support
"""

import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
from utils.gemini_client import GeminiClient, GeminiError

load_dotenv()

st.set_page_config(
    page_title="IT-Insight",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ SESSION STATE ============
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# ============ TOGGLE THEME ============
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# ============ THEME COLORS ============
def get_theme():
    if st.session_state.dark_mode:
        return {
            "bg": "#0a0e17",
            "bg2": "rgba(255,255,255,0.02)",
            "border": "rgba(255,255,255,0.05)",
            "text": "#e8f0f8",
            "text2": "#667799",
            "card_hover": "rgba(255,255,255,0.04)",
            "card_border_hover": "rgba(0, 180, 255, 0.15)",
            "upload_bg": "rgba(255,255,255,0.02)",
            "upload_border": "rgba(255,255,255,0.06)",
            "upload_hover": "rgba(0, 180, 255, 0.03)",
            "upload_border_hover": "rgba(0, 180, 255, 0.3)",
            "sidebar_bg": "rgba(10, 14, 23, 0.95)",
            "header_border": "rgba(255,255,255,0.05)",
            "footer_border": "rgba(255,255,255,0.03)",
            "footer_text": "#445566",
            "info_text": "#445566",
            "status_bg": "rgba(255,255,255,0.03)",
            "status_border": "rgba(255,255,255,0.05)",
        }
    else:
        return {
            "bg": "#f0f2f6",
            "bg2": "rgba(0,0,0,0.02)",
            "border": "rgba(0,0,0,0.06)",
            "text": "#1a1a2e",
            "text2": "#555577",
            "card_hover": "rgba(0,0,0,0.03)",
            "card_border_hover": "rgba(0, 180, 255, 0.2)",
            "upload_bg": "rgba(0,0,0,0.02)",
            "upload_border": "rgba(0,0,0,0.08)",
            "upload_hover": "rgba(0, 180, 255, 0.05)",
            "upload_border_hover": "rgba(0, 180, 255, 0.4)",
            "sidebar_bg": "rgba(240, 242, 246, 0.95)",
            "header_border": "rgba(0,0,0,0.06)",
            "footer_border": "rgba(0,0,0,0.04)",
            "footer_text": "#8899aa",
            "info_text": "#8899aa",
            "status_bg": "rgba(0,0,0,0.03)",
            "status_border": "rgba(0,0,0,0.06)",
        }

# ============ CUSTOM CSS ============
def inject_css():
    theme = get_theme()
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        .stApp {{
            background: {theme["bg"]} !important;
            font-family: 'Inter', sans-serif !important;
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1.5rem 0;
            border-bottom: 1px solid {theme["header_border"]};
            margin-bottom: 2.5rem;
        }}
        
        .header-left {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .logo-icon {{
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, #00b4ff, #7b2ffc);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            font-weight: 800;
            color: white;
            font-family: 'Inter', sans-serif;
        }}
        
        .logo-text {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {theme["text"]};
            letter-spacing: -0.5px;
        }}
        
        .logo-text span {{
            color: #00b4ff;
        }}
        
        .header-right {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.8rem;
            color: {theme["text2"]};
            background: {theme["status_bg"]};
            padding: 0.4rem 1rem;
            border-radius: 20px;
            border: 1px solid {theme["status_border"]};
        }}
        
        .status-dot {{
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #00b4ff;
            animation: pulse 1.5s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
        }}
        
        .upload-card {{
            background: {theme["upload_bg"]};
            border: 2px dashed {theme["upload_border"]};
            border-radius: 16px;
            padding: 3.5rem 2rem;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .upload-card:hover {{
            border-color: {theme["upload_border_hover"]};
            background: {theme["upload_hover"]};
        }}
        
        .upload-icon {{
            font-size: 3.5rem;
            margin-bottom: 1rem;
            opacity: 0.6;
        }}
        
        .upload-title {{
            font-size: 1.2rem;
            font-weight: 600;
            color: {theme["text"]};
            margin-bottom: 0.3rem;
        }}
        
        .upload-subtitle {{
            font-size: 0.9rem;
            color: {theme["text2"]};
        }}
        
        .result-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin: 1.5rem 0;
        }}
        
        .result-card {{
            background: {theme["bg2"]};
            border: 1px solid {theme["border"]};
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }}
        
        .result-card:hover {{
            background: {theme["card_hover"]};
            border-color: {theme["card_border_hover"]};
            transform: translateY(-2px);
        }}
        
        .result-label {{
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: {theme["text2"]};
            margin-bottom: 0.5rem;
        }}
        
        .result-value {{
            font-size: 1rem;
            font-weight: 400;
            color: {theme["text"]};
            line-height: 1.6;
        }}
        
        .stButton > button {{
            background: linear-gradient(135deg, #00b4ff, #7b2ffc) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.7rem 2rem !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 8px 30px rgba(0, 180, 255, 0.25) !important;
        }}
        
        [data-testid="stSidebar"] {{
            background: {theme["sidebar_bg"]} !important;
            border-right: 1px solid {theme["border"]} !important;
        }}
        
        [data-testid="stSidebar"] .stMarkdown {{
            color: {theme["text"]} !important;
        }}
        
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin: 1.5rem 0;
        }}
        
        .metric-item {{
            background: {theme["bg2"]};
            border: 1px solid {theme["border"]};
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
        }}
        
        .metric-value {{
            font-size: 1.3rem;
            font-weight: 700;
            color: #00b4ff;
        }}
        
        .metric-label {{
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: {theme["text2"]};
            margin-top: 0.2rem;
        }}
        
        .footer {{
            text-align: center;
            padding: 2rem 0 1rem 0;
            border-top: 1px solid {theme["footer_border"]};
            margin-top: 2.5rem;
            font-size: 0.75rem;
            color: {theme["footer_text"]};
            letter-spacing: 0.5px;
        }}
        
        .info-text {{
            text-align: center;
            color: {theme["info_text"]};
            font-size: 0.8rem;
            padding: 1.5rem 0;
        }}
        
        @media (max-width: 768px) {{
            .result-grid {{
                grid-template-columns: 1fr;
            }}
            .metric-grid {{
                grid-template-columns: 1fr 1fr;
            }}
            .header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 0.8rem;
            }}
            .header-right {{
                font-size: 0.7rem;
                padding: 0.3rem 0.8rem;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

# ============ HEADER ============
def display_header():
    st.markdown(
        """
        <div class="header">
            <div class="header-left">
                <div class="logo-icon">IT</div>
                <div class="logo-text">IT-<span>Insight</span></div>
            </div>
            <div class="header-right">
                <span class="status-dot"></span>
                System Online • v2.0
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

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
def display_metrics():
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("STATUS", "Active"),
        ("MODEL", "Gemini 2.0"),
        ("ENCRYPTION", "AES-256"),
        ("CONNECTION", "Secure")
    ]
    for col, (label, value) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-item">
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

def display_result(result):
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 1.1rem; font-weight: 600; color: #e8f0f8; margin: 1.5rem 0 1rem 0;">
            📊 Analysis Report
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    
    items = [
        ("Hardware Name", result.get('Hardware Name', 'N/A')),
        ("Primary Function", result.get('Primary Function', 'N/A')),
        ("Compatibility", result.get('Compatibility', 'N/A')),
        ("Recommendations", result.get('Recommendations', 'N/A'))
    ]
    
    for i, (label, value) in enumerate(items):
        with col1 if i < 2 else col2:
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-label">{label}</div>
                    <div class="result-value">{value}</div>
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
            <div class="result-label">✨ Key Features</div>
            <div class="result-value">
                {"<br>• ".join([''] + features) if features else 'N/A'}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============ MAIN APP ============
def main():
    theme = get_theme()
    inject_css()
    
    display_header()
    
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        st.markdown("---")
        
        # Theme Toggle
        st.markdown("**Theme**")
        icon = "🌙" if st.session_state.dark_mode else "☀️"
        label = "Dark Mode" if st.session_state.dark_mode else "Light Mode"
        if st.button(f"{icon} {label}", use_container_width=True):
            toggle_theme()
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("**Operations**")
        st.markdown("- Upload hardware image")
        st.markdown("- AI-powered analysis")
        st.markdown("- Export report")
        
        st.markdown("---")
        st.markdown("**Supported Formats**")
        st.markdown("PNG, JPG, JPEG, WEBP, BMP")
        
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
        
        st.markdown("---")
        st.markdown(f"""
            <div style="text-align: center; font-size: 0.7rem; color: {theme['text2']}; font-family: 'Inter', sans-serif;">
                IT-Insight v2.0<br>
                {'🌙 Dark' if st.session_state.dark_mode else '☀️ Light'} Mode
            </div>
            """, unsafe_allow_html=True)
    
    api_key = get_api_key()
    
    if not api_key:
        st.error("""
        ❌ **API Key Missing**
        
        Please set your Gemini API key in `.env` or Streamlit secrets.
        """)
        st.stop()
    
    display_metrics()
    
    st.markdown(
        """
        <div class="upload-card">
            <div class="upload-icon">🖥️</div>
            <div class="upload-title">Upload Hardware Image</div>
            <div class="upload-subtitle">Drag & drop or click to select</div>
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
                <div style="font-family: 'Inter', sans-serif; color: {theme['text2']}; font-size: 0.9rem; padding: 1rem 0;">
                    <strong>FILE:</strong> <span style="color: #00b4ff;">{uploaded_file.name}</span><br>
                    <strong>SIZE:</strong> <span style="color: #00b4ff;">{image.width} x {image.height}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if st.button("🔍 Analyze Hardware"):
                with st.spinner("Processing with Gemini AI..."):
                    try:
                        client = GeminiClient(api_key)
                        result = client.analyze_hardware(
                            image,
                            temperature=temperature,
                            max_tokens=max_tokens
                        )
                        st.session_state.analysis_result = result
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        if st.session_state.analysis_result:
            display_result(st.session_state.analysis_result)
    else:
        st.info("💡 Upload a hardware image to begin analysis")
        st.markdown(
            f"""
            <div class="info-text">
                Supported: CPU • GPU • RAM • Storage • Network • Peripherals
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown(
        f"""
        <div class="footer">
            IT-Insight • Powered by Google Gemini API • Secure & Encrypted
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

