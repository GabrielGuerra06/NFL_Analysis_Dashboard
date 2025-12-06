import streamlit as st
from pathlib import Path

# Get script directory
try:
    SCRIPT_DIR = Path(__file__).parent
except:
    SCRIPT_DIR = Path.cwd()

# Page Configuration
st.set_page_config(
    page_title="NFL Decade Analytics | 2009-2018",
    layout="wide"
)

# Check if dataset exists
csv_file = SCRIPT_DIR / "datasets" / "NFL Play by Play 2009-2018 (v5).csv"

if not csv_file.exists():
    # Dataset missing - show error page
    st.title("🏈 NFL DECADE ANALYTICS DASHBOARD")
    st.markdown("---")
    
    st.error("""
    ### 📊 Dataset Required
    
    This dashboard requires the NFL Play-by-Play dataset (667 MB), which is too large for Streamlit Cloud's free tier.
    """)
    
    st.markdown("""
    ### 🚀 To run this dashboard locally:
    
    **1. Clone the repository:**
    ```bash
    git clone https://github.com/GabrielGuerra06/NFL_Analysis_Dashboard.git
    cd NFL_Analysis_Dashboard
    ```
    
    **2. Download the dataset:**
    - Visit: [Kaggle NFL Dataset](https://www.kaggle.com/datasets/maxhorowitz/nflplaybyplay2009to2016)
    - Download **"NFL Play by Play 2009-2018 (v5).csv"**
    - Create a `datasets` folder in the project directory
    - Place the CSV file inside the `datasets` folder
    
    **3. Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```
    
    **4. Run the dashboard:**
    ```bash
    streamlit run nfl_streamlit_app.py
    ```
    """)
    
    st.info("💡 **Alternative:** You can deploy this on a cloud VM with more resources.")
    
    st.markdown("---")
    st.markdown("""
    ### 📖 About This Dashboard
    
    This comprehensive NFL analytics dashboard provides:
    - **Team Performance Analysis** with racing bar visualizations
    - **Quarterback Statistics** across a decade
    - **Running Back & Wide Receiver Metrics**
    - **Defensive Analysis** and comparisons
    - **Geographic Team Distribution** with interactive maps
    - **Seaborn Statistical Visualizations**
    
    Check out the [GitHub Repository](https://github.com/GabrielGuerra06/NFL_Analysis_Dashboard) to explore the code!
    """)
    
    # Debug info
    with st.expander("🔧 Debug Information"):
        st.write(f"**Script Directory:** `{SCRIPT_DIR}`")
        st.write(f"**Looking for CSV at:** `{csv_file}`")
        st.write(f"**File exists:** `{csv_file.exists()}`")
    
    st.stop()

else:
    # Dataset exists - redirect to full app
    st.info("Dataset found! Please use `nfl_streamlit_app.py` for the full dashboard with all visualizations.")
    st.stop()
