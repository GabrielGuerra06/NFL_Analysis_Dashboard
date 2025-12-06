
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib
matplotlib.use('Agg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime
import warnings
import os
from pathlib import Path
warnings.filterwarnings('ignore')

# Get the directory where this script is located
try:
    SCRIPT_DIR = Path(__file__).parent
except:
    SCRIPT_DIR = Path.cwd()
LOGOS_DIR = SCRIPT_DIR / "NFL_Logos"

# Page Configuration
st.set_page_config(
    page_title="NFL Decade Analytics | 2009-2018",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with Professional NFL Theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@300;400;700;900&display=swap');
    
    /* Main Background with Texture */
    .main {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
        background-attachment: fixed;
    }
    
    /* Animated Header */
    h1 {
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 50%, #FFD700 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shine 3s linear infinite;
        font-family: 'Bebas Neue', cursive;
        font-size: 3.5rem !important;
        font-weight: 900;
        letter-spacing: 3px;
        text-align: center;
        text-shadow: 2px 2px 8px rgba(255, 215, 0, 0.3);
    }
    
    @keyframes shine {
        to {
            background-position: 200% center;
        }
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f3460 100%);
        border-right: 2px solid #FFD700;
        box-shadow: 4px 0 15px rgba(255, 215, 0, 0.1);
    }
    
    section[data-testid="stSidebar"] .css-1d391kg {
        color: #FFD700;
        font-family: 'Bebas Neue', cursive;
        font-size: 1.5rem;
        letter-spacing: 2px;
    }
    
    /* Tab Navigation Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(26, 26, 46, 0.6);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        border-radius: 8px;
        color: #ecf0f1;
        font-weight: 700;
        font-size: 16px;
        padding: 10px 20px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        border-color: #FFD700;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 215, 0, 0.4);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%) !important;
        color: #0a0a0f !important;
        border-color: #ffffff !important;
        box-shadow: 0 8px 16px rgba(255, 215, 0, 0.6);
        font-weight: 900;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 900;
        color: #FFD700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        font-family: 'Bebas Neue', cursive;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1.1rem;
        color: #ecf0f1;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Data Frame Styling */
    .dataframe {
        border: 2px solid #FFD700 !important;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(255, 215, 0, 0.2);
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%) !important;
        color: #FFD700 !important;
        font-weight: bold;
        font-size: 14px;
        padding: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .dataframe tbody tr:hover {
        background-color: rgba(255, 215, 0, 0.1) !important;
        cursor: pointer;
    }
    
    /* Success/Info Messages */
    .stSuccess {
        background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
        border-left: 5px solid #FFD700;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 4px 8px rgba(39, 174, 96, 0.3);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        border-left: 5px solid #FFA500;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
    }
    
    /* Plotly Chart Container */
    .js-plotly-plot {
        border-radius: 10px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        background: rgba(26, 26, 46, 0.6);
        padding: 10px;
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-top-color: #FFD700 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #0a0a0f;
        font-weight: 900;
        border: none;
        padding: 12px 30px;
        font-size: 16px;
        border-radius: 8px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 8px rgba(255, 215, 0, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(255, 215, 0, 0.5);
        background: linear-gradient(135deg, #FFA500 0%, #FFD700 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        border: 2px solid #FFD700;
        border-radius: 8px;
        color: #FFD700;
        font-weight: 700;
        padding: 12px;
        font-size: 16px;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        box-shadow: 0 4px 8px rgba(255, 215, 0, 0.3);
    }
    
    /* Section Headers */
    h2, h3 {
        color: #FFD700;
        font-family: 'Bebas Neue', cursive;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Footer */
    footer {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
        color: #FFD700;
        text-align: center;
        padding: 20px;
        font-family: 'Roboto', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_data():
    """Load NFL play-by-play data - tries parquet first, then CSV"""
    
    # Try to load optimized parquet file first (for cloud deployment)
    parquet_file = SCRIPT_DIR / "datasets" / "nfl_data_cloud.parquet"
    csv_file = SCRIPT_DIR / "datasets" / "NFL Play by Play 2009-2018 (v5).csv"
    
    try:
        if parquet_file.exists():
            st.info("Loading optimized dataset for cloud deployment...")
            df = pd.read_parquet(parquet_file)
            # The parquet already has 'year' column
            return df
        elif csv_file.exists():
            st.info("Loading full dataset from CSV...")
            df = pd.read_csv(csv_file, low_memory=False)
            df['game_date'] = pd.to_datetime(df['game_date'])
            df['year'] = df['game_date'].dt.year
            df = df[(df['year'] >= 2009) & (df['year'] <= 2018)].copy()
            
            # Consolidate SD (San Diego) and LAC (LA Chargers) into LAC
            df['posteam'] = df['posteam'].replace('SD', 'LAC')
            df['defteam'] = df['defteam'].replace('SD', 'LAC')
            
            return df
        else:
            st.error("""
            ### Dataset not found!
            
            Please ensure either:
            - `datasets/nfl_data_cloud.parquet` (optimized, 10MB)
            - `datasets/NFL Play by Play 2009-2018 (v5).csv` (full, 667MB)
            
            exists in your project directory.
            """)
            st.stop()
            return None
            
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        st.stop()
        return None

def main():
    # Display animated header
    st.markdown("<h1>NFL DECADE ANALYTICS DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #ecf0f1; font-family: Roboto;'>Comprehensive Analysis of 2009-2018 Play-by-Play Data</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data with progress indicator
    with st.spinner("Loading NFL analytics data..."):
        df = load_data()
    
    if df is None:
        return
    
    # Display success message
    st.success(f" Dataset loaded successfully! Analyzing {len(df):,} plays across 10 seasons")
    
    # Sidebar filters
    st.sidebar.title(" NFL Analytics Filters")
    st.sidebar.markdown("---")
    
    # Year selection
    years = sorted(df['year'].unique())
    selected_years = st.sidebar.multiselect(
        " Select Seasons",
        options=years,
        default=years
    )
    
    if not selected_years:
        st.warning("Please select at least one season to analyze.")
        st.stop()
    
    # Filter data
    filtered_df = df[df['year'].isin(selected_years)].copy()
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(" Total Plays", f"{len(filtered_df):,}")
    with col2:
        st.metric(" Seasons", f"{len(selected_years)}")
    with col3:
        total_tds = filtered_df['touchdown'].sum() if 'touchdown' in filtered_df.columns else 0
        st.metric(" Touchdowns", f"{int(total_tds):,}")
    with col4:
        total_games = filtered_df['game_id'].nunique() if 'game_id' in filtered_df.columns else 0
        st.metric(" Games", f"{total_games:,}")
    
    st.markdown("---")
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        " Team Performance",
        " QB Analysis",
        " RB Statistics",
        " WR Metrics",
        " Defensive Analysis",
        " Geographic Distribution",
        " Advanced Seaborn Viz"
    ])
    
    with tab1:
        show_team_performance(filtered_df)
    
    with tab2:
        show_qb_analysis(filtered_df)
    
    with tab3:
        show_rb_statistics(filtered_df)
    
    with tab4:
        show_wr_metrics(filtered_df)
    
    with tab5:
        show_defensive_analysis(filtered_df)
    
    with tab6:
        show_geographic_distribution(filtered_df)
    
    with tab7:
        show_seaborn_visualizations(filtered_df)

# Import the visualization functions from the full file
# (We'll need to copy them here or import them - for now I'll create simplified versions)

def show_team_performance(df):
    st.markdown("### Team Performance Over Time")
    st.markdown("""
    **Data Storytelling**: This visualization tracks offensive performance trends across NFL teams throughout the decade. 
    Watch how dominant franchises emerged, dynasties were built, and competitive balances shifted year by year. 
    The racing bar chart reveals which teams consistently drove the most yards, highlighting coaching strategies and roster strengths.
    """)
    
    # Calculate team statistics
    if 'yards_gained' in df.columns and 'posteam' in df.columns:
        team_stats = df.groupby(['year', 'posteam'])['yards_gained'].sum().reset_index()
        team_stats = team_stats.sort_values(['year', 'yards_gained'], ascending=[True, False])
        
        # Create racing bar chart
        fig = go.Figure()
        
        years = sorted(team_stats['year'].unique())
        
        for year in years:
            year_data = team_stats[team_stats['year'] == year].nlargest(10, 'yards_gained')
            
            fig.add_trace(go.Bar(
                x=year_data['yards_gained'],
                y=year_data['posteam'],
                orientation='h',
                name=str(year),
                visible=(year == years[0])
            ))
        
        # Add animation buttons
        steps = []
        for i, year in enumerate(years):
            step = dict(
                method="update",
                args=[{"visible": [j == i for j in range(len(years))]}],
                label=str(year)
            )
            steps.append(step)
        
        sliders = [dict(
            active=0,
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.85,
            currentvalue=dict(
                prefix="Year: ",
                visible=True,
                xanchor="right"
            ),
            pad=dict(b=10, t=50),
            len=0.9,
            steps=steps
        )]
        
        fig.update_layout(
            title="Top 10 Teams by Total Yards Gained",
            sliders=sliders,
            xaxis_title="Total Yards",
            yaxis_title="Team",
            height=600,
            template="plotly_dark"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Required columns not available for team performance analysis.")

def show_qb_analysis(df):
    st.markdown("### Quarterback Performance Analysis")
    st.markdown("""
    **Elite QB Evolution**: This section analyzes the quarterbacks who defined the decade. From touchdown passes to 
    interception rates, discover which signal-callers dominated the era and how passing strategies evolved from 2009 to 2018.
    """)
    
    if 'passer_player_name' in df.columns and 'pass_touchdown' in df.columns:
        qb_stats = df[df['passer_player_name'].notna()].groupby('passer_player_name').agg({
            'pass_touchdown': 'sum',
            'interception': 'sum',
            'yards_gained': 'sum'
        }).reset_index()
        
        qb_stats = qb_stats.sort_values('pass_touchdown', ascending=False).head(20)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=qb_stats['passer_player_name'],
            y=qb_stats['pass_touchdown'],
            name='Touchdowns',
            marker_color='#FFD700'
        ))
        
        fig.update_layout(
            title="Top 20 Quarterbacks by Passing Touchdowns (2009-2018)",
            xaxis_title="Quarterback",
            yaxis_title="Passing Touchdowns",
            height=600,
            template="plotly_dark",
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show top QBs table
        st.dataframe(qb_stats.head(10), use_container_width=True)
    else:
        st.warning("QB statistics not available in dataset.")

def show_rb_statistics(df):
    st.markdown("### Running Back Performance")
    st.markdown("""
    **Ground Game Dominance**: Explore the running backs who powered their teams' offenses. This analysis reveals 
    rushing efficiency, touchdown production, and the evolution of the running game in modern NFL strategy.
    """)
    
    if 'rusher_player_name' in df.columns and 'rush_touchdown' in df.columns:
        rb_stats = df[df['rusher_player_name'].notna()].groupby('rusher_player_name').agg({
            'rush_touchdown': 'sum',
            'yards_gained': 'sum'
        }).reset_index()
        
        rb_stats = rb_stats[rb_stats['yards_gained'] > 1000].sort_values('rush_touchdown', ascending=False).head(20)
        
        fig = px.scatter(
            rb_stats,
            x='yards_gained',
            y='rush_touchdown',
            text='rusher_player_name',
            title="Top Running Backs: Yards vs Touchdowns",
            labels={'yards_gained': 'Total Rushing Yards', 'rush_touchdown': 'Rushing Touchdowns'}
        )
        
        fig.update_traces(textposition='top center', marker=dict(size=12, color='#FFA500'))
        fig.update_layout(height=600, template="plotly_dark")
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("RB statistics not available in dataset.")

def show_wr_metrics(df):
    st.markdown("### Wide Receiver Analysis")
    st.markdown("""
    **Receiving Excellence**: Chart the top pass-catchers of the decade. This visualization highlights the receivers 
    who consistently found the end zone and accumulated yards, showcasing the evolution of passing attacks.
    """)
    
    st.info("WR analysis coming soon with full dataset columns.")

def show_defensive_analysis(df):
    st.markdown("### Defensive Performance")
    st.markdown("""
    **Defensive Dominance**: Analyze which teams' defenses created turnovers, generated sacks, and controlled opponents. 
    Defense wins championships - see which units proved this adage true during the decade.
    """)
    
    if 'defteam' in df.columns and 'interception' in df.columns:
        def_stats = df.groupby('defteam').agg({
            'interception': 'sum',
            'sack': 'sum',
            'fumble': 'sum'
        }).reset_index()
        
        def_stats['total_turnovers'] = def_stats['interception'] + def_stats['fumble']
        def_stats = def_stats.sort_values('total_turnovers', ascending=False)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=def_stats['defteam'],
            y=def_stats['interception'],
            name='Interceptions',
            marker_color='#FF6B6B'
        ))
        fig.add_trace(go.Bar(
            x=def_stats['defteam'],
            y=def_stats['fumble'],
            name='Fumbles Recovered',
            marker_color='#4ECDC4'
        ))
        
        fig.update_layout(
            title="Defensive Turnovers by Team",
            xaxis_title="Team",
            yaxis_title="Turnovers",
            barmode='stack',
            height=600,
            template="plotly_dark"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Defensive statistics not available.")

def show_geographic_distribution(df):
    st.markdown("### Geographic Team Distribution")
    st.markdown("""
    **NFL Geography**: Visualize where NFL teams are located across the United States. This map shows the 
    geographic distribution of franchises and their regional concentrations.
    """)
    
    st.info("Geographic visualization requires additional team location data. Coming soon!")

def show_seaborn_visualizations(df):
    st.markdown("### Advanced Statistical Visualizations")
    st.markdown("""
    **Statistical Deep Dive**: Advanced statistical analyses using Seaborn to uncover patterns in play types, 
    scoring distributions, and performance correlations that tell the deeper story of NFL strategy.
    """)
    
    # Play type distribution
    if 'play_type' in df.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        play_counts = df['play_type'].value_counts().head(10)
        sns.barplot(x=play_counts.values, y=play_counts.index, palette='viridis', ax=ax)
        ax.set_title('Top 10 Play Types Distribution', fontsize=16, fontweight='bold')
        ax.set_xlabel('Count', fontsize=12)
        ax.set_ylabel('Play Type', fontsize=12)
        st.pyplot(fig)
        plt.close()
    
    # Yards gained distribution
    if 'yards_gained' in df.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        yards_clean = df['yards_gained'].dropna()
        yards_clean = yards_clean[(yards_clean >= -20) & (yards_clean <= 50)]
        sns.histplot(yards_clean, bins=50, kde=True, color='#FFD700', ax=ax)
        ax.set_title('Distribution of Yards Gained per Play', fontsize=16, fontweight='bold')
        ax.set_xlabel('Yards Gained', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        st.pyplot(fig)
        plt.close()

if __name__ == "__main__":
    main()

