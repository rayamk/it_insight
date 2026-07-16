"""
IT-Insight: Hardware Analysis Tool
Main Streamlit application entry point
"""

import streamlit as st
from PIL import Image
import os
from utils.gemini_client import GeminiClient
from utils.gemini_client import GeminiError

# Page configuration
st.set_page_config(
    page_title="IT-Insight - Hardware Analyzer",
    page_icon="🖥️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #00FF00;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #888;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-card {
        background-color: #1e1e1e;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #00FF00;
        margin: 1rem 0;
    }
    .stButton button {
        width: 100%;
        background-color: #00FF00;
        color: #000;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None

def display_header():
    """Display the app header"""
    st.markdown('<p class="main-header">🖥️ IT-Insight</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">AI-Powered Hardware Analysis Tool</p>',
        unsafe_allow_html=True
    )

def get_api_key():
    """Retrieve API key from environment or Streamlit secrets"""
    # Try to get from Streamlit secrets first
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        return api_key
    except (KeyError, AttributeError):
        pass
    
    # Fallback to environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key
    
    # If no key found, return None
    return None

def display_result(result):
    """Display the analysis results in a clean format"""
    st.markdown("### 📊 Analysis Results")
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("**🆔 Hardware Name**")
            st.write(result.get('Hardware Name', 'N/A'))
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("**⚡ Primary Function**")
            st.write(result.get('Primary Function', 'N/A'))
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("**🔗 Compatibility**")
            st.write(result.get('Compatibility', 'N/A'))
            st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("**✨ Key Features**")
        features = result.get('Key Features', 'N/A')
        if features != 'N/A' and isinstance(features, list):
            for feature in features:
                st.markdown(f"• {feature}")
        else:
            st.write(features)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("**💡 Recommendations**")
        st.write(result.get('Recommendations', 'N/A'))
        st.markdown("</div>", unsafe_allow_html=True)

def main():
    """Main application logic"""
    initialize_session_state()
    display_header()
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        st.markdown("---")
        st.markdown("**How it works:**")
        st.markdown("""
        1. Upload an image of IT hardware
        2. Click 'Analyze' button
        3. Get instant AI-powered insights
        """)
        
        st.markdown("---")
        st.markdown("**Supported Formats:**")
        st.markdown("PNG, JPG, JPEG, WEBP, BMP")
        
        # Advanced settings
        with st.expander("🛠️ Advanced Settings"):
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values make output more creative, lower values more deterministic"
            )
            max_tokens = st.slider(
                "Max Tokens",
                min_value=100,
                max_value=1000,
                value=300,
                step=50,
                help="Maximum length of the response"
            )
    
    # Main content area
    api_key = get_api_key()
    
    if not api_key:
        st.error("""
        ❌ **API Key Missing!** 
        
        Please set your Google Gemini API key using one of these methods:
        1. Create a `.env` file with `GEMINI_API_KEY=your_key_here`
        2. Add to Streamlit secrets in `.streamlit/secrets.toml`
        """)
        st.stop()
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📤 Upload IT Hardware Image",
        type=['png', 'jpg', 'jpeg', 'webp', 'bmp'],
        help="Upload a clear image of the hardware for analysis"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([1, 1])
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
        
        with col2:
            if st.button("🔍 Analyze Hardware", type="primary"):
                with st.spinner("🧠 Analyzing with Gemini AI..."):
                    try:
                        # Initialize Gemini client
                        client = GeminiClient(api_key)
                        
                        # Analyze the image
                        result = client.analyze_hardware(
                            image,
                            temperature=temperature,
                            max_tokens=max_tokens
                        )
                        
                        # Store result in session state
                        st.session_state.analysis_result = result
                        
                    except GeminiError as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ An unexpected error occurred: {str(e)}")
        
        # Display results if available
        if st.session_state.analysis_result:
            display_result(st.session_state.analysis_result)
            
            # Export option
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("📋 Copy Results to Clipboard"):
                    st.info("Results displayed above. You can manually copy them.")
                    st.balloons()
    
    else:
        # Show placeholder when no image is uploaded
        st.info("👆 Upload an image of IT hardware to start the analysis")
        
        # Example use cases
        with st.expander("📚 Example Use Cases"):
            st.markdown("""
            - **Server Components**: Identify server CPUs, RAM modules, or motherboards
            - **Network Equipment**: Analyze routers, switches, or network adapters
            - **Storage Devices**: Identify HDDs, SSDs, or NVMe drives
            - **Peripherals**: Recognize keyboards, mice, or monitors
            - **Cables & Adapters**: Identify connectivity hardware
            """)

if __name__ == "__main__":
    main()
