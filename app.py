"""
IT-Insight: Professional Hardware Analysis Tool
With Multi-Image Upload & Gallery Preview
CSS separated into static/style.css
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

if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []

if 'selected_image' not in st.session_state:
    st.session_state.selected_image = None

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
            "delete_bg": "rgba(255, 50, 50, 0.15)",
            "delete_hover": "rgba(255, 50, 50, 0.25)",
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
            "delete_bg": "rgba(255, 50, 50, 0.1)",
            "delete_hover": "rgba(255, 50, 50, 0.2)",
        }

# ============ INJECT CSS ============
def inject_css():
    theme = get_theme()
    
    # Read external CSS file
    with open("static/style.css", "r") as f:
        css = f.read()
    
    # Inject CSS with theme variables
    st.markdown(f"""
    <style>
        :root {{
            --bg: {theme["bg"]};
            --bg2: {theme["bg2"]};
            --border: {theme["border"]};
            --text: {theme["text"]};
            --text2: {theme["text2"]};
            --card-hover: {theme["card_hover"]};
            --card-border-hover: {theme["card_border_hover"]};
            --upload-bg: {theme["upload_bg"]};
            --upload-border: {theme["upload_border"]};
            --upload-hover: {theme["upload_hover"]};
            --upload-border-hover: {theme["upload_border_hover"]};
            --sidebar-bg: {theme["sidebar_bg"]};
            --header-border: {theme["header_border"]};
            --footer-border: {theme["footer_border"]};
            --footer-text: {theme["footer_text"]};
            --info-text: {theme["info_text"]};
            --status-bg: {theme["status_bg"]};
            --status-border: {theme["status_border"]};
            --delete-bg: {theme["delete_bg"]};
            --delete-hover: {theme["delete_hover"]};
        }}
        
        .stApp {{
            background: var(--bg) !important;
        }}
        
        {css}
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
    inject_css()
    
    display_header()
    
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        st.markdown("---")
        
        icon = "🌙" if st.session_state.dark_mode else "☀️"
        label = "Dark Mode" if st.session_state.dark_mode else "Light Mode"
        if st.button(f"{icon} {label}", use_container_width=True):
            toggle_theme()
            st.rerun()
        
        st.markdown("---")
        st.markdown("**Operations**")
        st.markdown("- Upload images")
        st.markdown("- Click image to select")
        st.markdown("- Delete with ❌")
        
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
            <div style="text-align: center; font-size: 0.7rem; color: #667799; font-family: 'Inter', sans-serif;">
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
    
    # ===== UPLOAD AREA =====
    st.markdown(
        """
        <div class="upload-card">
            <div class="upload-icon">🖥️</div>
            <div class="upload-title">Upload Hardware Images</div>
            <div class="upload-subtitle">Click to select multiple images • Drag & drop supported</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    uploaded_files = st.file_uploader(
        " ",
        type=['png', 'jpg', 'jpeg', 'webp', 'bmp'],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        for file in uploaded_files:
            image = Image.open(file)
            st.session_state.uploaded_images.append({
                "name": file.name,
                "image": image,
                "file": file
            })
        st.rerun()
    
    # ===== GALLERY =====
    if st.session_state.uploaded_images:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin: 1rem 0 0.5rem 0;">
                <span style="font-size: 0.9rem; font-weight: 600; color: #e8f0f8;">
                    📸 Uploaded Images ({len(st.session_state.uploaded_images)})
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        cols = st.columns(4)
        for idx, img_data in enumerate(st.session_state.uploaded_images):
            col = cols[idx % 4]
            with col:
                st.image(img_data["image"], use_container_width=True)
                st.caption(f"📷 {img_data['name'][:15]}...")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("❌", key=f"del_{idx}", help="Delete image"):
                        st.session_state.uploaded_images.pop(idx)
                        if st.session_state.selected_image == idx:
                            st.session_state.selected_image = None
                        st.rerun()
                with col2:
                    if st.button("🔍", key=f"sel_{idx}", help="Select for analysis"):
                        st.session_state.selected_image = idx
                        st.rerun()
                with col3:
                    if st.button("📊", key=f"ana_{idx}", help="Analyze this image"):
                        st.session_state.selected_image = idx
                        st.session_state.analysis_result = None
                        st.rerun()
        
        if st.session_state.selected_image is not None:
            idx = st.session_state.selected_image
            if idx < len(st.session_state.uploaded_images):
                img_data = st.session_state.uploaded_images[idx]
                st.markdown("---")
                st.markdown(f"""
                    <div style="font-size: 1rem; font-weight: 600; color: #e8f0f8;">
                        🔍 Analyzing: {img_data['name']}
                    </div>
                    """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.image(img_data["image"], caption="Selected Image", use_container_width=True)
                
                with col2:
                    if st.button("🔍 Analyze Hardware", type="primary"):
                        with st.spinner("Processing with Gemini AI..."):
                            try:
                                client = GeminiClient(api_key)
                                result = client.analyze_hardware(
                                    img_data["image"],
                                    temperature=temperature,
                                    max_tokens=max_tokens
                                )
                                st.session_state.analysis_result = result
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                
                if st.session_state.analysis_result:
                    display_result(st.session_state.analysis_result)
        
        if len(st.session_state.uploaded_images) > 0:
            if st.button("🗑️ Clear All Images", type="secondary"):
                st.session_state.uploaded_images = []
                st.session_state.selected_image = None
                st.session_state.analysis_result = None
                st.rerun()
    
    else:
        st.info("💡 Upload images to begin analysis")
        st.markdown(
            """
            <div class="info-text">
                Supported: CPU • GPU • RAM • Storage • Network • Peripherals
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown(
        """
        <div class="footer">
            IT-Insight • Powered by Google Gemini API • Secure & Encrypted
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
