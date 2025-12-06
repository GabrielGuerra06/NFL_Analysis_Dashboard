
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
    page_title=" NFL Decade Analytics | 2009-2018",
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
        font-family: 'Bebas Neue', 'Arial Black', sans-serif;
        text-align: center;
        font-size: 4rem !important;
        font-weight: 900;
        letter-spacing: 4px;
        animation: glow 2s ease-in-out infinite alternate, shimmer 3s linear infinite;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        margin: 20px 0 30px 0 !important;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px #FFD700); }
        to { filter: drop-shadow(0 0 25px #FFA500); }
    }
    
    @keyframes shimmer {
        to { background-position: 200% center; }
    }
    
    /* Section Headers with Icons */
    h2 {
        color: #00D9FF;
        font-family: 'Bebas Neue', 'Arial Black', sans-serif;
        font-weight: 800;
        font-size: 2.5rem !important;
        border-bottom: 4px solid #FFD700;
        border-image: linear-gradient(90deg, #FFD700, #FFA500, transparent) 1;
        padding-bottom: 15px;
        margin-top: 3rem !important;
        margin-bottom: 2rem !important;
        letter-spacing: 2px;
        text-shadow: 0 2px 10px rgba(0, 217, 255, 0.3);
    }
    
    h3 {
        color: #FFD700;
        font-family: 'Roboto', sans-serif;
        font-weight: 700;
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        letter-spacing: 1px;
    }
    
    h4 {
        color: #00D9FF;
        font-family: 'Roboto', sans-serif;
        font-weight: 600;
        font-size: 1.4rem !important;
    }
    
    /* Enhanced Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 3rem !important;
        font-weight: 900;
        font-family: 'Bebas Neue', sans-serif;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: #00D9FF !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        font-family: 'Roboto', sans-serif;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: #FFD700;
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(255, 215, 0, 0.4);
    }
    
    /* Enhanced Tab System */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 65px;
        background: linear-gradient(135deg, #1a1a2e 0%, #0a0a0f 100%);
        border-radius: 12px;
        color: #00D9FF;
        font-weight: 700;
        font-size: 1.15rem;
        font-family: 'Roboto', sans-serif;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        padding: 0 35px;
        justify-content: center;
        text-align: center;
        letter-spacing: 1px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
        border-color: #FFD700;
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%) !important;
        color: #000 !important;
        font-weight: 900;
        border: 2px solid #00D9FF !important;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.6);
    }
    
    /* Info/Warning/Success Boxes */
    .stAlert {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.95) 0%, rgba(22, 33, 62, 0.95) 100%);
        border-radius: 12px;
        border-left: 5px solid #00D9FF;
        padding: 20px;
        margin: 15px 0;
        font-family: 'Roboto', sans-serif;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar Enhancements */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0f 0%, #16213e 100%);
        border-right: 3px solid #FFD700;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #FFD700;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2rem !important;
        border-bottom: 3px solid #00D9FF;
    }
    
    /* Input Fields */
    .stTextInput input, .stMultiSelect {
        background-color: rgba(26, 26, 46, 0.8) !important;
        color: white !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 8px;
        font-family: 'Roboto', sans-serif;
    }
    
    .stTextInput input:focus, .stMultiSelect:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
    }
    
    /* Plotly Chart Containers */
    .js-plotly-plot {
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .js-plotly-plot:hover {
        box-shadow: 0 12px 30px rgba(255, 215, 0, 0.3);
        transform: translateY(-2px);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0f;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #FFA500 0%, #FFD700 100%);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        margin: 30px 0;
    }
    
    /* Loading Animation */
    .stSpinner > div {
        border-top-color: #FFD700 !important;
    }
    
    /* Column Spacing */
    [data-testid="column"] {
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# NFL Team Colors and Names
NFL_COLORS = {
    'ARI': '#97233F', 'ATL': '#A71930', 'BAL': '#241773', 'BUF': '#00338D',
    'CAR': '#0085CA', 'CHI': '#0B162A', 'CIN': '#FB4F14', 'CLE': '#311D00',
    'DAL': '#041E42', 'DEN': '#FB4F14', 'DET': '#0076B6', 'GB': '#203731',
    'HOU': '#03202F', 'IND': '#002C5F', 'JAX': '#006778', 'KC': '#E31837',
    'LAC': '#0080C6', 'LA': '#003594', 'MIA': '#008E97', 'MIN': '#4F2683',
    'NE': '#002244', 'NO': '#D3BC8D', 'NYG': '#0B2265', 'NYJ': '#125740',
    'OAK': '#000000', 'PHI': '#004C54', 'PIT': '#FFB612', 'SF': '#AA0000',
    'SEA': '#002244', 'TB': '#D50A0A', 'TEN': '#0C2340', 'WAS': '#773141', 'SD': '#0080C6'
}

NFL_NAMES = {
    'ARI': 'Arizona Cardinals', 'ATL': 'Atlanta Falcons', 'BAL': 'Baltimore Ravens',
    'BUF': 'Buffalo Bills', 'CAR': 'Carolina Panthers', 'CHI': 'Chicago Bears',
    'CIN': 'Cincinnati Bengals', 'CLE': 'Cleveland Browns', 'DAL': 'Dallas Cowboys',
    'DEN': 'Denver Broncos', 'DET': 'Detroit Lions', 'GB': 'Green Bay Packers',
    'HOU': 'Houston Texans', 'IND': 'Indianapolis Colts', 'JAX': 'Jacksonville Jaguars',
    'KC': 'Kansas City Chiefs', 'LAC': 'LA Chargers', 'LA': 'LA Rams',
    'MIA': 'Miami Dolphins', 'MIN': 'Minnesota Vikings', 'NE': 'New England Patriots',
    'NO': 'New Orleans Saints', 'NYG': 'New York Giants', 'NYJ': 'New York Jets',
    'OAK': 'Oakland Raiders', 'PHI': 'Philadelphia Eagles', 'PIT': 'Pittsburgh Steelers',
    'SF': 'San Francisco 49ers', 'SEA': 'Seattle Seahawks', 'TB': 'Tampa Bay Buccaneers',
    'TEN': 'Tennessee Titans', 'WAS': 'Washington', 'SD': 'San Diego Chargers'
}

# NFL Stadium Locations
NFL_LOCATIONS = {
    'ARI': (33.5276, -112.2626), 'ATL': (33.7490, -84.3880), 'BAL': (39.2904, -76.6122),
    'BUF': (42.8864, -78.8784), 'CAR': (35.2271, -80.8431), 'CHI': (41.8781, -87.6298),
    'CIN': (39.1031, -84.5120), 'CLE': (41.4993, -80.9429), 'DAL': (32.7767, -96.7970),
    'DEN': (39.7392, -104.9903), 'DET': (42.3314, -83.0458), 'GB': (44.5133, -88.0133),
    'HOU': (29.7604, -95.3698), 'IND': (39.7684, -86.1581), 'JAX': (30.3322, -81.6557),
    'KC': (39.0997, -94.5786), 'LAC': (33.9533, -118.3390), 'LA': (34.0522, -118.2437),
    'MIA': (25.7617, -80.1918), 'MIN': (44.9778, -93.2650), 'NE': (42.3601, -71.0589),
    'NO': (29.9511, -90.0715), 'NYG': (40.7128, -74.0060), 'NYJ': (40.7128, -74.0060),
    'OAK': (37.7749, -122.4194), 'PHI': (39.9526, -75.1652), 'PIT': (40.4406, -79.9959),
    'SF': (37.7749, -122.4194), 'SEA': (47.6062, -122.3321), 'TB': (27.9506, -82.4572),
    'TEN': (36.1627, -86.7816), 'WAS': (38.9072, -76.9856), 'SD': (32.7157, -117.1611)
}

# Load Data with Caching
@st.cache_data(show_spinner=False, ttl=3600)
def load_data():
    """Load NFL play-by-play data - tries optimized parquet first, then CSV"""
    
    # Try optimized parquet file first (for cloud deployment - 12.1MB, 48 columns)
    parquet_file = SCRIPT_DIR / "datasets" / "nfl_data_cloud.parquet"
    # Fallback to full CSV (for local development - 667MB)
    csv_file = SCRIPT_DIR / "datasets" / "NFL Play by Play 2009-2018 (v5).csv"
    
    try:
        if parquet_file.exists():
            # Load optimized parquet (already processed and filtered)
            df = pd.read_parquet(parquet_file)
            return df
        elif csv_file.exists():
            # Load full CSV and process
            df = pd.read_csv(csv_file, low_memory=False)
            df['game_date'] = pd.to_datetime(df['game_date'])
            df['year'] = df['game_date'].dt.year
            df = df[(df['year'] >= 2009) & (df['year'] <= 2018)].copy()
            
            # Consolidate SD (San Diego) and LAC (LA Chargers) into LAC
            df['posteam'] = df['posteam'].replace('SD', 'LAC')
            df['defteam'] = df['defteam'].replace('SD', 'LAC')
            
            return df
        else:
            st.error("Dataset file not found. Please ensure either nfl_data_cloud.parquet or the full CSV exists in the datasets folder.")
            st.stop()
            return None
            
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        st.stop()
        return None

@st.cache_data(show_spinner=False, ttl=3600)
def filter_data_cached(df, selected_teams, selected_years):
    """Cache filtered data to avoid reprocessing on every interaction"""
    team_tuple = tuple(sorted(selected_teams))
    year_tuple = tuple(sorted(selected_years))
    
    df_filtered = df[
        (df['posteam'].isin(selected_teams)) & 
        (df['year'].isin(selected_years))
    ].copy()
    
    return df_filtered

@st.cache_data(show_spinner=False, ttl=3600)
def get_aggregated_stats(df_filtered, group_by_cols, agg_dict):
    """Cache aggregated statistics to avoid recalculation"""
    return df_filtered.groupby(list(group_by_cols)).agg(agg_dict).reset_index()

@st.cache_data(show_spinner=False, ttl=3600)
def create_racing_bar_data(df_filtered, selected_teams_tuple, metric_col, group_col, frames_per_year=20):
    """Create racing bar animation data with caching - optimized for speed"""
    selected_teams = list(selected_teams_tuple)  # Convert tuple back to list for processing
    # Calculate data per year
    data_by_year = {}
    years = sorted(df_filtered['year'].unique())
    
    for year in years:
        year_data = df_filtered[df_filtered['year'] == year]
        metric_by_group = {}
        
        for group in selected_teams:
            value = year_data[year_data[group_col] == group][metric_col].sum()
            metric_by_group[group] = value
        
        data_by_year[year] = metric_by_group
    
    # Create animation frames (reduced from 100 to 20 for 5x speedup)
    frames_data = []
    cumulative = {team: 0 for team in selected_teams}
    
    for year in years:
        year_increment = data_by_year[year]
        
        for frame_idx in range(frames_per_year):
            progress = frame_idx / frames_per_year
            current = {team: cumulative[team] + year_increment.get(team, 0) * progress for team in selected_teams}
            
            # Sort and get top 15
            sorted_data = sorted(current.items(), key=lambda x: x[1], reverse=True)[:15]
            
            frames_data.append({
                'year': year,
                'frame': frame_idx,
                'teams': [t[0] for t in sorted_data],
                'values': [t[1] for t in sorted_data],
                'name': f"{year}.{frame_idx}"
            })
        
        # Update cumulative
        for team in selected_teams:
            cumulative[team] += year_increment.get(team, 0)
    
    return frames_data, cumulative

def main():
    # Enhanced Header with NFL Logo and Subtitle
    st.markdown("<div style='text-align: center; margin-bottom: 10px;'>", unsafe_allow_html=True)
    col_logo1, col_title, col_logo2 = st.columns([1, 4, 1])
    with col_logo1:
        try:
            st.image(str(LOGOS_DIR / "nfl_logo.png"), width=120)
        except:
            pass
    with col_title:
        st.markdown("<h1>NFL DECADE ANALYTICS DASHBOARD</h1>", unsafe_allow_html=True)
    with col_logo2:
        try:
            st.image(str(LOGOS_DIR / "nfl_logo.png"), width=120)
        except:
            pass
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Load data with enhanced spinner
    with st.spinner(' Loading NFL Play-by-Play Dataset...'):
        df = load_data()
    
    # Enhanced Introduction Section
    st.markdown("##  ABOUT THIS DASHBOARD")
    
    intro_col1, intro_col2 = st.columns([2, 1])
    with intro_col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%); 
                    padding: 25px; border-radius: 15px; border-left: 5px solid #FFD700; 
                    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4); margin-bottom: 20px;'>
            <p style='color: #FFFFFF; font-size: 1.1rem; line-height: 1.8; font-family: Roboto;'>
                <strong style='color: #FFD700;'>American Football</strong> is one of the most popular sports in the United States. 
                The <strong style='color: #00D9FF;'>NFL (National Football League)</strong> captures extensive data on virtually 
                every play in each game. This dashboard analyzes <strong style='color: #FFD700;'>a complete decade</strong> 
                of NFL action, providing deep insights into team and player performance.
            </p>
            <p style='color: #FFFFFF; font-size: 1.1rem; line-height: 1.8; font-family: Roboto; margin-top: 15px;'>
                The game features two teams competing to score by advancing the ball into the opposing team's end zone. 
                Teams are divided into <strong style='color: #00D9FF;'>offense and defense</strong>, with specialized 
                positions including Quarterbacks, Wide Receivers, and Running Backs. Each season consists of 17 regular 
                games, with the top teams advancing to the playoffs.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with intro_col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 165, 0, 0.1) 100%); 
                    padding: 25px; border-radius: 15px; border: 2px solid #FFD700; 
                    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4); margin-bottom: 20px;'>
            <h3 style='color: #FFD700; text-align: center; margin-bottom: 20px; font-size: 1.5rem;'> SCORING SYSTEM</h3>
            <ul style='color: #FFFFFF; font-size: 1.05rem; line-height: 2; list-style: none; padding: 0;'>
                <li> <strong style='color: #FFD700;'>Touchdown:</strong> 6 points + 1 extra = <strong>7 pts</strong></li>
                <li> <strong style='color: #00D9FF;'>Field Goal:</strong> <strong>3 points</strong></li>
                <li> <strong style='color: #FF6B6B;'>Safety:</strong> <strong>2 points</strong></li>
                <li> <strong style='color: #9D4EDD;'>Game:</strong> 4 quarters  15 min</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%); 
                padding: 20px; border-radius: 12px; border-left: 5px solid #00D9FF; margin: 20px 0;'>
        <p style='color: #FFFFFF; font-size: 1.1rem; line-height: 1.8; font-family: Roboto; margin: 0;'>
            <strong style='color: #00D9FF;'> Dashboard Objectives:</strong> Explore team performance trends, 
            analyze elite player statistics (QBs, RBs, WRs), examine defensive dominance, and discover how 
            the NFL evolved throughout the decade. <strong style='color: #FFD700;'>Interactive filters</strong> 
            allow you to focus on your favorite teams and compare player performances across seasons.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Team logo mapping (simplified names matching file names)
    team_logo_map = {
        'ARI': 'arizona.png', 'ATL': 'falcons.png', 'BAL': 'ravens.png',
        'BUF': 'bills.png', 'CAR': 'carolina.png', 'CHI': 'chicago.png',
        'CIN': 'bengals.png', 'CLE': 'browns.png', 'DAL': 'dallas.png',
        'DEN': 'denver.png', 'DET': 'detroit.png', 'GB': 'greenbay.png',
        'HOU': 'houston.png', 'IND': 'indianapolis.png', 'JAX': 'jacksonville.png',
        'KC': 'kansascity.png', 'LAC': 'chargers.png', 'LA': 'rams.png',
        'MIA': 'miami.png', 'MIN': 'vikings.png', 'NE': 'patriots.png',
        'NO': 'newOrleans.png', 'NYG': 'giant.png', 'NYJ': 'jets.png',
        'OAK': 'raiders.png', 'PHI': 'eagles.png', 'PIT': 'steelers.png',
        'SF': 'sanfrancisco.png', 'SEA': 'seattle.png', 'TB': 'tampabay.png',
        'TEN': 'titans.png', 'WAS': 'washington.png', 'SD': 'rams.png'
    }
    
    # Display team logos in grid
    logo_cols = st.columns(8)
    teams_in_data = sorted([t for t in df['posteam'].unique() if pd.notna(t) and t in NFL_COLORS])
    
    for idx, team in enumerate(teams_in_data[:32]):  # Show up to 32 teams
        col_idx = idx % 8
        with logo_cols[col_idx]:
            if team in team_logo_map:
                try:
                    st.image(str(LOGOS_DIR / team_logo_map[team]), width=80, caption=NFL_NAMES.get(team, team))
                except:
                    st.write(NFL_NAMES.get(team, team))
            else:
                st.markdown(f"**{team}**")
    
    st.markdown("---")

    # Enhanced Sidebar Filters
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); 
                border-radius: 15px; margin-bottom: 20px;'>
        <h2 style='color: #000; margin: 0; font-size: 1.8rem; font-family: Bebas Neue;'>FILTERS</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Team Quick Search
    st.sidebar.markdown("###  Quick Team Search")
    team_search = st.sidebar.text_input(
        "Team Code",
        value="",
        help="Enter a team code (e.g., NE, DAL, GB) for focused analysis",
        placeholder="e.g., NE, DAL, GB..."
    ).upper().strip()
    
    # Year filter with enhanced styling
    years = sorted(df['year'].unique())
    st.sidebar.markdown("###  Season Years")
    selected_years = st.sidebar.multiselect(
        "Select Years",
        options=years,
        default=years,
        help="Filter data by season"
    )
    
    # Team filter (conditional based on text input)
    teams = sorted([t for t in df['posteam'].unique() if pd.notna(t) and t in NFL_COLORS])
    st.sidebar.markdown("###  Select Teams")
    if team_search and team_search in teams:
        selected_teams = [team_search]
        st.sidebar.success(f" {NFL_NAMES.get(team_search, team_search)}")
    else:
        selected_teams = st.sidebar.multiselect(
            "Teams to Analyze",
            options=teams,
            default=teams,
            format_func=lambda x: f"{x} - {NFL_NAMES.get(x, x)}",
            help="Select one or multiple teams"
        )
        if team_search:
            st.sidebar.error(f" '{team_search}' not found")
    
    # Performance Mode Toggle
    st.sidebar.markdown("---")
    st.sidebar.markdown("###  Performance Settings")
    performance_mode = st.sidebar.radio(
        "Rendering Speed",
        options=["⚡ Fast (Recommended)", "🎨 High Quality"],
        index=0,
        help="Fast mode reduces animation frames for 5x faster loading. Quality mode uses more frames for smoother animations."
    )
    frames_per_year = 20 if "Fast" in performance_mode else 50
    st.sidebar.caption(f"Using {frames_per_year} frames/year for racing bars")
    
    # Apply filters with caching
    df_filtered = filter_data_cached(df, tuple(sorted(selected_teams)), tuple(sorted(selected_years)))
    
    # Enhanced Global KPIs Section
    st.markdown("##  KEY PERFORMANCE INDICATORS")
    st.markdown("""
    <div style='background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; border-left: 3px solid #FFD700; margin-bottom: 20px;'>
        <p style='color: #FFFFFF; font-size: 0.95rem; line-height: 1.5; margin: 0;'>
            <strong style='color: #FFD700;'> At-A-Glance Metrics:</strong> These key numbers summarize the filtered dataset's scope and intensity. 
            Total plays show game volume, yards measure offensive output, touchdowns reveal scoring prowess, and EPA quantifies strategic value. Use filters to explore specific teams or time periods.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi4, kpi5, kpi6 = st.columns(3)
    
    with kpi1:
        st.metric(" Total Plays", f"{len(df_filtered):,}", 
                 help="Total number of offensive plays executed")
    with kpi2:
        st.metric(" Games Played", f"{df_filtered['game_id'].nunique():,}",
                 help="Total regular season games")
    with kpi3:
        st.metric(" Touchdowns", f"{int(df_filtered['touchdown'].sum()):,}",
                 help="Total touchdowns scored")
    with kpi4:
        st.metric(" Total Yards", f"{int(df_filtered['yards_gained'].sum()):,}",
                 help="Cumulative yards gained")
    with kpi5:
        st.metric(" Teams", f"{df_filtered['posteam'].nunique()}",
                 help="Number of teams in analysis")
    with kpi6:
        st.metric(" Seasons", f"{df_filtered['year'].nunique()}",
                 help="Years covered in dataset")
    
    # Enhanced Data Insights
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%); 
                padding: 25px; border-radius: 15px; border-left: 5px solid #00D9FF; 
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4); margin: 25px 0;'>
        <h4 style='color: #FFD700; margin-top: 0;'> Dataset Insights</h4>
        <p style='color: #FFFFFF; font-size: 1.05rem; line-height: 1.8; font-family: Roboto;'>
            This comprehensive dataset contains <strong style='color: #FFD700;'>417,172 plays</strong> across 
            <strong style='color: #00D9FF;'>2,524 regular season games</strong> spanning a complete decade (2009-2018). 
            With an average of <strong style='color: #FFD700;'>~4.9 touchdowns per game</strong> and over 
            <strong style='color: #00D9FF;'>1.68 million total yards</strong>, this data reveals the explosive 
            offensive nature of modern NFL football.
        </p>
        <p style='color: #FFFFFF; font-size: 1.05rem; line-height: 1.8; font-family: Roboto; margin-top: 15px;'>
            Each season features 17 weeks with approximately 15 games per week, showcasing the performances of 32 teams 
            competing for playoff positions and ultimately, the Super Bowl championship.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.warning(" **Data Note:** This dataset focuses on offensive statistics. Defensive and special teams touchdowns are not included in the touchdown counts, which may result in slight differences from official NFL statistics.")
    st.markdown("---")
    
    # ENHANCED GEOGRAPHIC MAP SECTION
    st.markdown("##  NFL TEAMS GEOGRAPHIC DISTRIBUTION")
    st.markdown("<p style='color: #00D9FF; font-size: 1.15rem; margin-bottom: 20px;'>Interactive map showing team locations and performance metrics across the United States</p>", unsafe_allow_html=True)

    st.info(" **Map Features:** Hover over markers to see detailed team statistics. Marker size reflects touchdown performance. Team locations are based on stadium coordinates.")
    

    
    # Create GeoDataFrame for map
    teams_data = []
    for team, coords in NFL_LOCATIONS.items():
        if team in NFL_COLORS and team in selected_teams and team != 'SD':  # Skip SD as it's now LAC
            team_stats = df_filtered[df_filtered['posteam'] == team].agg({
                'touchdown': 'sum',
                'yards_gained': 'sum',
                'play_id': 'count'
            })
            teams_data.append({
                'team': team,
                'name': NFL_NAMES[team],
                'geometry': Point(coords[1], coords[0]),
                'color': NFL_COLORS[team],
                'lat': coords[0],
                'lon': coords[1],
                'touchdowns': int(team_stats['touchdown']) if team_stats['touchdown'] > 0 else 0,
                'yards': int(team_stats['yards_gained']) if team_stats['yards_gained'] > 0 else 0,
                'plays': int(team_stats['play_id']) if team_stats['play_id'] > 0 else 0
            })
    
    if teams_data:
        gdf = gpd.GeoDataFrame(teams_data, crs='EPSG:4326')
        
        # Create enhanced map with Plotly
        fig_map = go.Figure()
        
        # Add glowing markers with team colors
        for idx, row in gdf.iterrows():
            # Main marker with glow effect
            fig_map.add_trace(go.Scattergeo(
                lon=[row['lon']],
                lat=[row['lat']],
                mode='markers',
                marker=dict(
                    size=35 + (row['touchdowns'] / 30) if row['touchdowns'] > 0 else 30,
                    color=row['color'],
                    line=dict(width=5, color='white'),
                    symbol='circle',
                    opacity=0.95
                ),
                name=row['name'],
                showlegend=False,
                hovertemplate=f"<b style='font-size:16px'>{row['name']}</b><br>" +
                             f"<b style='color:#FFD700'> {row['team']}</b><br><br>" +
                             f"<b> Touchdowns:</b> {row['touchdowns']:,}<br>" +
                             f"<b> Total Yards:</b> {row['yards']:,}<br>" +
                             f"<b> Total Plays:</b> {row['plays']:,}<br>" +
                             f"<b> Avg Yards/Play:</b> {row['yards']/row['plays']:.1f}<extra></extra>"
            ))
            
            # Outer glow ring
            fig_map.add_trace(go.Scattergeo(
                lon=[row['lon']],
                lat=[row['lat']],
                mode='markers',
                marker=dict(
                    size=45 + (row['touchdowns'] / 25) if row['touchdowns'] > 0 else 40,
                    color=row['color'],
                    line=dict(width=0),
                    symbol='circle',
                    opacity=0.3
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Add team logo as text annotation
            logo_file = team_logo_map.get(row['team'], None)
            if logo_file:
                fig_map.add_trace(go.Scattergeo(
                    lon=[row['lon']],
                    lat=[row['lat']],
                    mode='text',
                    text=f"<b>{row['team']}</b>",
                    textfont=dict(size=11, color='white', family='Arial Black'),
                    textposition='top center',
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        # Enhanced layout with better styling
        fig_map.update_layout(
            title=dict(
                text='<b> NFL TEAMS GEOGRAPHIC DISTRIBUTION - PERFORMANCE HEAT MAP </b>',
                font=dict(size=28, color='white', family='Arial Black'),
                x=0.5,
                y=0.97,
                xanchor='center'
            ),
            geo=dict(
                scope='usa',
                projection_type='albers usa',
                showland=True,
                landcolor='#0f1419',
                coastlinecolor='#FFD700',
                coastlinewidth=3,
                showlakes=True,
                lakecolor='#050810',
                showcountries=True,
                countrycolor='#FFD700',
                bgcolor='#050810',
                showsubunits=True,
                subunitcolor='#3a4a5a',
                subunitwidth=1.5
            ),
            height=700,
            paper_bgcolor='#0a0a0f',
            font=dict(color='white'),
            showlegend=False,
            margin=dict(l=0, r=0, t=80, b=20)
        )
        
        st.plotly_chart(fig_map, width="stretch")
    
    st.markdown("---")
    
    # Add performance tip
    st.info("💡 **Performance Tip:** Each tab loads data on-demand. Switch between tabs to explore different analyses.")
    
    # MAIN TABS
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        " TEAM PERFORMANCE",
        " QUARTERBACK STATS",
        " RUNNING BACKS",
        " WIDE RECEIVERS",
        " DEFENSE ANALYSIS",
        " SEABORN ANALYSIS",
        " GAME HIGHLIGHTS"
    ])
    
    # TAB 1: TEAM PERFORMANCE WITH RACING BAR
    with tab1:
        with st.spinner('Loading team performance data...'):
            st.markdown("##  TEAM PERFORMANCE ANALYSIS")
            
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 46, 0.8) 0%, rgba(22, 33, 62, 0.8) 100%); 
                        padding: 20px; border-radius: 12px; border-left: 4px solid #FFD700; margin-bottom: 25px;'>
                <p style='color: #FFFFFF; font-size: 1.05rem; line-height: 1.6; margin: 0;'>
                    <strong style='color: #FFD700;'> The Decade's Story:</strong> Which teams dominated the 2010s? 
                    This animated racing bar reveals how franchises accumulated touchdowns season by season, showing 
                    sustained excellence versus flash-in-the-pan success. Watch dynasties rise and underdogs climb the ranks.
                </p>
        </div>
        """, unsafe_allow_html=True)
        
        # RACING BAR CHART - Most Winning Teams
        st.markdown("###  Racing Bar: Team Performance Evolution (2009-2018)")
        st.caption(" Press Play to see teams compete for touchdown supremacy across 10 seasons. Larger bars = more offensive firepower.")
        
        # Use cached racing bar data (5x faster than before)
        with st.spinner('Generating racing bar animation...'):
            frames_data, cumulative_wins = create_racing_bar_data(
                df_filtered, 
                tuple(sorted(selected_teams)),  # Pass as tuple for caching
                'touchdown', 
                'posteam',
                frames_per_year=frames_per_year  # Uses performance setting
            )
            
            # Create frames for Plotly
            frames = []
            for frame_info in frames_data:
                teams_list = frame_info['teams']
                wins_list = frame_info['values']
                colors_list = [NFL_COLORS.get(t, '#FFD700') for t in teams_list]
                names_list = [NFL_NAMES.get(t, t) for t in teams_list]
                
                frames.append(go.Frame(
                    data=[go.Bar(
                        y=names_list,
                        x=wins_list,
                        orientation='h',
                        marker=dict(color=colors_list, line=dict(color='white', width=2)),
                        text=[f"{int(w)}" for w in wins_list],
                        textposition='outside',
                        textfont=dict(size=12, color='white', family='Arial Black')
                    )],
                    name=frame_info['name'],
                    layout=go.Layout(title_text=f"<b>Cumulative Touchdowns through {frame_info['year']}</b>")
                ))
        
        # Initial figure
        initial_sorted = sorted(cumulative_wins.items(), key=lambda x: x[1], reverse=True)[:15]
        initial_teams = [t[0] for t in initial_sorted]
        initial_wins = [t[1] for t in initial_sorted]
        initial_colors = [NFL_COLORS.get(t, '#FFD700') for t in initial_teams]
        initial_names = [NFL_NAMES.get(t, t) for t in initial_teams]
        
        fig_race_teams = go.Figure(
            data=[go.Bar(
                y=initial_names,
                x=initial_wins,
                orientation='h',
                marker=dict(color=initial_colors, line=dict(color='white', width=2))
            )],
            frames=frames
        )
        
        fig_race_teams.update_layout(
            title=dict(text='<b>RACING BAR: TEAM PERFORMANCE EVOLUTION</b>', font=dict(size=24, color='white')),
            xaxis=dict(title='Cumulative Touchdowns', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white'), range=[0, max(initial_wins)*1.1]),
            yaxis=dict(tickfont=dict(color='white', size=11)),
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            height=700,
            margin=dict(l=200, r=50, t=100, b=150),
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {'label': 'Play', 'method': 'animate',
                     'args': [None, {'frame': {'duration': 30, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 20, 'easing': 'linear'}}]},
                    {'label': 'Pause', 'method': 'animate',
                     'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}]}
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 10},
                'x': 0.85, 'xanchor': 'left', 'y': 1.15, 'yanchor': 'top',
                'bgcolor': '#1a1a2e',
                'bordercolor': '#FFD700',
                'borderwidth': 2,
                'font': {'size': 16, 'color': '#FFD700'}
            }],
            sliders=[{
                'active': 0,
                'yanchor': 'top',
                'y': -0.15,
                'xanchor': 'left',
                'currentvalue': {
                    'prefix': 'Year: ',
                    'visible': True,
                    'xanchor': 'right',
                    'font': {'size': 16, 'color': '#FFD700'}
                },
                'steps': [{'args': [[f.name], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}],
                          'label': f.name.split('.')[0], 'method': 'animate'} for i, f in enumerate(frames) if i % 100 == 0],
                'x': 0.0, 'len': 1.0
            }]
        )
        
        st.plotly_chart(fig_race_teams, width='stretch')
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # TD Distribution with Ridgeplot-style KDE
            st.markdown("####  Team Scoring Patterns - Touchdown Distribution")
            
            td_by_team_year = df_filtered.groupby(['posteam', 'year'])['touchdown'].sum().reset_index()
            top_td_teams = df_filtered.groupby('posteam')['touchdown'].sum().nlargest(8).index
            td_filtered = td_by_team_year[td_by_team_year['posteam'].isin(top_td_teams)]
            
            # Create ridge-like plot with KDE
            fig_td_seaborn, ax = plt.subplots(figsize=(13, 9))
            fig_td_seaborn.patch.set_facecolor('#16213e')
            
            # Sort teams by median TD for better visualization
            team_medians = td_filtered.groupby('posteam')['touchdown'].median().sort_values(ascending=False)
            sorted_teams = team_medians.index
            
            # Create overlapping KDE plots
            y_offset = 0
            for i, team in enumerate(sorted_teams):
                team_data = td_filtered[td_filtered['posteam'] == team]['touchdown']
                color = NFL_COLORS.get(team, '#FFD700')
                
                # KDE plot
                sns.kdeplot(data=team_data, ax=ax, color=color, fill=True, 
                           alpha=0.7, linewidth=3, label=f"{NFL_NAMES.get(team, team)[:12]}")
                
                # Add individual points as rug plot
                y_vals = np.ones(len(team_data)) * (i * 0.05 - 0.2)
                ax.scatter(team_data.values, y_vals, color=color, s=60, 
                          alpha=0.6, edgecolors='white', linewidth=1.5, zorder=10)
            
            ax.set_title('TOP 8 TEAMS - TOUCHDOWN SCORING PATTERNS (2009-2018)', 
                        fontsize=17, color='#FFD700', fontweight='bold', pad=20)
            ax.set_xlabel('Touchdowns per Season', fontsize=14, color='white', fontweight='bold')
            ax.set_ylabel('Density', fontsize=14, color='white', fontweight='bold')
            ax.set_facecolor('#1a1a2e')
            ax.tick_params(colors='white', labelsize=11)
            ax.grid(True, alpha=0.3, color='white', linestyle='--', axis='x')
            
            # Enhanced legend
            legend = ax.legend(loc='upper right', facecolor='#1a1a2e', 
                             edgecolor='#FFD700', fontsize=10, framealpha=0.95,
                             title='Teams', title_fontsize=11)
            plt.setp(legend.get_texts(), color='white')
            plt.setp(legend.get_title(), color='#FFD700', fontweight='bold')
            
            # Add statistics annotation
            overall_mean = td_filtered['touchdown'].mean()
            overall_median = td_filtered['touchdown'].median()
            ax.axvline(x=overall_mean, color='#FF6B6B', linestyle='--', linewidth=3, alpha=0.8)
            ax.axvline(x=overall_median, color='#00D9FF', linestyle=':', linewidth=3, alpha=0.8)
            ax.text(overall_mean, ax.get_ylim()[1]*0.95, f'Mean: {overall_mean:.1f}', 
                   ha='center', va='top', color='#FF6B6B', fontweight='bold', fontsize=11,
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e', edgecolor='#FF6B6B', linewidth=2))
            ax.text(overall_median, ax.get_ylim()[1]*0.85, f'Median: {overall_median:.1f}', 
                   ha='center', va='top', color='#00D9FF', fontweight='bold', fontsize=11,
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e', edgecolor='#00D9FF', linewidth=2))
            
            plt.tight_layout()
            st.pyplot(fig_td_seaborn)
            plt.close()
        
        with col2:
            st.caption(" **EPA (Expected Points Added):** Advanced metric measuring play efficiency. Positive EPA = offense gained more points than expected.")
            # EPA by Team
            team_epa = df_filtered.groupby('posteam')['epa'].mean().nlargest(15)
            fig_epa = go.Figure()
            fig_epa.add_trace(go.Bar(
                x=[NFL_NAMES.get(t, t) for t in team_epa.index],
                y=team_epa.values,
                marker=dict(
                    color=[NFL_COLORS.get(t, '#00D9FF') for t in team_epa.index],
                    line=dict(color='white', width=2)
                ),
                text=[f"{v:.3f}" for v in team_epa.values],
                textposition='outside',
                textfont=dict(size=12, color='white', family='Arial Black')
            ))
            fig_epa.update_layout(
                title=dict(text='<b>TOP 15 TEAMS - AVG EPA</b>', font=dict(size=20, color='white', family='Arial Black')),
                xaxis=dict(tickfont=dict(color='white', size=10), tickangle=-45),
                yaxis=dict(title='Average EPA', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
                plot_bgcolor='#1a1a2e',
                paper_bgcolor='#16213e',
                font=dict(color='white'),
                height=500
            )
            st.plotly_chart(fig_epa, width="stretch")
        
        # Yards Evolution Over Time
        st.markdown("###  Yards Evolution by Year")
        st.caption(" **Decade Trajectories:** Follow how top teams' total offensive output changed year-by-year. Upward trends show program improvement, while sharp drops reveal injury impacts or roster changes.")
        yearly_yards = df_filtered.groupby(['year', 'posteam'])['yards_gained'].sum().reset_index()
        top_teams = df_filtered.groupby('posteam')['yards_gained'].sum().nlargest(10).index
        yearly_yards_top = yearly_yards[yearly_yards['posteam'].isin(top_teams)]
        
        fig_evolution = go.Figure()
        for team in top_teams:
            team_data = yearly_yards_top[yearly_yards_top['posteam'] == team]
            fig_evolution.add_trace(go.Scatter(
                x=team_data['year'],
                y=team_data['yards_gained'],
                mode='lines+markers',
                name=NFL_NAMES.get(team, team),
                line=dict(color=NFL_COLORS.get(team, '#FFD700'), width=3),
                marker=dict(size=10, line=dict(color='white', width=2))
            ))
        
        fig_evolution.update_layout(
            title=dict(text='<b>TOTAL YARDS EVOLUTION - TOP 10 TEAMS</b>', font=dict(size=22, color='white', family='Arial Black')),
            xaxis=dict(title='Year', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
            yaxis=dict(title='Total Yards', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            height=600,
            hovermode='x unified',
            legend=dict(bgcolor='#1a1a2e', bordercolor='#FFD700', borderwidth=2)
        )
        st.plotly_chart(fig_evolution, width="stretch")
    
    # TAB 2: QUARTERBACK STATS WITH RACING BAR
    with tab2:
        st.markdown("##  QUARTERBACK ANALYSIS")
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(26, 26, 46, 0.8) 0%, rgba(22, 33, 62, 0.8) 100%); 
                    padding: 20px; border-radius: 12px; border-left: 4px solid #4ECDC4; margin-bottom: 25px;'>
            <p style='color: #FFFFFF; font-size: 1.05rem; line-height: 1.6; margin: 0;'>
                <strong style='color: #4ECDC4;'> The Signal Callers:</strong> Quarterbacks define offenses and franchises. 
                From Peyton Manning's precision to Tom Brady's clutch performances, this section chronicles who threw for 
                the most yards, touchdowns, and efficiency. Watch legends compete and new stars emerge.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        qb_data = df_filtered[df_filtered['passer_player_name'].notna()].copy()
        
        # RACING BAR CHART - Top QBs by Passing Yards
        st.markdown("###  Racing Bar: Top Quarterbacks by Passing Yards")
        st.caption(" Animated timeline showing career passing yard accumulation. Team colors indicate franchise affiliations.")
        
        # Calculate cumulative yards per QB per year with smooth transitions
        qb_frames = []
        qb_cumulative = {}
        frames_per_year = 100
        
        # Get team for each QB to apply team colors
        qb_team_map = {}
        for qb in qb_data['passer_player_name'].unique():
            if pd.notna(qb):
                team = qb_data[qb_data['passer_player_name'] == qb]['posteam'].mode()
                qb_team_map[qb] = team.values[0] if len(team) > 0 else 'NFL'
        
        for year in range(2009, 2019):
            year_qbs = qb_data[qb_data['year'] == year].groupby('passer_player_name')['yards_gained'].sum().to_dict()
            
            for frame_idx in range(frames_per_year):
                progress = frame_idx / frames_per_year
                current_qb_vals = {}
                
                for qb in set(list(qb_cumulative.keys()) + list(year_qbs.keys())):
                    base = qb_cumulative.get(qb, 0)
                    increment = year_qbs.get(qb, 0) * progress
                    current_qb_vals[qb] = base + increment
                
                sorted_qbs = sorted(current_qb_vals.items(), key=lambda x: x[1], reverse=True)[:15]
                qb_names = [q[0] for q in sorted_qbs]
                qb_yards = [q[1] for q in sorted_qbs]
                qb_colors = [NFL_COLORS.get(qb_team_map.get(q[0], 'NFL'), '#4ECDC4') for q in sorted_qbs]
                
                qb_frames.append(go.Frame(
                    data=[go.Bar(
                        y=qb_names,
                        x=qb_yards,
                        orientation='h',
                        marker=dict(color=qb_colors, line=dict(color='white', width=2)),
                        text=[f"{int(y):,}" for y in qb_yards],
                        textposition='outside',
                        textfont=dict(size=11, color='white', family='Arial Black')
                    )],
                    name=f"{year}.{frame_idx}",
                    layout=go.Layout(title_text=f"<b>QB Passing Yards through {year}</b>")
                ))
            
            for qb, yards in year_qbs.items():
                qb_cumulative[qb] = qb_cumulative.get(qb, 0) + yards
        
        # Initial QB figure
        initial_qb_data = qb_data[qb_data['year'] <= 2009].groupby('passer_player_name')['yards_gained'].sum().nlargest(15)
        initial_qb_colors = [NFL_COLORS.get(qb_team_map.get(qb, 'NFL'), '#4ECDC4') for qb in initial_qb_data.index]
        
        fig_race_qb = go.Figure(
            data=[go.Bar(
                y=initial_qb_data.index,
                x=initial_qb_data.values,
                orientation='h',
                marker=dict(color=initial_qb_colors, line=dict(color='white', width=2))
            )],
            frames=qb_frames
        )
        
        # Calculate max cumulative value to set consistent x-axis range
        max_cumulative_qb = max([sum(qb_data[qb_data['year'] <= year].groupby('passer_player_name')['yards_gained'].sum().nlargest(15).values) for year in range(2009, 2019)])
        
        fig_race_qb.update_layout(
            title=dict(text='<b>RACING BAR: TOP QUARTERBACKS BY PASSING YARDS</b>', font=dict(size=24, color='white')),
            xaxis=dict(title='Cumulative Passing Yards', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white'), range=[0, 55000]),
            yaxis=dict(tickfont=dict(color='white', size=10)),
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            height=700,
            margin=dict(l=200, r=50, t=100, b=150),
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {'label': 'Play', 'method': 'animate',
                     'args': [None, {'frame': {'duration': 30, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 20, 'easing': 'linear'}}]},
                    {'label': 'Pause', 'method': 'animate',
                     'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}]}
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 10},
                'x': 0.85, 'xanchor': 'left', 'y': 1.15, 'yanchor': 'top',
                'bgcolor': '#1a1a2e',
                'bordercolor': '#FFD700',
                'borderwidth': 2,
                'font': {'size': 16, 'color': '#FFD700'}
            }],
            sliders=[{
                'active': 0,
                'yanchor': 'top',
                'y': -0.15,
                'xanchor': 'left',
                'currentvalue': {
                    'prefix': 'Year: ',
                    'visible': True,
                    'xanchor': 'right',
                    'font': {'size': 16, 'color': '#FFD700'}
                },
                'steps': [{'args': [[f.name], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}],
                          'label': f.name.split('.')[0], 'method': 'animate'} for i, f in enumerate(qb_frames) if i % 100 == 0],
                'x': 0.0, 'len': 1.0
            }]
        )
        
        st.plotly_chart(fig_race_qb, width='stretch')
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.caption(" **Cumulative Career Yards:** Total passing yards define QB longevity and production. Each dot represents a quarterback's decade-long output.")
            # QB Passing Yards - Lollipop Chart
            qb_yards = qb_data.groupby('passer_player_name')['yards_gained'].sum().nlargest(15)
            
            # Get team for each QB to apply team colors
            qb_teams = {}
            for qb in qb_yards.index:
                team = qb_data[qb_data['passer_player_name'] == qb]['posteam'].mode()
                qb_teams[qb] = team.values[0] if len(team) > 0 else 'NFL'
            
            fig_qb_yards, ax_qb = plt.subplots(figsize=(10, 9))
            fig_qb_yards.patch.set_facecolor('#16213e')
            
            y_pos = np.arange(len(qb_yards))
            colors_qb = [NFL_COLORS.get(qb_teams.get(qb, 'NFL'), '#4ECDC4') for qb in qb_yards.index]
            
            # Create lollipop stems
            ax_qb.hlines(y=y_pos, xmin=0, xmax=qb_yards.values, color=colors_qb, alpha=0.8, linewidth=4)
            # Create lollipop heads
            ax_qb.scatter(qb_yards.values, y_pos, color=colors_qb, s=250, alpha=0.9, edgecolors='white', linewidth=3, zorder=3)
            
            # Add value labels
            for i, (qb, yards) in enumerate(qb_yards.items()):
                ax_qb.text(yards + 500, i, f"{int(yards):,}", va='center', ha='left',
                          fontsize=11, color='white', fontweight='bold')
                # Add team code
                team = qb_teams.get(qb, 'NFL')
                ax_qb.text(yards * 0.05, i, team, va='center', ha='left',
                          fontsize=9, color='white', fontweight='bold',
                          bbox=dict(boxstyle='round,pad=0.3', facecolor='black', 
                                   edgecolor='white', linewidth=1, alpha=0.7))
            
            ax_qb.set_yticks(y_pos)
            ax_qb.set_yticklabels([qb.split()[-1] for qb in qb_yards.index], fontsize=11, color='white', fontweight='bold')
            ax_qb.set_xlabel('Passing Yards', fontsize=13, color='white', fontweight='bold')
            ax_qb.set_title('TOP 15 QBs - PASSING YARDS', fontsize=18, color='#FFD700', fontweight='bold', pad=15)
            ax_qb.set_facecolor('#1a1a2e')
            ax_qb.tick_params(colors='white', labelsize=10)
            ax_qb.grid(True, alpha=0.3, color='white', linestyle='--', axis='x')
            ax_qb.invert_yaxis()
            
            plt.tight_layout()
            st.pyplot(fig_qb_yards)
            plt.close()
        
        with col2:
            st.caption(" **Touchdown Leaders:** Finding the end zone separates good QBs from great ones. These are the decade's most prolific scorers through the air.")
            # QB Touchdowns with Team Colors
            qb_tds = qb_data.groupby('passer_player_name')['touchdown'].sum().nlargest(15)
            
            # Get team for each QB
            qb_td_teams = {}
            for qb in qb_tds.index:
                team = qb_data[qb_data['passer_player_name'] == qb]['posteam'].mode()
                qb_td_teams[qb] = team.values[0] if len(team) > 0 else 'NFL'
            
            qb_td_colors = [NFL_COLORS.get(qb_td_teams.get(qb, 'NFL'), '#FF6B6B') for qb in qb_tds.index]
            
            fig_qb_tds = go.Figure()
            fig_qb_tds.add_trace(go.Bar(
                y=qb_tds.index,
                x=qb_tds.values,
                orientation='h',
                marker=dict(
                    color=qb_td_colors,
                    line=dict(color='white', width=2)
                ),
                text=qb_tds.values,
                textposition='outside',
                textfont=dict(size=12, color='white', family='Arial Black')
            ))
            fig_qb_tds.update_layout(
                title=dict(text='<b>TOP 15 QBs - TOUCHDOWNS</b>', font=dict(size=20, color='white', family='Arial Black')),
                xaxis=dict(title='Touchdowns', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
                yaxis=dict(tickfont=dict(color='white', size=10)),
                plot_bgcolor='#1a1a2e',
                paper_bgcolor='#16213e',
                font=dict(color='white'),
                height=550
            )
            st.plotly_chart(fig_qb_tds, width="stretch")
        
        # QB Efficiency (EPA)
        st.markdown("###  QB Efficiency - EPA Analysis")
        st.caption(" **Efficiency Matters:** EPA (Expected Points Added) measures game-changing impact per play. Top-right quadrant reveals QBs who combined high volume with elite efficiency.")
        qb_epa = qb_data.groupby('passer_player_name').agg({
            'epa': 'mean',
            'pass_attempt': 'sum'
        }).reset_index()
        qb_epa = qb_epa[qb_epa['pass_attempt'] >= 500].nlargest(20, 'epa')
        
        fig_qb_epa = go.Figure()
        fig_qb_epa.add_trace(go.Scatter(
            x=qb_epa['pass_attempt'],
            y=qb_epa['epa'],
            mode='markers+text',
            marker=dict(
                size=qb_epa['epa'] * 100,
                color=qb_epa['epa'],
                colorscale='RdYlGn',
                showscale=True,
                line=dict(color='white', width=2),
                colorbar=dict(title=dict(text='EPA', font=dict(color='white')))
            ),
            text=qb_epa['passer_player_name'].apply(lambda x: x.split()[-1]),
            textposition='top center',
            textfont=dict(size=10, color='white', family='Arial Black')
        ))
        fig_qb_epa.update_layout(
            title=dict(text='<b>QB EFFICIENCY vs VOLUME (min 500 attempts)</b>', font=dict(size=22, color='white', family='Arial Black')),
            xaxis=dict(title='Pass Attempts', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
            yaxis=dict(title='Average EPA', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            height=600
        )
        st.plotly_chart(fig_qb_epa, width="stretch")
    
    # TAB 3: RUNNING BACKS WITH RACING BAR
    with tab3:
        st.markdown("##  RUNNING BACK ANALYSIS")
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(26, 26, 46, 0.8) 0%, rgba(22, 33, 62, 0.8) 100%); 
                    padding: 20px; border-radius: 12px; border-left: 4px solid #06FFA5; margin-bottom: 25px;'>
            <p style='color: #FFFFFF; font-size: 1.05rem; line-height: 1.6; margin: 0;'>
                <strong style='color: #06FFA5;'> Ground Game Warriors:</strong> Despite the league's evolution toward passing, 
                running backs remain the physical heartbeat of offenses. Watch legends like Adrian Peterson and Marshawn Lynch 
                dominate through power and vision. The racing bars reveal which backs sustained excellence across multiple seasons.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        rb_data = df_filtered[df_filtered['rusher_player_name'].notna()].copy()
        
        # RACING BAR CHART - Top RBs by Rushing Yards
        st.markdown("###  Racing Bar: Top Running Backs by Rushing Yards")
        st.caption(" **Decade of Dominance:** Track how elite backs accumulated career rushing yards. Colors represent team affiliations - notice when stars change jerseys.")
        
        # Calculate cumulative yards per RB per year with smooth transitions
        rb_frames = []
        rb_cumulative = {}
        frames_per_year = 100
        
        # Get team for each RB to apply team colors
        rb_team_map = {}
        for rb in rb_data['rusher_player_name'].unique():
            if pd.notna(rb):
                team = rb_data[rb_data['rusher_player_name'] == rb]['posteam'].mode()
                rb_team_map[rb] = team.values[0] if len(team) > 0 else 'NFL'
        
        for year in range(2009, 2019):
            year_rbs = rb_data[rb_data['year'] == year].groupby('rusher_player_name')['yards_gained'].sum().to_dict()
            
            for frame_idx in range(frames_per_year):
                progress = frame_idx / frames_per_year
                current_rb_vals = {}
                
                for rb in set(list(rb_cumulative.keys()) + list(year_rbs.keys())):
                    base = rb_cumulative.get(rb, 0)
                    increment = year_rbs.get(rb, 0) * progress
                    current_rb_vals[rb] = base + increment
                
                sorted_rbs = sorted(current_rb_vals.items(), key=lambda x: x[1], reverse=True)[:15]
                rb_names = [r[0] for r in sorted_rbs]
                rb_yards = [r[1] for r in sorted_rbs]
                rb_colors = [NFL_COLORS.get(rb_team_map.get(r[0], 'NFL'), '#FF6B6B') for r in sorted_rbs]
                
                rb_frames.append(go.Frame(
                    data=[go.Bar(
                        y=rb_names,
                        x=rb_yards,
                        orientation='h',
                        marker=dict(color=rb_colors, line=dict(color='white', width=2)),
                        text=[f"{int(y):,}" for y in rb_yards],
                        textposition='outside',
                        textfont=dict(size=11, color='white', family='Arial Black')
                    )],
                    name=f"{year}.{frame_idx}",
                    layout=go.Layout(title_text=f"<b>RB Rushing Yards through {year}</b>")
                ))
            
            for rb, yards in year_rbs.items():
                rb_cumulative[rb] = rb_cumulative.get(rb, 0) + yards
        
        # Initial RB figure
        initial_rb_data = rb_data[rb_data['year'] <= 2009].groupby('rusher_player_name')['yards_gained'].sum().nlargest(15)
        initial_rb_colors = [NFL_COLORS.get(rb_team_map.get(rb, 'NFL'), '#FF6B6B') for rb in initial_rb_data.index]
        
        fig_race_rb = go.Figure(
            data=[go.Bar(
                y=initial_rb_data.index,
                x=initial_rb_data.values,
                orientation='h',
                marker=dict(color=initial_rb_colors, line=dict(color='white', width=2))
            )],
            frames=rb_frames
        )
        
        fig_race_rb.update_layout(
            title=dict(text='<b>RACING BAR: TOP RUNNING BACKS BY RUSHING YARDS</b>', font=dict(size=24, color='white')),
            xaxis=dict(title='Cumulative Rushing Yards', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white'), range=[0, 12000]),
            yaxis=dict(tickfont=dict(color='white', size=10)),
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            height=700,
            margin=dict(l=200, r=50, t=100, b=150),
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {'label': 'Play', 'method': 'animate',
                     'args': [None, {'frame': {'duration': 30, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 20, 'easing': 'linear'}}]},
                    {'label': 'Pause', 'method': 'animate',
                     'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}]}
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 10},
                'x': 0.85, 'xanchor': 'left', 'y': 1.15, 'yanchor': 'top',
                'bgcolor': '#1a1a2e',
                'bordercolor': '#FFD700',
                'borderwidth': 2,
                'font': {'size': 16, 'color': '#FFD700'}
            }],
            sliders=[{
                'active': 0,
                'yanchor': 'top',
                'y': -0.15,
                'xanchor': 'left',
                'currentvalue': {
                    'prefix': 'Year: ',
                    'visible': True,
                    'xanchor': 'right',
                    'font': {'size': 16, 'color': '#FFD700'}
                },
                'steps': [{'args': [[f.name], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}],
                          'label': f.name.split('.')[0], 'method': 'animate'} for i, f in enumerate(rb_frames) if i % 100 == 0],
                'x': 0.0, 'len': 1.0
            }]
        )
        
        st.plotly_chart(fig_race_rb, width='stretch')
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.caption(" **Workhorses of the Decade:** These 15 backs carried their teams on their shoulders. The lollipop stems show the massive yardage gaps between elite and great backs.")
            # Top RBs by Rushing Yards - Lollipop Chart
            rb_yards = rb_data.groupby('rusher_player_name')['yards_gained'].sum().nlargest(15)
            
            # Get team for each RB to apply team colors
            rb_teams = {}
            for rb in rb_yards.index:
                team = rb_data[rb_data['rusher_player_name'] == rb]['posteam'].mode()
                rb_teams[rb] = team.values[0] if len(team) > 0 else 'NFL'
            
            fig_rb_yards, ax_rb = plt.subplots(figsize=(10, 9))
            fig_rb_yards.patch.set_facecolor('#16213e')
            
            y_pos = np.arange(len(rb_yards))
            colors_rb = [NFL_COLORS.get(rb_teams.get(rb, 'NFL'), '#FF6B6B') for rb in rb_yards.index]
            
            # Create lollipop stems
            ax_rb.hlines(y=y_pos, xmin=0, xmax=rb_yards.values, color=colors_rb, alpha=0.8, linewidth=4)
            # Create lollipop heads
            ax_rb.scatter(rb_yards.values, y_pos, color=colors_rb, s=250, alpha=0.9, edgecolors='white', linewidth=3, zorder=3)
            
            # Add value labels
            for i, (rb, yards) in enumerate(rb_yards.items()):
                ax_rb.text(yards + 200, i, f"{int(yards):,}", va='center', ha='left',
                          fontsize=11, color='white', fontweight='bold')
                # Add team code
                team = rb_teams.get(rb, 'NFL')
                ax_rb.text(yards * 0.05, i, team, va='center', ha='left',
                          fontsize=9, color='white', fontweight='bold',
                          bbox=dict(boxstyle='round,pad=0.3', facecolor='black', 
                                   edgecolor='white', linewidth=1, alpha=0.7))
            
            ax_rb.set_yticks(y_pos)
            ax_rb.set_yticklabels([rb.split()[-1] for rb in rb_yards.index], fontsize=11, color='white', fontweight='bold')
            ax_rb.set_xlabel('Rushing Yards', fontsize=13, color='white', fontweight='bold')
            ax_rb.set_title('TOP 15 RBs - RUSHING YARDS', fontsize=18, color='#FFD700', fontweight='bold', pad=15)
            ax_rb.set_facecolor('#1a1a2e')
            ax_rb.tick_params(colors='white', labelsize=10)
            ax_rb.grid(True, alpha=0.3, color='white', linestyle='--', axis='x')
            ax_rb.invert_yaxis()
            
            plt.tight_layout()
            st.pyplot(fig_rb_yards)
            plt.close()
        
        with col2:
            st.caption(" **Red Zone Beasts:** When teams needed those critical yards near the goal line, these backs delivered. TD totals reveal who was most trusted in scoring position.")
            # RB Touchdowns with Team Colors
            rb_tds = rb_data.groupby('rusher_player_name')['touchdown'].sum().nlargest(15)
            
            # Get team for each RB
            rb_td_teams = {}
            for rb in rb_tds.index:
                team = rb_data[rb_data['rusher_player_name'] == rb]['posteam'].mode()
                rb_td_teams[rb] = team.values[0] if len(team) > 0 else 'NFL'
            
            rb_td_colors = [NFL_COLORS.get(rb_td_teams.get(rb, 'NFL'), '#4ECDC4') for rb in rb_tds.index]
            
            fig_rb_tds = go.Figure()
            fig_rb_tds.add_trace(go.Bar(
                x=[r for r in rb_tds.index],
                y=rb_tds.values,
                marker=dict(
                    color=rb_td_colors,
                    line=dict(color='white', width=2)
                ),
                text=rb_tds.values,
                textposition='outside',
                textfont=dict(size=12, color='white', family='Arial Black')
            ))
            fig_rb_tds.update_layout(
                title=dict(text='<b>TOP 15 RBs - TOUCHDOWNS</b>', font=dict(size=20, color='white', family='Arial Black')),
                xaxis=dict(tickfont=dict(color='white', size=9), tickangle=-45),
                yaxis=dict(title='Touchdowns', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
                plot_bgcolor='#1a1a2e',
                paper_bgcolor='#16213e',
                font=dict(color='white'),
                height=550
            )
            st.plotly_chart(fig_rb_tds, width="stretch")
        
        # RB Yards per Carry
        st.markdown("###  Yards per Carry Analysis")
        rb_ypc = rb_data.groupby('rusher_player_name').agg({
            'yards_gained': ['sum', 'mean'],
            'rush_attempt': 'sum'
        }).reset_index()
        rb_ypc.columns = ['player', 'total_yards', 'ypc', 'attempts']
        rb_ypc = rb_ypc[rb_ypc['attempts'] >= 300].nlargest(20, 'ypc')
        
        fig_rb_ypc = go.Figure()
        fig_rb_ypc.add_trace(go.Scatter(
            x=rb_ypc['attempts'],
            y=rb_ypc['ypc'],
            mode='markers+text',
            marker=dict(
                size=rb_ypc['total_yards'] / 100,
                color=rb_ypc['ypc'],
                colorscale='Viridis',
                showscale=True,
                line=dict(color='white', width=2),
                colorbar=dict(title=dict(text='YPC', font=dict(color='white')))
            ),
            text=rb_ypc['player'].apply(lambda x: x.split()[-1]),
            textposition='top center',
            textfont=dict(size=10, color='white', family='Arial Black')
        ))
        fig_rb_ypc.update_layout(
            title=dict(text='<b>RB EFFICIENCY - YARDS PER CARRY (min 300 attempts)</b>', font=dict(size=22, color='white', family='Arial Black')),
            xaxis=dict(title='Rush Attempts', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
            yaxis=dict(title='Yards per Carry', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            height=600
        )
        st.plotly_chart(fig_rb_ypc, width="stretch")
    
    # TAB 4: WIDE RECEIVERS
    with tab4:
        st.markdown("##  WIDE RECEIVER ANALYSIS")
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(26, 26, 46, 0.8) 0%, rgba(22, 33, 62, 0.8) 100%); 
                    padding: 20px; border-radius: 12px; border-left: 4px solid #FF6B35; margin-bottom: 25px;'>
            <p style='color: #FFFFFF; font-size: 1.05rem; line-height: 1.6; margin: 0;'>
                <strong style='color: #FF6B35;'> Playmakers & Game-Breakers:</strong> Wide receivers are the artists of football - 
                combining speed, hands, and route-running precision. From Calvin Johnson's dominance to Antonio Brown's consistency, 
                this section showcases the players who changed games with a single catch. Watch the legends separate themselves.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        wr_data = df_filtered[df_filtered['receiver_player_name'].notna()].copy()
        
        # RACING BAR CHART - Top WRs by Receiving Yards
        st.markdown("###  Racing Bar: Top Wide Receivers by Receiving Yards")
        st.caption(" **Elite Pass Catchers:** Follow the career progressions of the decade's best receivers. Each bar's movement tells a story of consistency and explosive seasons.")
        
        # Calculate cumulative yards per WR per year with smooth transitions
        wr_frames = []
        wr_cumulative = {}
        frames_per_year = 100
        
        # Get team for each WR to apply team colors
        wr_team_map = {}
        for wr in wr_data['receiver_player_name'].unique():
            if pd.notna(wr):
                team = wr_data[wr_data['receiver_player_name'] == wr]['posteam'].mode()
                wr_team_map[wr] = team.values[0] if len(team) > 0 else 'NFL'
        
        for year in range(2009, 2019):
            year_wrs = wr_data[wr_data['year'] == year].groupby('receiver_player_name')['yards_gained'].sum().to_dict()
            
            for frame_idx in range(frames_per_year):
                progress = frame_idx / frames_per_year
                current_wr_vals = {}
                
                for wr in set(list(wr_cumulative.keys()) + list(year_wrs.keys())):
                    base = wr_cumulative.get(wr, 0)
                    increment = year_wrs.get(wr, 0) * progress
                    current_wr_vals[wr] = base + increment
                
                sorted_wrs = sorted(current_wr_vals.items(), key=lambda x: x[1], reverse=True)[:15]
                wr_names = [w[0] for w in sorted_wrs]
                wr_yards = [w[1] for w in sorted_wrs]
                wr_colors = [NFL_COLORS.get(wr_team_map.get(w[0], 'NFL'), '#A78BFA') for w in sorted_wrs]
                
                wr_frames.append(go.Frame(
                    data=[go.Bar(
                        y=wr_names,
                        x=wr_yards,
                        orientation='h',
                        marker=dict(color=wr_colors, line=dict(color='white', width=2)),
                        text=[f"{int(y):,}" for y in wr_yards],
                        textposition='outside',
                        textfont=dict(size=12, color='white', family='Arial Black')
                    )],
                    name=f"{year}.{frame_idx}"
                ))
            
            for wr, yards in year_wrs.items():
                wr_cumulative[wr] = wr_cumulative.get(wr, 0) + yards
        
        # Initial WR figure
        initial_wr_data = wr_data[wr_data['year'] <= 2009].groupby('receiver_player_name')['yards_gained'].sum().nlargest(15)
        initial_wr_colors = [NFL_COLORS.get(wr_team_map.get(wr, 'NFL'), '#A78BFA') for wr in initial_wr_data.index]
        
        fig_race_wr = go.Figure(
            data=[go.Bar(
                y=initial_wr_data.index,
                x=initial_wr_data.values,
                orientation='h',
                marker=dict(color=initial_wr_colors, line=dict(color='white', width=2))
            )],
            frames=wr_frames
        )
        
        fig_race_wr.update_layout(
            title=dict(text='<b>RACING BAR: TOP WIDE RECEIVERS BY RECEIVING YARDS</b>', font=dict(size=24, color='white')),
            xaxis=dict(title='Cumulative Receiving Yards', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white'), range=[0, 14000]),
            yaxis=dict(tickfont=dict(color='white', size=10)),
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            height=700,
            margin=dict(l=200, r=50, t=100, b=150),
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {'label': 'Play', 'method': 'animate',
                     'args': [None, {'frame': {'duration': 30, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 20, 'easing': 'linear'}}]},
                    {'label': 'Pause', 'method': 'animate',
                     'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}]}
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 10},
                'x': 0.85, 'xanchor': 'left', 'y': 1.15, 'yanchor': 'top',
                'bgcolor': '#1a1a2e',
                'bordercolor': '#FFD700',
                'borderwidth': 2,
                'font': {'size': 16, 'color': '#FFD700'}
            }],
            sliders=[{
                'active': 0,
                'yanchor': 'top',
                'y': -0.15,
                'xanchor': 'left',
                'currentvalue': {
                    'prefix': 'Year: ',
                    'visible': True,
                    'xanchor': 'right',
                    'font': {'size': 16, 'color': '#FFD700'}
                },
                'steps': [{'args': [[f.name], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}],
                          'label': f.name.split('.')[0], 'method': 'animate'} for i, f in enumerate(wr_frames) if i % 100 == 0],
                'x': 0.0, 'len': 1.0
            }]
        )
        
        st.plotly_chart(fig_race_wr, width='stretch')
        
        st.markdown("---")
        
        st.markdown("### Top Wide Receivers by Receiving Yards")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.caption(" **Elite Pass Catchers:** These receivers define excellence - combining route precision, reliable hands, and game-breaking speed to accumulate massive receiving yards.")
            # Top WRs by Receiving Yards - Lollipop Chart
            wr_yards = wr_data.groupby('receiver_player_name')['yards_gained'].sum().nlargest(15)
            
            # Get team for each WR to apply team colors
            wr_teams = {}
            for wr in wr_yards.index:
                team = wr_data[wr_data['receiver_player_name'] == wr]['posteam'].mode()
                wr_teams[wr] = team.values[0] if len(team) > 0 else 'NFL'
            
            fig_wr_yards, ax_wr = plt.subplots(figsize=(10, 9))
            fig_wr_yards.patch.set_facecolor('#16213e')
            
            y_pos = np.arange(len(wr_yards))
            colors_wr = [NFL_COLORS.get(wr_teams.get(wr, 'NFL'), '#A78BFA') for wr in wr_yards.index]
            
            # Create lollipop stems
            ax_wr.hlines(y=y_pos, xmin=0, xmax=wr_yards.values, color=colors_wr, alpha=0.8, linewidth=4)
            # Create lollipop heads
            ax_wr.scatter(wr_yards.values, y_pos, color=colors_wr, s=250, alpha=0.9, edgecolors='white', linewidth=3, zorder=3)
            
            # Add value labels
            for i, (wr, yards) in enumerate(wr_yards.items()):
                ax_wr.text(yards + 200, i, f"{int(yards):,}", va='center', ha='left',
                          fontsize=11, color='white', fontweight='bold')
                # Add team code
                team = wr_teams.get(wr, 'NFL')
                ax_wr.text(yards * 0.05, i, team, va='center', ha='left',
                          fontsize=9, color='white', fontweight='bold',
                          bbox=dict(boxstyle='round,pad=0.3', facecolor='black', 
                                   edgecolor='white', linewidth=1, alpha=0.7))
            
            ax_wr.set_yticks(y_pos)
            ax_wr.set_yticklabels([wr.split()[-1] for wr in wr_yards.index], fontsize=11, color='white', fontweight='bold')
            ax_wr.set_xlabel('Receiving Yards', fontsize=13, color='white', fontweight='bold')
            ax_wr.set_title('TOP 15 WRs - RECEIVING YARDS', fontsize=18, color='#FFD700', fontweight='bold', pad=15)
            ax_wr.set_facecolor('#1a1a2e')
            ax_wr.tick_params(colors='white', labelsize=10)
            ax_wr.grid(True, alpha=0.3, color='white', linestyle='--', axis='x')
            ax_wr.invert_yaxis()
            
            plt.tight_layout()
            st.pyplot(fig_wr_yards)
            plt.close()
        
        with col2:
            st.caption(" **Touchdown Makers:** Finding the end zone is the ultimate WR achievement. These pass catchers turned opportunities into points with remarkable consistency.")
            # WR Touchdowns with Team Colors
            wr_tds = wr_data.groupby('receiver_player_name')['touchdown'].sum().nlargest(15)
            
            # Get team for each WR
            wr_td_teams = {}
            for wr in wr_tds.index:
                team = wr_data[wr_data['receiver_player_name'] == wr]['posteam'].mode()
                wr_td_teams[wr] = team.values[0] if len(team) > 0 else 'NFL'
            
            wr_td_colors = [NFL_COLORS.get(wr_td_teams.get(wr, 'NFL'), '#A78BFA') for wr in wr_tds.index]
            
            fig_wr_tds = go.Figure()
            fig_wr_tds.add_trace(go.Bar(
                x=[r for r in wr_tds.index],
                y=wr_tds.values,
                marker=dict(
                    color=wr_td_colors,
                    line=dict(color='white', width=2)
                ),
                text=wr_tds.values,
                textposition='outside',
                textfont=dict(size=12, color='white', family='Arial Black')
            ))
            fig_wr_tds.update_layout(
                title=dict(text='<b>TOP 15 WRs - TOUCHDOWNS</b>', font=dict(size=20, color='white', family='Arial Black')),
                xaxis=dict(tickfont=dict(color='white', size=9), tickangle=-45),
                yaxis=dict(title='Touchdowns', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
                plot_bgcolor='#1a1a2e',
                paper_bgcolor='#16213e',
                font=dict(color='white'),
                height=550
            )
            st.plotly_chart(fig_wr_tds, width="stretch")
        
        # WR Receptions and Yards per Reception
        st.markdown("###  Reception Efficiency Analysis")
        st.caption(" **Volume vs Explosiveness:** Top-right quadrant shows rare receivers who combine high catch totals with big yards per catch. These are the true game-breakers.")
        wr_stats = wr_data.groupby('receiver_player_name').agg({
            'yards_gained': ['sum', 'mean'],
            'complete_pass': 'sum'
        }).reset_index()
        wr_stats.columns = ['player', 'total_yards', 'yards_per_rec', 'receptions']
        wr_stats = wr_stats[wr_stats['receptions'] >= 100].nlargest(20, 'yards_per_rec')
        
        fig_wr_efficiency = go.Figure()
        fig_wr_efficiency.add_trace(go.Scatter(
            x=wr_stats['receptions'],
            y=wr_stats['yards_per_rec'],
            mode='markers+text',
            marker=dict(
                size=wr_stats['total_yards'] / 150,
                color=wr_stats['yards_per_rec'],
                colorscale='Viridis',
                showscale=True,
                line=dict(color='white', width=2),
                colorbar=dict(title=dict(text='Yards/Rec', font=dict(color='white')))
            ),
            text=wr_stats['player'].apply(lambda x: x.split()[-1]),
            textposition='top center',
            textfont=dict(size=10, color='white', family='Arial Black')
        ))
        fig_wr_efficiency.update_layout(
            title=dict(text='<b>WR EFFICIENCY - YARDS PER RECEPTION (min 100 receptions)</b>', font=dict(size=22, color='white', family='Arial Black')),
            xaxis=dict(title='Total Receptions', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
            yaxis=dict(title='Yards per Reception', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            height=600
        )
        st.plotly_chart(fig_wr_efficiency, width="stretch")
    
    # TAB 5: DEFENSE ANALYSIS - CONSOLIDATED
    with tab5:
        st.markdown("##  ELITE DEFENSIVE UNITS & PLAYMAKERS")
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(26, 26, 46, 0.8) 0%, rgba(22, 33, 62, 0.8) 100%); 
                    padding: 20px; border-radius: 12px; border-left: 4px solid #00D9FF; margin-bottom: 25px;'>
            <p style='color: #FFFFFF; font-size: 1.05rem; line-height: 1.6; margin: 0;'>
                <strong style='color: #00D9FF;'> Defense Wins Championships:</strong> While offense fills highlights, 
                defense wins titles. This section reveals which units excelled at forcing turnovers, disrupting quarterbacks, 
                and preventing points. Four integrated visualizations tell the complete defensive story from multiple angles.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption(" **Four-Panel Analysis:** Top-left shows interception leaders (polar chart), top-right displays multi-category performance (heatmap), bottom-left reveals sacks-turnover correlation (scatter), bottom-right compares elite units (violin plots). Together, these visualizations tell the complete defensive story.")
        
        st.markdown("""
        <div style='background: rgba(0, 217, 255, 0.1); padding: 12px; border-radius: 8px; border-left: 3px solid #00D9FF; margin: 15px 0;'>
            <p style='color: #FFFFFF; font-size: 0.9rem; line-height: 1.5; margin: 0;'>
                <strong style='color: #00D9FF;'> How to Read:</strong> 
                <strong>Polar Chart:</strong> Interception leaders radiate outward. 
                <strong>Heatmap:</strong> Brighter colors = better performance across sacks, INTs, forced fumbles. 
                <strong>Scatter:</strong> Top-right quadrant = teams excelling in both sacks and turnovers. 
                <strong>Violin:</strong> Wider shapes show more variability in defensive performance.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create consolidated matplotlib figure - 2x2 grid
        fig_defense, axes_def = plt.subplots(2, 2, figsize=(20, 16))
        fig_defense.patch.set_facecolor('#16213e')
        
        # 1. POLAR CHART - Top Defenses by Interceptions
        ax_polar = plt.subplot(2, 2, 1, projection='polar')
        int_data = df_filtered[df_filtered['interception'] == 1]
        team_ints = int_data.groupby('defteam')['interception'].sum().nlargest(10)
        
        theta = np.linspace(0, 2 * np.pi, len(team_ints), endpoint=False)
        width = 2 * np.pi / len(team_ints)
        colors_int = [NFL_COLORS.get(team, '#4ECDC4') for team in team_ints.index]
        
        bars = ax_polar.bar(theta, team_ints.values, width=width, color=colors_int, 
                           edgecolor='white', linewidth=3, alpha=0.85)
        ax_polar.set_theta_zero_location('N')
        ax_polar.set_theta_direction(-1)
        ax_polar.set_xticks(theta)
        ax_polar.set_xticklabels([team for team in team_ints.index], 
                                 color='#FFD700', fontsize=13, fontweight='bold',
                                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a1a2e',
                                          edgecolor='white', linewidth=1.5, alpha=0.9))
        ax_polar.set_ylim(0, max(team_ints.values) * 1.2)
        ax_polar.set_facecolor('#0a0a0f')  # Very dark background
        ax_polar.tick_params(colors='white', labelsize=11)
        ax_polar.set_title('TOP 10 INTERCEPTION LEADERS', fontsize=17, 
                          color='#FFD700', fontweight='bold', pad=25)
        ax_polar.grid(True, alpha=0.4, color='#FFD700', linestyle='--', linewidth=1.5)
        
        # Add value labels
        for bar, value, team in zip(bars, team_ints.values, team_ints.index):
            height = bar.get_height()
            ax_polar.text(bar.get_x() + bar.get_width()/2., height + 8,
                         f'{int(value)}', ha='center', va='bottom', 
                         color='white', fontweight='bold', fontsize=11)
        
        # Add legend with team information
        legend_labels = [f"{team}: {int(val)} INTs" for team, val in zip(team_ints.index, team_ints.values)]
        ax_polar.legend(legend_labels, loc='upper left', bbox_to_anchor=(1.15, 1.0),
                       facecolor='#1a1a2e', edgecolor='#FFD700', framealpha=0.95,
                       fontsize=9, ncol=1)
        plt.setp(ax_polar.get_legend().get_texts(), color='white')
        
        # 2. HEATMAP - Defensive Performance Matrix
        ax_heat = axes_def[0, 1]
        
        # Prepare data for heatmap
        sack_data = df_filtered[df_filtered['sack'] == 1]
        fumble_data = df_filtered[df_filtered['fumble_lost'] == 1]
        
        top_def_teams = team_ints.head(8).index
        
        defense_matrix = []
        for team in top_def_teams:
            ints = team_ints.get(team, 0)
            sacks = sack_data[sack_data['defteam'] == team]['sack'].sum()
            fumbles = fumble_data[fumble_data['defteam'] == team]['fumble_lost'].sum()
            epa = df_filtered[df_filtered['defteam'] == team]['epa'].mean()
            defense_matrix.append([ints, sacks, fumbles, -epa*100])  # Negative EPA is better for defense
        
        defense_df = pd.DataFrame(defense_matrix, 
                                 index=[NFL_NAMES.get(t, t)[:10] for t in top_def_teams],
                                 columns=['INTs', 'Sacks', 'Fumbles', 'EPA Impact'])
        
        # Normalize for better visualization
        defense_df_norm = (defense_df - defense_df.min()) / (defense_df.max() - defense_df.min())
        
        sns.heatmap(defense_df_norm, annot=defense_df.values, fmt='.0f', 
                   cmap='RdYlGn', center=0.5, ax=ax_heat,
                   cbar_kws={'label': 'Performance Score (0-1)', 'pad': 0.02},
                   linewidths=3, linecolor='white',
                   annot_kws={'size': 11, 'weight': 'bold', 'color': 'white'})
        
        # Customize colorbar
        cbar = ax_heat.collections[0].colorbar
        cbar.ax.tick_params(colors='white', labelsize=10)
        cbar.ax.set_ylabel('Performance Score (0-1)', color='white', fontweight='bold', fontsize=11)
        
        ax_heat.set_title('DEFENSIVE PERFORMANCE MATRIX - Top 8 Teams', fontsize=17, 
                         color='#FFD700', fontweight='bold', pad=20)
        ax_heat.set_xlabel('Defensive Metric', fontsize=13, color='white', fontweight='bold')
        ax_heat.set_ylabel('Team', fontsize=13, color='white', fontweight='bold')
        ax_heat.tick_params(colors='white', labelsize=11)
        
        # Add explanation text
        ax_heat.text(0.5, -0.15, 'Higher values indicate better defensive performance',
                    transform=ax_heat.transAxes, ha='center', fontsize=10,
                    color='#FFD700', style='italic')
        
        # 3. SCATTER PLOT - Sacks vs Turnovers with Team Logos as text
        ax_scatter = axes_def[1, 0]
        
        team_stats = []
        for team in df_filtered['defteam'].unique():
            if pd.notna(team) and team in NFL_COLORS:
                team_df = df_filtered[df_filtered['defteam'] == team]
                sacks = len(team_df[team_df['sack'] == 1])
                ints = len(team_df[team_df['interception'] == 1])
                fumbles = len(team_df[team_df['fumble_lost'] == 1])
                turnovers = ints + fumbles
                team_stats.append({
                    'team': team,
                    'sacks': sacks,
                    'turnovers': turnovers,
                    'color': NFL_COLORS.get(team, '#00D9FF')
                })
        
        team_stats_df = pd.DataFrame(team_stats).nlargest(15, 'turnovers')
        
        scatter = ax_scatter.scatter(team_stats_df['sacks'], team_stats_df['turnovers'], 
                                    s=600, c=team_stats_df['color'], 
                                    edgecolors='white', linewidth=3, alpha=0.85, zorder=3)
        
        # Add team codes as labels
        for _, row in team_stats_df.iterrows():
            ax_scatter.text(row['sacks'], row['turnovers'], row['team'], 
                          fontsize=10, fontweight='bold', color='white',
                          ha='center', va='center', zorder=4)
        
        ax_scatter.set_xlabel('Total Sacks', fontsize=13, color='white', fontweight='bold')
        ax_scatter.set_ylabel('Total Turnovers (INTs + Fumbles)', fontsize=13, color='white', fontweight='bold')
        ax_scatter.set_title('DEFENSIVE IMPACT: Sacks vs Turnovers', fontsize=17,
                           color='#FFD700', fontweight='bold', pad=15)
        ax_scatter.set_facecolor('#1a1a2e')
        ax_scatter.tick_params(colors='white', labelsize=11)
        ax_scatter.grid(True, alpha=0.3, color='white', linestyle='--')
        
        # Add trend line
        z = np.polyfit(team_stats_df['sacks'], team_stats_df['turnovers'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(team_stats_df['sacks'].min(), team_stats_df['sacks'].max(), 100)
        ax_scatter.plot(x_trend, p(x_trend), color='#FFD700', linestyle='--', 
                       linewidth=3, alpha=0.7, label=f'Trend: y = {z[0]:.2f}x + {z[1]:.2f}')
        
        # Calculate R-squared
        correlation = np.corrcoef(team_stats_df['sacks'], team_stats_df['turnovers'])[0, 1]
        r_squared = correlation ** 2
        
        legend_scatter = ax_scatter.legend(facecolor='#1a1a2e', edgecolor='#FFD700', 
                                          fontsize=11, framealpha=0.95,
                                          title=f'R = {r_squared:.3f}')
        plt.setp(legend_scatter.get_texts(), color='white')
        plt.setp(legend_scatter.get_title(), color='#FFD700', fontweight='bold')
        
        # 4. VIOLIN PLOT - EPA Distribution by Top Defense Teams
        ax_violin = axes_def[1, 1]
        
        top_6_def = team_ints.head(6).index
        epa_by_team = []
        team_labels = []
        colors_violin = []
        
        for team in top_6_def:
            team_epa = df_filtered[df_filtered['defteam'] == team]['epa'].dropna()
            if len(team_epa) > 0:
                epa_by_team.append(team_epa.values)
                team_labels.append(team)
                colors_violin.append(NFL_COLORS.get(team, '#FF6B6B'))
        
        parts = ax_violin.violinplot(epa_by_team, positions=range(len(team_labels)),
                                     widths=0.7, showmeans=True, showmedians=True)
        
        # Customize violin colors
        for i, pc in enumerate(parts['bodies']):
            pc.set_facecolor(colors_violin[i])
            pc.set_edgecolor('white')
            pc.set_linewidth(2)
            pc.set_alpha(0.7)
        
        # Customize other elements
        for partname in ('cbars', 'cmins', 'cmaxes', 'cmedians', 'cmeans'):
            if partname in parts:
                vp = parts[partname]
                vp.set_edgecolor('white')
                vp.set_linewidth(2)
        
        ax_violin.set_xticks(range(len(team_labels)))
        ax_violin.set_xticklabels(team_labels, fontsize=12, color='white', 
                                  fontweight='bold', rotation=0)
        ax_violin.set_ylabel('EPA Allowed (Lower = Better)', fontsize=13, 
                            color='white', fontweight='bold')
        ax_violin.set_title('EPA DISTRIBUTION - Elite Defensive Units', fontsize=17,
                          color='#FFD700', fontweight='bold', pad=15)
        ax_violin.set_facecolor('#1a1a2e')
        ax_violin.tick_params(colors='white', labelsize=11)
        ax_violin.grid(True, alpha=0.3, color='white', linestyle='--', axis='y')
        ax_violin.axhline(y=0, color='#FFD700', linestyle='--', linewidth=2, alpha=0.8, label='Neutral EPA')
        
        # Add mean and median values for each team
        for i, (team, epa_vals) in enumerate(zip(team_labels, epa_by_team)):
            mean_epa = np.mean(epa_vals)
            median_epa = np.median(epa_vals)
            # Add mean annotation
            ax_violin.text(i, mean_epa, f'={mean_epa:.3f}',
                          ha='center', va='bottom', color='#FF6B6B',
                          fontweight='bold', fontsize=9,
                          bbox=dict(boxstyle='round,pad=0.3', facecolor='black',
                                   edgecolor='#FF6B6B', linewidth=1, alpha=0.8))
            # Add median annotation
            ax_violin.text(i, median_epa, f'M={median_epa:.3f}',
                          ha='center', va='top', color='#4ECDC4',
                          fontweight='bold', fontsize=9,
                          bbox=dict(boxstyle='round,pad=0.3', facecolor='black',
                                   edgecolor='#4ECDC4', linewidth=1, alpha=0.8))
        
        # Add legend with team colors
        legend_handles = [plt.Line2D([0], [0], marker='o', color='w', 
                                     markerfacecolor=NFL_COLORS.get(team, '#FF6B6B'), 
                                     markersize=10, label=team, markeredgecolor='white', markeredgewidth=2)
                         for team in team_labels]
        legend_violin = ax_violin.legend(handles=legend_handles, loc='upper right',
                                        facecolor='#1a1a2e', edgecolor='#FFD700',
                                        framealpha=0.95, fontsize=10, title='Teams')
        plt.setp(legend_violin.get_texts(), color='white')
        plt.setp(legend_violin.get_title(), color='#FFD700', fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig_defense)
        plt.close()
        
        st.markdown("---")
        
        # ELITE DEFENSIVE PLAYERS - Single consolidated figure
        st.markdown("###  ELITE DEFENSIVE PLAYMAKERS")
        
        fig_players, axes_players = plt.subplots(1, 2, figsize=(20, 8))
        fig_players.patch.set_facecolor('#16213e')
        
        # LEFT: Top Interception Leaders - Radial Lollipop Chart
        ax_int_players = plt.subplot(1, 2, 1, projection='polar')
        int_players = df_filtered[df_filtered['interception'] == 1].copy()
        top_int = int_players['interception_player_name'].value_counts().head(12)
        
        player_teams_int = {}
        for player in top_int.index:
            teams = int_players[int_players['interception_player_name'] == player]['defteam'].mode()
            player_teams_int[player] = teams.values[0] if len(teams) > 0 else 'NFL'
        
        colors_players = [NFL_COLORS.get(player_teams_int.get(p, 'NFL'), '#4ECDC4') for p in top_int.index]
        
        # Create radial positions
        theta_players = np.linspace(0, 2 * np.pi, len(top_int), endpoint=False)
        radii = top_int.values
        
        # Draw lollipop stems
        for t, r, color in zip(theta_players, radii, colors_players):
            ax_int_players.plot([t, t], [0, r], color=color, linewidth=4, alpha=0.8, zorder=2)
        
        # Draw lollipop heads
        ax_int_players.scatter(theta_players, radii, s=400, c=colors_players,
                              edgecolors='white', linewidth=3, alpha=0.9, zorder=3)
        
        # Add player names and values
        for t, r, player, val in zip(theta_players, radii, top_int.index, top_int.values):
            # Player name (outside)
            ax_int_players.text(t, r + max(radii) * 0.12, f"{player.split()[-1]}\n({int(val)})",
                               ha='center', va='center', color='white',
                               fontweight='bold', fontsize=10,
                               bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a1a2e',
                                        edgecolor='#FFD700', linewidth=1.5, alpha=0.9))
        
        ax_int_players.set_theta_zero_location('N')
        ax_int_players.set_theta_direction(-1)
        ax_int_players.set_ylim(0, max(radii) * 1.3)
        ax_int_players.set_facecolor('#0a0a0f')
        ax_int_players.set_title('TOP 12 INTERCEPTION LEADERS', fontsize=18,
                                color='#FFD700', fontweight='bold', pad=25)
        ax_int_players.set_xticks([])
        ax_int_players.set_yticks([])
        ax_int_players.grid(True, alpha=0.3, color='#FFD700', linestyle='--')
        
        # RIGHT: Top Tackle Leaders - Bubble Chart with Player Names
        ax_tackle_players = axes_players[1]
        
        tackle_data = []
        for col in ['solo_tackle_1_player_name', 'solo_tackle_2_player_name', 
                   'assist_tackle_1_player_name', 'assist_tackle_2_player_name']:
            if col in df_filtered.columns:
                tackles = df_filtered[df_filtered[col].notna()][[col, 'defteam']].copy()
                tackles.columns = ['player', 'team']
                tackle_data.append(tackles)
        
        all_tackles = pd.concat(tackle_data, ignore_index=True)
        top_tacklers = all_tackles['player'].value_counts().head(12)
        
        tackler_teams = {}
        for player in top_tacklers.index:
            teams = all_tackles[all_tackles['player'] == player]['team'].mode()
            tackler_teams[player] = teams.values[0] if len(teams) > 0 else 'NFL'
        
        colors_tacklers = [NFL_COLORS.get(tackler_teams.get(p, 'NFL'), '#FF6B6B') for p in top_tacklers.index]
        
        # Create bubble chart layout - arrange in grid pattern
        n_players = len(top_tacklers)
        cols = 4
        rows = int(np.ceil(n_players / cols))
        
        x_positions = []
        y_positions = []
        for i in range(n_players):
            x_positions.append(i % cols)
            y_positions.append(rows - 1 - (i // cols))
        
        # Draw bubbles
        sizes = (top_tacklers.values / top_tacklers.values.max() * 3000) + 500
        ax_tackle_players.scatter(x_positions, y_positions, s=sizes, c=colors_tacklers,
                                 edgecolors='white', linewidth=3, alpha=0.85, zorder=3)
        
        # Add player names and tackle counts
        for x, y, player, tackles, color in zip(x_positions, y_positions, 
                                                 top_tacklers.index, top_tacklers.values,
                                                 colors_tacklers):
            # Player last name
            ax_tackle_players.text(x, y + 0.08, f"{player.split()[-1]}",
                                  ha='center', va='center', color='white',
                                  fontweight='bold', fontsize=11, zorder=4)
            # Tackle count
            ax_tackle_players.text(x, y - 0.08, f"{int(tackles)}",
                                  ha='center', va='center', color='#FFD700',
                                  fontweight='bold', fontsize=13, zorder=4)
            # Team code
            team = tackler_teams.get(player, 'NFL')
            ax_tackle_players.text(x, y - 0.22, team,
                                  ha='center', va='center', color='white',
                                  fontweight='bold', fontsize=9,
                                  bbox=dict(boxstyle='round,pad=0.2', facecolor='black',
                                           edgecolor='white', linewidth=1, alpha=0.7),
                                  zorder=4)
        
        ax_tackle_players.set_xlim(-0.6, cols - 0.4)
        ax_tackle_players.set_ylim(-0.6, rows - 0.4)
        ax_tackle_players.set_title('TOP 12 TACKLE LEADERS', fontsize=18,
                                   color='#FFD700', fontweight='bold', pad=20)
        ax_tackle_players.set_facecolor('#1a1a2e')
        ax_tackle_players.set_xticks([])
        ax_tackle_players.set_yticks([])
        ax_tackle_players.spines['top'].set_visible(False)
        ax_tackle_players.spines['right'].set_visible(False)
        ax_tackle_players.spines['bottom'].set_visible(False)
        ax_tackle_players.spines['left'].set_visible(False)
        
        plt.tight_layout()
        st.pyplot(fig_players)
        plt.close()

    # TAB 6: SEABORN ANALYSIS
    with tab6:
        st.markdown("##  SEABORN STATISTICAL ANALYSIS")
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(26, 26, 46, 0.8) 0%, rgba(22, 33, 62, 0.8) 100%); 
                    padding: 20px; border-radius: 12px; border-left: 4px solid #9D4EDD; margin-bottom: 25px;'>
            <p style='color: #FFFFFF; font-size: 1.05rem; line-height: 1.6; margin: 0;'>
                <strong style='color: #9D4EDD;'> Statistical Deep Dive:</strong> Move beyond basic stats into advanced 
                analytics. These six visualizations explore win probability curves, yard distributions, play correlations, 
                and situational performance. Perfect for data enthusiasts seeking deeper insights.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption(" **Reading tip:** Look for patterns, outliers, and correlations. Each chart reveals different aspects of game dynamics and player efficiency.")
        
        # Set seaborn style
        sns.set_style("darkgrid")
        
        # Create figure with seaborn plots
        fig, axes = plt.subplots(2, 3, figsize=(22, 14))
        fig.patch.set_facecolor('#16213e')
        
        # 1. Boxplot - Win Probability by Score Differential
        ax1 = axes[0, 0]
        wp_data = df_filtered[df_filtered['score_differential'].between(-21, 21)].copy()
        sns.scatterplot(data=wp_data.sample(min(5000, len(wp_data))), x='score_differential', y='wp', 
                       hue='qtr', palette='viridis', ax=ax1, alpha=0.6, s=50, edgecolor='white', linewidth=0.5)
        ax1.set_title('Win Probability vs Score Differential', fontsize=16, color='#FFD700', fontweight='bold', pad=15)
        ax1.set_xlabel('Score Differential', fontsize=12, color='white', fontweight='bold')
        ax1.set_ylabel('Win Probability', fontsize=12, color='white', fontweight='bold')
        ax1.set_facecolor('#1a1a2e')
        ax1.tick_params(colors='white', labelsize=11)
        ax1.grid(True, alpha=0.2, color='white', linestyle='--')
        ax1.axhline(y=0.5, color='#FFD700', linestyle='--', linewidth=2, label='50% Win Prob')
        ax1.axvline(x=0, color='#FF6B6B', linestyle='--', linewidth=2, label='Tied')
        legend1 = ax1.legend(facecolor='#1a1a2e', edgecolor='#FFD700', fontsize=10, 
                            title='Quarter', title_fontsize=11, framealpha=0.95, loc='best')
        plt.setp(legend1.get_texts(), color='white')
        plt.setp(legend1.get_title(), color='#FFD700')
        
        # 2. Violinplot - Yards by Down
        ax2 = axes[0, 1]
        down_data = df_filtered[df_filtered['down'].isin([1, 2, 3, 4])]
        parts = sns.violinplot(data=down_data, x='down', y='yards_gained', palette='muted', ax=ax2, linewidth=2)
        ax2.set_title('Yards Gained by Down', fontsize=16, color='#FFD700', fontweight='bold', pad=15)
        ax2.set_xlabel('Down Number', fontsize=12, color='white', fontweight='bold')
        ax2.set_ylabel('Yards Gained', fontsize=12, color='white', fontweight='bold')
        ax2.set_facecolor('#1a1a2e')
        ax2.tick_params(colors='white', labelsize=11)
        ax2.grid(True, alpha=0.2, color='white', axis='y', linestyle='--')
        ax2.axhline(y=0, color='#FFD700', linestyle='--', linewidth=2, alpha=0.7, label='Zero Yards')
        # Add mean line for context
        mean_yards = down_data.groupby('down')['yards_gained'].mean()
        for i, down in enumerate([1, 2, 3, 4]):
            if down in mean_yards.index:
                ax2.text(i, mean_yards[down], f'={mean_yards[down]:.1f}',
                        ha='center', va='bottom', color='#FFD700', fontweight='bold', fontsize=9)
        legend2 = ax2.legend(facecolor='#1a1a2e', edgecolor='#FFD700', fontsize=10, framealpha=0.95)
        plt.setp(legend2.get_texts(), color='white')
        ax2.set_ylim(-20, 60)
        ax2.axhline(y=0, color='#FFD700', linestyle='--', linewidth=2, label='No Gain/Loss')
        legend2 = ax2.legend(facecolor='#1a1a2e', edgecolor='#FFD700', fontsize=10, framealpha=0.95)
        plt.setp(legend2.get_texts(), color='white')
        
        # 3. Heatmap - Correlation Matrix
        ax3 = axes[0, 2]
        corr_cols = ['yards_gained', 'epa', 'wp', 'wpa', 'air_yards']
        corr_data = df_filtered[corr_cols].corr()
        sns.heatmap(corr_data, annot=True, cmap='RdYlGn', center=0, ax=ax3,
                   cbar_kws={'label': 'Correlation'}, fmt='.3f', linewidths=2, linecolor='white',
                   annot_kws={'size': 11, 'weight': 'bold'})
        ax3.set_title('Correlation Matrix: Key Metrics', fontsize=16, color='#FFD700', fontweight='bold', pad=15)
        ax3.tick_params(colors='white', labelsize=10)
        
        # 4. Regplot - EPA vs Air Yards
        ax4 = axes[1, 0]
        reg_data = df_filtered[df_filtered['air_yards'].notna()].sample(min(1500, len(df_filtered)))
        sns.regplot(data=reg_data, x='air_yards', y='epa', scatter_kws={'alpha':0.4, 's':40, 'edgecolor':'white', 'label':'Plays'},
                   line_kws={'color':'#FFD700', 'linewidth':4, 'label':'Trend Line'}, ax=ax4, color='#00D9FF')
        ax4.set_title('EPA vs Air Yards Relationship', fontsize=16, color='#FFD700', fontweight='bold', pad=15)
        ax4.set_xlabel('Air Yards (distance thrown)', fontsize=12, color='white', fontweight='bold')
        ax4.set_ylabel('Expected Points Added', fontsize=12, color='white', fontweight='bold')
        ax4.set_facecolor('#1a1a2e')
        ax4.tick_params(colors='white', labelsize=11)
        ax4.grid(True, alpha=0.2, color='white', linestyle='--')
        legend4 = ax4.legend(facecolor='#1a1a2e', edgecolor='#FFD700', fontsize=10, framealpha=0.95)
        plt.setp(legend4.get_texts(), color='white')
        
        # 5. KDE Plot - Yards Distribution
        ax5 = axes[1, 1]
        yards_data = df_filtered[df_filtered['yards_gained'].between(-10, 50)]['yards_gained']
        sns.kdeplot(data=yards_data, fill=True, color='#4ECDC4', alpha=0.7, ax=ax5, linewidth=3)
        ax5.set_title('Yards Distribution Density', fontsize=16, color='#FFD700', fontweight='bold', pad=15)
        ax5.set_xlabel('Yards Gained', fontsize=12, color='white', fontweight='bold')
        ax5.set_ylabel('Density', fontsize=14, color='white', fontweight='bold')
        ax5.set_facecolor('#1a1a2e')
        ax5.tick_params(colors='white', labelsize=11)
        ax5.grid(True, alpha=0.2, color='white', linestyle='--')
        ax5.axvline(x=yards_data.mean(), color='#FFD700', linestyle='--', linewidth=3, label=f'Mean: {yards_data.mean():.2f}')
        legend5 = ax5.legend(facecolor='#1a1a2e', edgecolor='#FFD700', fontsize=11, framealpha=0.95)
        plt.setp(legend5.get_texts(), color='white')
        
        # 6. Countplot - Plays by Quarter
        ax6 = axes[1, 2]
        sns.countplot(data=df_filtered, x='qtr', palette='rocket', ax=ax6, edgecolor='white', linewidth=2)
        ax6.set_title('Play Frequency by Quarter', fontsize=16, color='#FFD700', fontweight='bold', pad=15)
        ax6.set_xlabel('Quarter', fontsize=12, color='white', fontweight='bold')
        ax6.set_ylabel('Number of Plays', fontsize=12, color='white', fontweight='bold')
        ax6.set_facecolor('#1a1a2e')
        ax6.tick_params(colors='white', labelsize=11)
        ax6.grid(True, alpha=0.2, color='white', axis='y', linestyle='--')
        # Add value labels on bars
        for container in ax6.containers:
            ax6.bar_label(container, color='white', fontweight='bold', fontsize=10)
        # Add total plays annotation
        total_plays = len(df_filtered)
        ax6.text(0.95, 0.95, f'Total Plays: {total_plays:,}',
                transform=ax6.transAxes, ha='right', va='top',
                color='#FFD700', fontweight='bold', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e', 
                         edgecolor='#FFD700', linewidth=2, alpha=0.9))
        
        plt.tight_layout(pad=3.0)
        st.pyplot(fig)
        plt.close()
        
        # Additional Seaborn Analysis
        st.markdown("###  Pass vs Rush Comparison")
        st.caption(" **Offensive Philosophy:** Compare the risk-reward of passing vs rushing. Passing offers higher upside but more variance, while rushing provides steadier but smaller gains.")
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pass_rush, ax = plt.subplots(figsize=(10, 6))
            fig_pass_rush.patch.set_facecolor('#16213e')
            
            pass_rush_data = df_filtered[df_filtered['play_type'].isin(['pass', 'run'])].copy()
            sns.boxplot(data=pass_rush_data, x='play_type', y='yards_gained', 
                       hue='play_type', palette=['#FF6B6B', '#4ECDC4'], ax=ax, linewidth=2.5, legend=False)
            ax.set_title('Pass vs Rush: Yards Distribution', fontsize=18, color='#FFD700', fontweight='bold', pad=15)
            ax.set_xlabel('Play Type', fontsize=14, color='white', fontweight='bold')
            ax.set_ylabel('Yards Gained', fontsize=14, color='white', fontweight='bold')
            ax.set_facecolor('#1a1a2e')
            ax.tick_params(colors='white', labelsize=12)
            ax.grid(True, alpha=0.2, color='white', linestyle='--')
            ax.set_ylim(-20, 60)
            # Add statistics
            pass_mean = pass_rush_data[pass_rush_data['play_type']=='pass']['yards_gained'].mean()
            run_mean = pass_rush_data[pass_rush_data['play_type']=='run']['yards_gained'].mean()
            ax.text(0.02, 0.98, f'Pass Avg: {pass_mean:.2f} yds\nRun Avg: {run_mean:.2f} yds',
                   transform=ax.transAxes, ha='left', va='top',
                   color='white', fontweight='bold', fontsize=11,
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e',
                            edgecolor='#FFD700', linewidth=2, alpha=0.9))
            
            plt.tight_layout()
            st.pyplot(fig_pass_rush)
            plt.close()
        
        with col2:
            fig_time, ax = plt.subplots(figsize=(10, 6))
            fig_time.patch.set_facecolor('#16213e')
            
            time_data = df_filtered[df_filtered['qtr'].isin([1, 2, 3, 4])].copy()
            sns.violinplot(data=time_data, x='qtr', y='epa', palette='viridis', ax=ax, linewidth=2)
            ax.set_title('EPA by Quarter', fontsize=18, color='#FFD700', fontweight='bold', pad=15)
            ax.set_xlabel('Quarter', fontsize=14, color='white', fontweight='bold')
            ax.set_ylabel('EPA', fontsize=14, color='white', fontweight='bold')
            ax.set_facecolor('#1a1a2e')
            ax.tick_params(colors='white', labelsize=12)
            ax.grid(True, alpha=0.2, color='white', axis='y', linestyle='--')
            ax.axhline(y=0, color='#FFD700', linestyle='--', linewidth=2, label='Neutral EPA')
            # Add average EPA per quarter
            qtr_means = time_data.groupby('qtr')['epa'].mean()
            for i, qtr in enumerate([1, 2, 3, 4]):
                if qtr in qtr_means.index:
                    ax.text(i, qtr_means[qtr], f'{qtr_means[qtr]:.3f}',
                           ha='center', va='bottom', color='#FFD700', fontweight='bold', fontsize=10)
            legend_epa = ax.legend(facecolor='#1a1a2e', edgecolor='#FFD700', fontsize=11, framealpha=0.95)
            plt.setp(legend_epa.get_texts(), color='white')
            
            plt.tight_layout()
            st.pyplot(fig_time)
            plt.close()
    
    # TAB 7: GAME HIGHLIGHTS
    with tab7:
        with st.spinner('Loading game highlights...'):
            st.markdown("##  GAME HIGHLIGHTS - ELITE PERFORMANCES")
            
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 46, 0.8) 0%, rgba(22, 33, 62, 0.8) 100%); 
                        padding: 20px; border-radius: 12px; border-left: 4px solid #FFD700; margin-bottom: 25px;'>
                <p style='color: #FFFFFF; font-size: 1.05rem; line-height: 1.6; margin: 0;'>
                    <strong style='color: #FFD700;'> Unforgettable Games:</strong> Some performances transcend statistics and become 
                    legendary. This section immortalizes the greatest single-game performances of the decade - games where stars became 
                    legends. Each field map visualizes the story of dominance, showing where magic happened on the gridiron.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.caption(" **Legend:** Gold stars mark touchdowns, colors represent play types (blue=rushing, orange=passing). Field position shows where each highlight occurred.")
            
            # Custom CSS for highlight cards
            st.markdown("""
            <style>
            .highlight-card {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border: 3px solid #FFD700;
                border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 8px 16px rgba(255, 215, 0, 0.3);
        }
        .player-name {
            color: #FFD700;
            font-size: 24px;
            font-weight: 900;
            font-family: 'Arial Black', sans-serif;
            margin-bottom: 5px;
        }
        .game-date {
            color: #00D9FF;
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 15px;
        }
        .stat-box {
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            color: #000;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: 900;
            margin: 5px 0;
        }
        .stat-value {
            font-size: 32px;
            font-weight: 900;
        }
        .stat-label {
            font-size: 14px;
            font-weight: 700;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Function to draw enhanced NFL field
        def draw_field(ax):
            """Draw an enhanced NFL field with yard lines"""
            # Background
            ax.add_patch(plt.Rectangle((-10, 0), 120, 53.3, facecolor='#1a4d2e', zorder=0))
            
            # Main field with striping effect
            for i in range(0, 100, 10):
                if i % 20 == 0:
                    ax.add_patch(plt.Rectangle((i, 0), 10, 53.3, facecolor='#2d5016', zorder=1))
                else:
                    ax.add_patch(plt.Rectangle((i, 0), 10, 53.3, facecolor='#1f3d0f', zorder=1))
            
            # End zones
            ax.add_patch(plt.Rectangle((-10, 0), 10, 53.3, facecolor='#0a1f0a', edgecolor='#FFD700', linewidth=4, zorder=2))
            ax.add_patch(plt.Rectangle((100, 0), 10, 53.3, facecolor='#0a1f0a', edgecolor='#FFD700', linewidth=4, zorder=2))
            
            # Yard lines
            for yard in range(0, 101, 10):
                ax.plot([yard, yard], [0, 53.3], color='white', linewidth=3, alpha=0.9, zorder=3)
                if 0 < yard < 100:
                    label = min(yard, 100 - yard) if yard != 50 else 50
                    # Add yard number with background
                    ax.text(yard, 26.65, str(label), color='white', fontsize=28, fontweight='bold', 
                           ha='center', va='center', zorder=4,
                           bbox=dict(boxstyle='circle', facecolor='#FFD700', edgecolor='white', linewidth=2, alpha=0.9))
            
            # Hash marks
            for yard in range(0, 101, 1):
                ax.plot([yard, yard], [23, 24], color='white', linewidth=1.5, alpha=0.7, zorder=3)
                ax.plot([yard, yard], [29, 30], color='white', linewidth=1.5, alpha=0.7, zorder=3)
            
            # Field border
            ax.add_patch(plt.Rectangle((0, 0), 100, 53.3, fill=False, edgecolor='white', linewidth=4, zorder=5))
            
            ax.set_xlim(-12, 112)
            ax.set_ylim(-2, 55.3)
            ax.set_aspect('equal')
            ax.axis('off')
        
        # QUARTERBACK HIGHLIGHTS
        st.markdown("###  ELITE QUARTERBACK PERFORMANCES")
        st.info(" Top 5 single-game QB performances ranked by total yards + TD bonus")
        
        qb_data = df_filtered[df_filtered['passer_player_name'].notna()].copy()
        
        # Find best single-game performances
        qb_games = qb_data.groupby(['passer_player_name', 'game_id', 'game_date', 'posteam']).agg({
            'pass_touchdown': 'sum',
            'yards_gained': 'sum',
            'complete_pass': 'sum',
            'pass_attempt': 'sum',
            'epa': 'sum',
            'interception': 'sum'
        }).reset_index()
        
        qb_games = qb_games[qb_games['pass_attempt'] >= 10]  # Min 10 attempts
        qb_games['performance_score'] = qb_games['yards_gained'] + (qb_games['pass_touchdown'] * 100) - (qb_games['interception'] * 50)
        top_qb_games = qb_games.nlargest(5, 'performance_score')
        
        for rank, (idx, game) in enumerate(top_qb_games.iterrows(), 1):
            team_color = NFL_COLORS.get(game['posteam'], '#FFD700')
            
            st.markdown(f"""
            <div class="highlight-card">
                <div class="player-name">#{rank} - {game['passer_player_name']} ({game['posteam']})</div>
                <div class="game-date"> {game['game_date'].strftime('%B %d, %Y') if hasattr(game['game_date'], 'strftime') else game['game_date']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Get all passes from this game
                game_passes = qb_data[
                    (qb_data['game_id'] == game['game_id']) & 
                    (qb_data['passer_player_name'] == game['passer_player_name']) &
                    (qb_data['yardline_100'].notna())
                ].copy()
                
                # Create field diagram
                fig, ax = plt.subplots(figsize=(18, 7))
                fig.patch.set_facecolor('#0a0a0f')
                draw_field(ax)
                
                # Plot passes with improved visualization
                pass_count = 0
                for _, play in game_passes.iterrows():
                    start_yard = 100 - play['yardline_100']
                    end_yard = start_yard + play['yards_gained']
                    
                    # Better vertical distribution
                    y_pos = 12 + (pass_count % 8) * 5.5
                    pass_count += 1
                    
                    # Enhanced colors and markers
                    if play['pass_touchdown'] == 1:
                        color = '#FFD700'
                        size = 400
                        marker = '*'
                        alpha = 1.0
                        edge_color = '#FF0000'
                        edge_width = 3
                    elif play['complete_pass'] == 1:
                        color = '#00FF41'
                        size = 180
                        marker = 'o'
                        alpha = 0.85
                        edge_color = 'white'
                        edge_width = 2.5
                    else:
                        color = '#FF4444'
                        size = 100
                        marker = 'x'
                        alpha = 0.7
                        edge_color = 'white'
                        edge_width = 2
                    
                    ax.scatter(start_yard, y_pos, c=color, s=size, marker=marker, 
                             edgecolors=edge_color, linewidths=edge_width, zorder=6, alpha=alpha)
                    
                    # Enhanced arrows for completions
                    if play['complete_pass'] == 1 and play['yards_gained'] > 0:
                        arrow_length = min(abs(play['yards_gained']), 100 - start_yard)
                        ax.arrow(start_yard, y_pos, arrow_length, 0,
                               head_width=3, head_length=2, fc=color, ec=edge_color, 
                               linewidth=2.5, alpha=0.7, zorder=5)
                
                # Enhanced legend
                ax.scatter([], [], c='#FFD700', s=350, marker='*', label=' TD Pass', 
                          edgecolors='#FF0000', linewidths=3)
                ax.scatter([], [], c='#00FF41', s=150, marker='o', label=' Complete', 
                          edgecolors='white', linewidths=2)
                ax.scatter([], [], c='#FF4444', s=80, marker='x', label=' Incomplete', 
                          edgecolors='white', linewidths=2)
                ax.legend(loc='upper left', fontsize=13, facecolor='#0a0a0f', edgecolor='#FFD700', 
                         labelcolor='white', framealpha=0.95, borderpad=1.5, handletextpad=1.5)
                
                ax.set_title(f'{game["passer_player_name"]} - Pass Chart', 
                           fontsize=20, color='#FFD700', fontweight='bold', pad=15)
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            with col2:
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{int(game['yards_gained'])}</div>
                    <div class="stat-label">PASS YARDS</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{int(game['pass_touchdown'])}</div>
                    <div class="stat-label">TOUCHDOWNS</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{int(game['complete_pass'])}/{int(game['pass_attempt'])}</div>
                    <div class="stat-label">COMPLETIONS</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{(game['complete_pass']/game['pass_attempt']*100):.1f}%</div>
                    <div class="stat-label">COMPLETION %</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
        
        # RUNNING BACK HIGHLIGHTS
        st.markdown("###  ELITE RUNNING BACK PERFORMANCES")
        st.info(" Top 5 single-game RB performances ranked by total yards + TD bonus")
        
        rb_data = df_filtered[df_filtered['rusher_player_name'].notna()].copy()
        
        rb_games = rb_data.groupby(['rusher_player_name', 'game_id', 'game_date', 'posteam']).agg({
            'rush_touchdown': 'sum',
            'yards_gained': 'sum',
            'rush_attempt': 'sum',
            'epa': 'sum'
        }).reset_index()
        
        rb_games = rb_games[rb_games['rush_attempt'] >= 8]  # Min 8 attempts
        rb_games['performance_score'] = rb_games['yards_gained'] + (rb_games['rush_touchdown'] * 80)
        top_rb_games = rb_games.nlargest(5, 'performance_score')
        
        for rank, (idx, game) in enumerate(top_rb_games.iterrows(), 1):
            st.markdown(f"""
            <div class="highlight-card">
                <div class="player-name">#{rank} - {game['rusher_player_name']} ({game['posteam']})</div>
                <div class="game-date"> {game['game_date'].strftime('%B %d, %Y') if hasattr(game['game_date'], 'strftime') else game['game_date']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                game_rushes = rb_data[
                    (rb_data['game_id'] == game['game_id']) & 
                    (rb_data['rusher_player_name'] == game['rusher_player_name']) &
                    (rb_data['yardline_100'].notna())
                ].copy()
                
                fig, ax = plt.subplots(figsize=(18, 7))
                fig.patch.set_facecolor('#0a0a0f')
                draw_field(ax)
                
                rush_count = 0
                for _, play in game_rushes.iterrows():
                    start_yard = 100 - play['yardline_100']
                    yards = play['yards_gained']
                    
                    # Better lane distribution
                    lane = rush_count % 4
                    y_pos = 15 + lane * 8.5
                    rush_count += 1
                    
                    if play['rush_touchdown'] == 1:
                        color = '#FFD700'
                        size = 400
                        marker = '*'
                        alpha = 1.0
                        edge_width = 3
                    elif yards >= 15:
                        color = '#00FF41'
                        size = 250
                        marker = 'D'
                        alpha = 0.9
                        edge_width = 2.5
                    elif yards >= 5:
                        color = '#00D9FF'
                        size = 150
                        marker = 'o'
                        alpha = 0.8
                        edge_width = 2
                    else:
                        color = '#FF4444'
                        size = 100
                        marker = 'x'
                        alpha = 0.7
                        edge_width = 2
                    
                    ax.scatter(start_yard, y_pos, c=color, s=size, marker=marker,
                             edgecolors='white', linewidths=edge_width, zorder=6, alpha=alpha)
                    
                    if yards > 0:
                        end_yard = min(start_yard + yards, 100)
                        ax.arrow(start_yard, y_pos, end_yard - start_yard, 0,
                               head_width=3, head_length=2, fc=color, ec='white', 
                               linewidth=2.5, alpha=0.7, zorder=5)
                
                ax.scatter([], [], c='#FFD700', s=350, marker='*', label=' TD Rush', edgecolors='white', linewidths=3)
                ax.scatter([], [], c='#00FF41', s=200, marker='D', label=' 15+ Yards', edgecolors='white', linewidths=2)
                ax.scatter([], [], c='#00D9FF', s=120, marker='o', label=' 5+ Yards', edgecolors='white', linewidths=2)
                ax.scatter([], [], c='#FF4444', s=70, marker='x', label=' < 5 Yards', edgecolors='white', linewidths=2)
                ax.legend(loc='upper left', fontsize=13, facecolor='#0a0a0f', edgecolor='#FFD700', 
                         labelcolor='white', framealpha=0.95, borderpad=1.5)
                
                ax.set_title(f'{game["rusher_player_name"]} - Rush Chart', 
                           fontsize=20, color='#FFD700', fontweight='bold', pad=15)
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            with col2:
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{int(game['yards_gained'])}</div>
                    <div class="stat-label">RUSH YARDS</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{int(game['rush_touchdown'])}</div>
                    <div class="stat-label">TOUCHDOWNS</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{int(game['rush_attempt'])}</div>
                    <div class="stat-label">ATTEMPTS</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{(game['yards_gained']/game['rush_attempt']):.1f}</div>
                    <div class="stat-label">YARDS/CARRY</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
        
        # WIDE RECEIVER HIGHLIGHTS
        st.markdown("###  ELITE WIDE RECEIVER PERFORMANCES")
        st.info(" Top 5 single-game WR performances ranked by receiving yards + TD bonus")
        
        wr_data = df_filtered[df_filtered['receiver_player_name'].notna()].copy()
        
        wr_games = wr_data.groupby(['receiver_player_name', 'game_id', 'game_date', 'posteam']).agg({
            'pass_touchdown': 'sum',
            'yards_gained': 'sum',
            'complete_pass': 'sum',
            'epa': 'sum'
        }).reset_index()
        
        wr_games = wr_games[wr_games['complete_pass'] >= 4]  # Min 4 receptions
        wr_games['performance_score'] = wr_games['yards_gained'] + (wr_games['pass_touchdown'] * 100)
        top_wr_games = wr_games.nlargest(5, 'performance_score')
        
        for rank, (idx, game) in enumerate(top_wr_games.iterrows(), 1):
            st.markdown(f"""
            <div class="highlight-card">
                <div class="player-name">#{rank} - {game['receiver_player_name']} ({game['posteam']})</div>
                <div class="game-date"> {game['game_date'].strftime('%B %d, %Y') if hasattr(game['game_date'], 'strftime') else game['game_date']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                game_recs = wr_data[
                    (wr_data['game_id'] == game['game_id']) & 
                    (wr_data['receiver_player_name'] == game['receiver_player_name']) &
                    (wr_data['complete_pass'] == 1) &
                    (wr_data['yardline_100'].notna())
                ].copy()
                
                fig, ax = plt.subplots(figsize=(18, 7))
                fig.patch.set_facecolor('#0a0a0f')
                draw_field(ax)
                
                rec_count = 0
                for _, play in game_recs.iterrows():
                    start_yard = 100 - play['yardline_100']
                    yards = play['yards_gained']
                    
                    # Enhanced zone distribution
                    zone = rec_count % 5
                    y_pos = 11 + zone * 8.5
                    rec_count += 1
                    
                    if play['pass_touchdown'] == 1:
                        color = '#FFD700'
                        size = 450
                        marker = '*'
                        alpha = 1.0
                        edge_width = 3
                    elif yards >= 25:
                        color = '#00FF41'
                        size = 280
                        marker = 'D'
                        alpha = 0.9
                        edge_width = 2.5
                    elif yards >= 10:
                        color = '#00D9FF'
                        size = 180
                        marker = 'o'
                        alpha = 0.8
                        edge_width = 2
                    else:
                        color = '#9D4EDD'
                        size = 120
                        marker = 'o'
                        alpha = 0.75
                        edge_width = 2
                    
                    ax.scatter(start_yard, y_pos, c=color, s=size, marker=marker,
                             edgecolors='white', linewidths=edge_width, zorder=6, alpha=alpha)
                    
                    if yards > 0:
                        end_yard = min(start_yard + yards, 100)
                        ax.arrow(start_yard, y_pos, end_yard - start_yard, 0,
                               head_width=3, head_length=2.5, fc=color, ec='white', 
                               linewidth=2.5, alpha=0.7, zorder=5)
                
                ax.scatter([], [], c='#FFD700', s=400, marker='*', label=' TD Catch', edgecolors='white', linewidths=3)
                ax.scatter([], [], c='#00FF41', s=220, marker='D', label=' 25+ Yards', edgecolors='white', linewidths=2)
                ax.scatter([], [], c='#00D9FF', s=150, marker='o', label=' 10+ Yards', edgecolors='white', linewidths=2)
                ax.scatter([], [], c='#9D4EDD', s=100, marker='o', label=' < 10 Yards', edgecolors='white', linewidths=2)
                ax.legend(loc='upper left', fontsize=13, facecolor='#0a0a0f', edgecolor='#FFD700', 
                         labelcolor='white', framealpha=0.95, borderpad=1.5)
                
                ax.set_title(f'{game["receiver_player_name"]} - Reception Chart', 
                           fontsize=20, color='#FFD700', fontweight='bold', pad=15)
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            with col2:
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{int(game['yards_gained'])}</div>
                    <div class="stat-label">REC YARDS</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{int(game['pass_touchdown'])}</div>
                    <div class="stat-label">TOUCHDOWNS</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{int(game['complete_pass'])}</div>
                    <div class="stat-label">RECEPTIONS</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{(game['yards_gained']/max(game['complete_pass'], 1)):.1f}</div>
                    <div class="stat-label">YARDS/REC</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"""
        ### ❌ Application Error
        
        An error occurred while running the dashboard: 
        
        ```
        {str(e)}
        ```
        
        **This is likely because:**
        - The dataset file is missing (required for cloud deployment)
        - See instructions above for local setup
        
        For local development, make sure you have:
        1. Downloaded the NFL dataset
        2. Placed it in the `datasets/` folder
        3. All dependencies installed from requirements.txt
        """)
        import traceback
        st.code(traceback.format_exc())

