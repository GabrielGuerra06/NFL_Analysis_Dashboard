
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point
import kagglehub
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="NFL Decade Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Professional Theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
    }
    h1 {
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Arial Black', sans-serif;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 900;
        animation: glow 2s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { filter: drop-shadow(0 0 5px #FFD700); }
        to { filter: drop-shadow(0 0 20px #FFA500); }
    }
    h2 {
        color: #00D9FF;
        font-family: 'Arial Black', sans-serif;
        font-weight: 800;
        border-bottom: 3px solid #FFD700;
        padding-bottom: 10px;
        margin-top: 2rem;
    }
    h3 {
        color: #FFD700;
        font-weight: 700;
        margin-top: 1.5rem;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    [data-testid="stMetricLabel"] {
        color: #00D9FF !important;
        font-weight: 700;
        font-size: 1.1rem !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #16213e;
        border-radius: 10px;
        padding: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: #1a1a2e;
        border-radius: 8px;
        color: #00D9FF;
        font-weight: 700;
        font-size: 1.1rem;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #16213e;
        border-color: #FFD700;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #000 !important;
        font-weight: 900;
        border: 2px solid #00D9FF;
    }
    .plot-container {
        background-color: #1a1a2e;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        border: 2px solid #FFD700;
        margin: 10px 0;
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
@st.cache_data(show_spinner=False)
def load_data():
    """Load NFL play-by-play data from 2009-2018"""
    path = kagglehub.dataset_download("maxhorowitz/nflplaybyplay2009to2016")
    df = pd.read_csv(path + "/NFL Play by Play 2009-2018 (v5).csv", low_memory=False)
    df['game_date'] = pd.to_datetime(df['game_date'])
    df['year'] = df['game_date'].dt.year
    df = df[(df['year'] >= 2009) & (df['year'] <= 2018)].copy()
    return df

def main():
    # Header
    st.markdown("<h1> NFL DECADE SUMMARY DASHBOARD (2009-2018) </h1>", unsafe_allow_html=True)
    
    # Load data with spinner
    with st.spinner('Loading NFL dataset...'):
        df = load_data()
    
    st.markdown("##  INTRODUCTION")
    st.markdown("The american football is one of the most popular sports in United states, the NFL (National Football League) is well known for gathering gib data of almost all the plays in each game." \
                "The game consists of two teams competing to score points by advancing the ball into the opposing teams end zone, divided by offense and deffense, "
                "both of them have particular roles and positions, like Quarterback, Wide Receiver, Running back, etc. consist on 17 games in the season and the best teams"
                "of each division classify to playoffs, this games consist on 4 quarters of 15 minutes each of them, when a team is attacking, the drive have many options in which it can end"
                "The first one is a Touchdown which means 6 points plus the extra point (7 total points), a field goal which is a kick to the opposite field (3 points) or the drive can end"
                "punting the football or being intercepted/fumbled by the other defense. With this data we can analyze the performance of each team and player through the years.")

    st.markdown("In This dashboard we will present the most relevant statistics and visualizations from a decade of NFL play by play data." \
    "The objective is to explore the team performances, player stats, like the best running backs, wide receivers and defense. " \
    "You will be able to filter by your favorite teams, compare your players performances and see how the NFL evolved through the years.")


    # Sidebar Filters - IMPROVED VERSION
    st.sidebar.markdown("##   DASHBOARD FILTERS")
    st.sidebar.markdown("---")
    
    # Text input for single team search
    st.sidebar.markdown("###  Quick Team Search")
    team_search = st.sidebar.text_input(
        "Enter Team Code (e.g., NE, DAL, GB):",
        value="",
        help="Enter a single team code to analyze just that team"
    ).upper().strip()
    
    # Year filter
    years = sorted(df['year'].unique())
    selected_years = st.sidebar.multiselect(
        " Select Years:",
        options=years,
        default=years,
        help="Filter data by season"
    )
    
    # Team filter (conditional based on text input)
    teams = sorted([t for t in df['posteam'].unique() if pd.notna(t) and t in NFL_COLORS])
    if team_search and team_search in teams:
        selected_teams = [team_search]
        st.sidebar.success(f"Filtering by: {NFL_NAMES.get(team_search, team_search)}")
    else:
        selected_teams = st.sidebar.multiselect(
            " Select Teams:",
            options=teams,
            default=teams,
            format_func=lambda x: NFL_NAMES.get(x, x),
            help="Filter data by team"
        )
        if team_search:
            st.sidebar.error(f"Team '{team_search}' not found. Please use valid codes.")
    
    # Apply filters
    df_filtered = df[
        (df['year'].isin(selected_years)) &
        (df['posteam'].isin(selected_teams))
    ].copy()
    
    # Global KPIs
    st.markdown("##  GLOBAL STATISTICS")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric(" Total Plays", f"{len(df_filtered):,}")
    with col2:
        st.metric(" Games", f"{df_filtered['game_id'].nunique():,}")
    with col3:
        st.metric(" Touchdowns", f"{int(df_filtered['touchdown'].sum()):,}")
    with col4:
        st.metric(" Total Yards", f"{int(df_filtered['yards_gained'].sum()):,}")
    with col5:
        st.metric(" Teams", f"{df_filtered['posteam'].nunique()}")
    with col6:
        st.metric(" Years", f"{df_filtered['year'].nunique()}")
    
    st.markdown("First of all lets explore and understand our data, we have a total of 417,172 plays only in the 17 normal games of this years, this means 2,524 total games, " \
    "being more specific per week 15 games are played aprox. (17 weeks x 15 games  = 255) and we are analyzing 10 years (255 games per  x 10 years = 2550 aprox), in this 2524 games they were a total of " \
    "12,378 touchdowns. This means per game we had 4.9 touchdowns aprox, between both teams playing, the touchdowns and total plays generated 1,684,852 total yards. " )

    st.warning("Its important to specify that the data set contained only the offensive yards, we are not considering the touchdonws by deffense or special teams, so it may defear with the official NFL data " )
    st.markdown("---")
    
    # INTRODUCTION WITH GEOGRAPHIC MAP - STORYTELLING
    st.markdown("##   NFL TEAMS GEOGRAPHIC DISTRIBUTION")
    st.markdown("#### To start our analysis we wanted to visualize the geographic distribution of NFL teams across the United States, so you can understand how popular this sport is how is established the NFL teams across the country.")

    st.markdown("###### Its important to notice that the teams are approximated by the location of the Stadium, as they are multiple teams from the same state, we wanted to leave just the" \
    " main location of each team.")

    st.info("###### We have a total of 32 teams, distributed across various states in the USA, to explore this plot, you can make zoom to the map and hover the dot of each team, the total touchdown, yards and plays of that team.")
    

    
    # Create GeoDataFrame for map
    teams_data = []
    for team, coords in NFL_LOCATIONS.items():
        if team in NFL_COLORS and team in selected_teams:
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
        
        # Create map with Plotly
        fig_map = go.Figure()
        
        for idx, row in gdf.iterrows():
            fig_map.add_trace(go.Scattergeo(
                lon=[row['lon']],
                lat=[row['lat']],
                mode='markers+text',
                marker=dict(
                    size=20 + (row['touchdowns'] / 50) if row['touchdowns'] > 0 else 15,
                    color=row['color'],
                    line=dict(width=3, color='white'),
                    symbol='circle'
                ),
                text=row['team'],
                textposition='top center',
                textfont=dict(size=12, color='white', family='Arial Black'),
                name=row['name'],
                hovertemplate=f"<b>{row['name']}</b><br>" +
                             f"Touchdowns: {row['touchdowns']:,}<br>" +
                             f"Total Yards: {row['yards']:,}<br>" +
                             f"Total Plays: {row['plays']:,}<extra></extra>"
            ))
        
        fig_map.update_layout(
            title=dict(
                text='<b>NFL TEAMS ACROSS THE UNITED STATES</b>',
                font=dict(size=26, color='white', family='Arial Black'),
                x=0.5
            ),
            geo=dict(
                scope='usa',
                projection_type='albers usa',
                showland=True,
                landcolor='#1a1a2e',
                coastlinecolor='#FFD700',
                coastlinewidth=2,
                showlakes=True,
                lakecolor='#0a0a0f',
                showcountries=True,
                countrycolor='#FFD700',
                bgcolor='#0a0a0f',
                showsubunits=True,
                subunitcolor='#FFD700'
            ),
            height=600,
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            showlegend=False
        )
        
        st.plotly_chart(fig_map, width='stretch')
    
    st.markdown("---")
    
    # MAIN TABS
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        " TEAM PERFORMANCE",
        " QUARTERBACK STATS",
        " RUNNING BACKS",
        " WIDE RECEIVERS",
        " DEFENSE ANALYSIS",
        " SEABORN ANALYSIS"
    ])
    
    # TAB 1: TEAM PERFORMANCE WITH RACING BAR
    with tab1:
        st.markdown("##  TEAM PERFORMANCE ANALYSIS")
        
        # RACING BAR CHART - Most Winning Teams
        st.markdown("###  Racing Bar: Team Performance Evolution (2009-2018)")
        st.markdown("_Watch how teams accumulated touchdowns year by year_")
        
        # Calculate cumulative touchdowns per team per year
        wins_by_year = {}
        for year in range(2009, 2019):
            year_data = df_filtered[df_filtered['year'] == year]
            team_tds = {}
            
            for team in selected_teams:
                tds = year_data[year_data['posteam'] == team]['touchdown'].sum()
                team_tds[team] = tds
            
            wins_by_year[year] = team_tds
        
        # Create animation frames
        frames = []
        cumulative_wins = {team: 0 for team in selected_teams}
        
        for year in range(2009, 2019):
            # Update cumulative
            for team, tds in wins_by_year[year].items():
                cumulative_wins[team] += tds
            
            # Get top 15
            sorted_teams = sorted(cumulative_wins.items(), key=lambda x: x[1], reverse=True)[:15]
            teams = [t[0] for t in sorted_teams]
            wins = [t[1] for t in sorted_teams]
            colors = [NFL_COLORS.get(t, '#FFD700') for t in teams]
            names = [NFL_NAMES.get(t, t) for t in teams]
            
            frame = go.Frame(
                data=[go.Bar(
                    y=names,
                    x=wins,
                    orientation='h',
                    marker=dict(color=colors, line=dict(color='white', width=2)),
                    text=[f"{int(w):,}" for w in wins],
                    textposition='outside',
                    textfont=dict(size=12, color='white', family='Arial Black')
                )],
                name=str(year),
                layout=go.Layout(title_text=f"<b>Cumulative Touchdowns through {year}</b>")
            )
            frames.append(frame)
        
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
            title='<b> RACING BAR: TEAM PERFORMANCE EVOLUTION</b>',
            xaxis=dict(title='Cumulative Touchdowns', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
            yaxis=dict(tickfont=dict(color='white', size=11)),
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            height=600,
            updatemenus=[{
                'type': 'buttons',
                'showactive': True,
                'buttons': [
                    {'label': '▶️ Play', 'method': 'animate',
                     'args': [None, {'frame': {'duration': 800, 'redraw': True}, 'fromcurrent': True}]},
                    {'label': '⏸️ Pause', 'method': 'animate',
                     'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}]}
                ],
                'x': 0.1, 'y': 1.15
            }],
            sliders=[{
                'active': 0,
                'steps': [{'args': [[f.name], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}],
                          'label': f.name, 'method': 'animate'} for f in frames],
                'x': 0.1, 'len': 0.9, 'y': 0
            }]
        )
        
        st.plotly_chart(fig_race_teams, width='stretch')
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Team Touchdowns
            team_tds = df_filtered.groupby('posteam')['touchdown'].sum().nlargest(15)
            fig_td = go.Figure()
            fig_td.add_trace(go.Bar(
                x=team_tds.values,
                y=[NFL_NAMES.get(t, t) for t in team_tds.index],
                orientation='h',
                marker=dict(
                    color=[NFL_COLORS.get(t, '#FFD700') for t in team_tds.index],
                    line=dict(color='white', width=2)
                ),
                text=team_tds.values,
                textposition='outside',
                textfont=dict(size=14, color='white', family='Arial Black')
            ))
            fig_td.update_layout(
                title=dict(text='<b>TOP 15 TEAMS - TOUCHDOWNS</b>', font=dict(size=20, color='white', family='Arial Black')),
                xaxis=dict(title='Touchdowns', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
                yaxis=dict(tickfont=dict(color='white', size=11)),
                plot_bgcolor='#1a1a2e',
                paper_bgcolor='#16213e',
                font=dict(color='white'),
                height=500
            )
            st.plotly_chart(fig_td, use_container_width=True)
        
        with col2:
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
            st.plotly_chart(fig_epa, use_container_width=True)
        
        # Yards Evolution Over Time
        st.markdown("###  Yards Evolution by Year")
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
        st.plotly_chart(fig_evolution, use_container_width=True)
    
    # TAB 2: QUARTERBACK STATS WITH RACING BAR
    with tab2:
        st.markdown("## 🎯 QUARTERBACK ANALYSIS")
        
        qb_data = df_filtered[df_filtered['passer_player_name'].notna()].copy()
        
        # RACING BAR CHART - Top QBs by Passing Yards
        st.markdown("### 🏆 Racing Bar: Top Quarterbacks by Passing Yards")
        st.markdown("_Watch the elite QBs accumulate passing yards throughout the decade_")
        
        # Calculate cumulative yards per QB per year
        qb_frames = []
        qb_cumulative = {}
        
        for year in range(2009, 2019):
            year_data = qb_data[qb_data['year'] <= year]
            qb_yards = year_data.groupby('passer_player_name')['yards_gained'].sum().nlargest(15)
            
            for qb in qb_yards.index:
                qb_cumulative[qb] = qb_yards[qb]
            
            sorted_qbs = sorted(qb_cumulative.items(), key=lambda x: x[1], reverse=True)[:15]
            qbs = [q[0] for q in sorted_qbs]
            yards = [q[1] for q in sorted_qbs]
            
            frame = go.Frame(
                data=[go.Bar(
                    y=qbs,
                    x=yards,
                    orientation='h',
                    marker=dict(color=yards, colorscale='Blues', line=dict(color='white', width=2)),
                    text=[f"{int(y):,}" for y in yards],
                    textposition='outside',
                    textfont=dict(size=11, color='white', family='Arial Black')
                )],
                name=str(year),
                layout=go.Layout(title_text=f"<b>QB Passing Yards through {year}</b>")
            )
            qb_frames.append(frame)
        
        # Initial QB figure
        initial_qb_data = qb_data[qb_data['year'] <= 2009].groupby('passer_player_name')['yards_gained'].sum().nlargest(15)
        
        fig_race_qb = go.Figure(
            data=[go.Bar(
                y=initial_qb_data.index,
                x=initial_qb_data.values,
                orientation='h',
                marker=dict(color=initial_qb_data.values, colorscale='Blues')
            )],
            frames=qb_frames
        )
        
        fig_race_qb.update_layout(
            title='<b>🎯 RACING BAR: TOP QUARTERBACKS BY PASSING YARDS</b>',
            xaxis=dict(title='Cumulative Passing Yards', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
            yaxis=dict(tickfont=dict(color='white', size=10)),
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            height=600,
            updatemenus=[{
                'type': 'buttons',
                'buttons': [
                    {'label': '▶️ Play', 'method': 'animate',
                     'args': [None, {'frame': {'duration': 800, 'redraw': True}}]},
                    {'label': '⏸️ Pause', 'method': 'animate',
                     'args': [[None], {'frame': {'duration': 0, 'redraw': False}}]}
                ],
                'x': 0.1, 'y': 1.15
            }],
            sliders=[{
                'steps': [{'args': [[f.name], {'frame': {'duration': 0, 'redraw': True}}],
                          'label': f.name, 'method': 'animate'} for f in qb_frames],
                'x': 0.1, 'len': 0.9
            }]
        )
        
        st.plotly_chart(fig_race_qb, width='stretch')
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top QBs by Passing Yards
            qb_yards = qb_data.groupby('passer_player_name')['yards_gained'].sum().nlargest(15)
            fig_qb_yards = go.Figure()
            fig_qb_yards.add_trace(go.Bar(
                y=qb_yards.index,
                x=qb_yards.values,
                orientation='h',
                marker=dict(
                    color=qb_yards.values,
                    colorscale='Blues',
                    line=dict(color='white', width=2)
                ),
                text=[f"{int(v):,}" for v in qb_yards.values],
                textposition='outside',
                textfont=dict(size=12, color='white', family='Arial Black')
            ))
            fig_qb_yards.update_layout(
                title=dict(text='<b>TOP 15 QBs - PASSING YARDS</b>', font=dict(size=20, color='white', family='Arial Black')),
                xaxis=dict(title='Passing Yards', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
                yaxis=dict(tickfont=dict(color='white', size=10)),
                plot_bgcolor='#1a1a2e',
                paper_bgcolor='#16213e',
                font=dict(color='white'),
                height=550
            )
            st.plotly_chart(fig_qb_yards, use_container_width=True)
        
        with col2:
            # QB Touchdowns
            qb_tds = qb_data.groupby('passer_player_name')['touchdown'].sum().nlargest(15)
            fig_qb_tds = go.Figure()
            fig_qb_tds.add_trace(go.Bar(
                y=qb_tds.index,
                x=qb_tds.values,
                orientation='h',
                marker=dict(
                    color=qb_tds.values,
                    colorscale='Reds',
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
            st.plotly_chart(fig_qb_tds, use_container_width=True)
        
        # QB Efficiency (EPA)
        st.markdown("### 📊 QB Efficiency - EPA Analysis")
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
        st.plotly_chart(fig_qb_epa, use_container_width=True)
    
    # TAB 3: RUNNING BACKS WITH RACING BAR
    with tab3:
        st.markdown("## 💨 RUNNING BACK ANALYSIS")
        
        rb_data = df_filtered[df_filtered['rusher_player_name'].notna()].copy()
        
        # RACING BAR CHART - Top RBs by Rushing Yards
        st.markdown("### 🏆 Racing Bar: Top Running Backs by Rushing Yards")
        st.markdown("_Watch the ground game dominate as RBs rack up yards_")
        
        # Calculate cumulative yards per RB per year
        rb_frames = []
        rb_cumulative = {}
        
        for year in range(2009, 2019):
            year_data = rb_data[rb_data['year'] <= year]
            rb_yards = year_data.groupby('rusher_player_name')['yards_gained'].sum().nlargest(15)
            
            for rb in rb_yards.index:
                rb_cumulative[rb] = rb_yards[rb]
            
            sorted_rbs = sorted(rb_cumulative.items(), key=lambda x: x[1], reverse=True)[:15]
            rbs = [r[0] for r in sorted_rbs]
            yards = [r[1] for r in sorted_rbs]
            
            frame = go.Frame(
                data=[go.Bar(
                    y=rbs,
                    x=yards,
                    orientation='h',
                    marker=dict(color=yards, colorscale='YlOrRd', line=dict(color='white', width=2)),
                    text=[f"{int(y):,}" for y in yards],
                    textposition='outside',
                    textfont=dict(size=11, color='white', family='Arial Black')
                )],
                name=str(year),
                layout=go.Layout(title_text=f"<b>RB Rushing Yards through {year}</b>")
            )
            rb_frames.append(frame)
        
        # Initial RB figure
        initial_rb_data = rb_data[rb_data['year'] <= 2009].groupby('rusher_player_name')['yards_gained'].sum().nlargest(15)
        
        fig_race_rb = go.Figure(
            data=[go.Bar(
                y=initial_rb_data.index,
                x=initial_rb_data.values,
                orientation='h',
                marker=dict(color=initial_rb_data.values, colorscale='YlOrRd')
            )],
            frames=rb_frames
        )
        
        fig_race_rb.update_layout(
            title='<b>💨 RACING BAR: TOP RUNNING BACKS BY RUSHING YARDS</b>',
            xaxis=dict(title='Cumulative Rushing Yards', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
            yaxis=dict(tickfont=dict(color='white', size=10)),
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            height=600,
            updatemenus=[{
                'type': 'buttons',
                'buttons': [
                    {'label': '▶️ Play', 'method': 'animate',
                     'args': [None, {'frame': {'duration': 800, 'redraw': True}}]},
                    {'label': '⏸️ Pause', 'method': 'animate',
                     'args': [[None], {'frame': {'duration': 0, 'redraw': False}}]}
                ],
                'x': 0.1, 'y': 1.15
            }],
            sliders=[{
                'steps': [{'args': [[f.name], {'frame': {'duration': 0, 'redraw': True}}],
                          'label': f.name, 'method': 'animate'} for f in rb_frames],
                'x': 0.1, 'len': 0.9
            }]
        )
        
        st.plotly_chart(fig_race_rb, width='stretch')
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top RBs by Rushing Yards
            rb_yards = rb_data.groupby('rusher_player_name')['yards_gained'].sum().nlargest(15)
            fig_rb_yards = go.Figure()
            fig_rb_yards.add_trace(go.Bar(
                y=rb_yards.index,
                x=rb_yards.values,
                orientation='h',
                marker=dict(
                    color=rb_yards.values,
                    colorscale='YlOrRd',
                    line=dict(color='white', width=2)
                ),
                text=[f"{int(v):,}" for v in rb_yards.values],
                textposition='outside',
                textfont=dict(size=12, color='white', family='Arial Black')
            ))
            fig_rb_yards.update_layout(
                title=dict(text='<b>TOP 15 RBs - RUSHING YARDS</b>', font=dict(size=20, color='white', family='Arial Black')),
                xaxis=dict(title='Rushing Yards', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
                yaxis=dict(tickfont=dict(color='white', size=10)),
                plot_bgcolor='#1a1a2e',
                paper_bgcolor='#16213e',
                font=dict(color='white'),
                height=550
            )
            st.plotly_chart(fig_rb_yards, use_container_width=True)
        
        with col2:
            # RB Touchdowns
            rb_tds = rb_data.groupby('rusher_player_name')['touchdown'].sum().nlargest(15)
            fig_rb_tds = go.Figure()
            fig_rb_tds.add_trace(go.Bar(
                x=[r for r in rb_tds.index],
                y=rb_tds.values,
                marker=dict(
                    color=rb_tds.values,
                    colorscale='Greens',
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
            st.plotly_chart(fig_rb_tds, use_container_width=True)
        
        # RB Yards per Carry
        st.markdown("### 📊 Yards per Carry Analysis")
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
        st.plotly_chart(fig_rb_ypc, use_container_width=True)
    
    # TAB 4: WIDE RECEIVERS
    with tab4:
        st.markdown("## 🏆 WIDE RECEIVER ANALYSIS")
        
        wr_data = df_filtered[df_filtered['receiver_player_name'].notna()].copy()
        
        st.markdown("### Top Wide Receivers by Receiving Yards")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top WRs by Receiving Yards
            wr_yards = wr_data.groupby('receiver_player_name')['yards_gained'].sum().nlargest(15)
            fig_wr_yards = go.Figure()
            fig_wr_yards.add_trace(go.Bar(
                y=wr_yards.index,
                x=wr_yards.values,
                orientation='h',
                marker=dict(
                    color=wr_yards.values,
                    colorscale='Purples',
                    line=dict(color='white', width=2)
                ),
                text=[f"{int(v):,}" for v in wr_yards.values],
                textposition='outside',
                textfont=dict(size=12, color='white', family='Arial Black')
            ))
            fig_wr_yards.update_layout(
                title=dict(text='<b>TOP 15 WRs - RECEIVING YARDS</b>', font=dict(size=20, color='white', family='Arial Black')),
                xaxis=dict(title='Receiving Yards', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
                yaxis=dict(tickfont=dict(color='white', size=10)),
                plot_bgcolor='#1a1a2e',
                paper_bgcolor='#16213e',
                font=dict(color='white'),
                height=550
            )
            st.plotly_chart(fig_wr_yards, use_container_width=True)
        
        with col2:
            # WR Touchdowns
            wr_tds = wr_data.groupby('receiver_player_name')['touchdown'].sum().nlargest(15)
            fig_wr_tds = go.Figure()
            fig_wr_tds.add_trace(go.Bar(
                x=[r for r in wr_tds.index],
                y=wr_tds.values,
                marker=dict(
                    color=wr_tds.values,
                    colorscale='Oranges',
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
            st.plotly_chart(fig_wr_tds, use_container_width=True)
        
        # WR Receptions and Yards per Reception
        st.markdown("### 📊 Reception Efficiency Analysis")
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
        st.plotly_chart(fig_wr_efficiency, use_container_width=True)
    
    # TAB 5: DEFENSE ANALYSIS
    with tab5:
        st.markdown("## 🛡️ DEFENSE ANALYSIS")
        
        st.markdown("### Best Defensive Performances")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Teams with most interceptions
            int_data = df_filtered[df_filtered['interception'] == 1]
            team_ints = int_data.groupby('defteam')['interception'].sum().nlargest(15)
            fig_ints = go.Figure()
            fig_ints.add_trace(go.Bar(
                x=team_ints.values,
                y=[NFL_NAMES.get(t, t) for t in team_ints.index],
                orientation='h',
                marker=dict(
                    color=[NFL_COLORS.get(t, '#00D9FF') for t in team_ints.index],
                    line=dict(color='white', width=2)
                ),
                text=team_ints.values,
                textposition='outside',
                textfont=dict(size=14, color='white', family='Arial Black')
            ))
            fig_ints.update_layout(
                title=dict(text='<b>TOP 15 TEAMS - INTERCEPTIONS</b>', font=dict(size=20, color='white', family='Arial Black')),
                xaxis=dict(title='Interceptions', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
                yaxis=dict(tickfont=dict(color='white', size=11)),
                plot_bgcolor='#1a1a2e',
                paper_bgcolor='#16213e',
                font=dict(color='white'),
                height=550
            )
            st.plotly_chart(fig_ints, use_container_width=True)
        
        with col2:
            # Teams with most sacks
            sack_data = df_filtered[df_filtered['sack'] == 1]
            team_sacks = sack_data.groupby('defteam')['sack'].sum().nlargest(15)
            fig_sacks = go.Figure()
            fig_sacks.add_trace(go.Bar(
                x=[NFL_NAMES.get(t, t) for t in team_sacks.index],
                y=team_sacks.values,
                marker=dict(
                    color=[NFL_COLORS.get(t, '#FF6B6B') for t in team_sacks.index],
                    line=dict(color='white', width=2)
                ),
                text=team_sacks.values,
                textposition='outside',
                textfont=dict(size=14, color='white', family='Arial Black')
            ))
            fig_sacks.update_layout(
                title=dict(text='<b>TOP 15 TEAMS - SACKS</b>', font=dict(size=20, color='white', family='Arial Black')),
                xaxis=dict(tickfont=dict(color='white', size=10), tickangle=-45),
                yaxis=dict(title='Sacks', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
                plot_bgcolor='#1a1a2e',
                paper_bgcolor='#16213e',
                font=dict(color='white'),
                height=550
            )
            st.plotly_chart(fig_sacks, use_container_width=True)
        
        # Defensive EPA Analysis
        st.markdown("### 📊 Defensive Efficiency (EPA Allowed)")
        def_epa = df_filtered.groupby('defteam')['epa'].mean().nsmallest(15)  # Lower EPA is better for defense
        
        fig_def_epa = go.Figure()
        fig_def_epa.add_trace(go.Bar(
            x=[NFL_NAMES.get(t, t) for t in def_epa.index],
            y=def_epa.values,
            marker=dict(
                color=[NFL_COLORS.get(t, '#4ECDC4') for t in def_epa.index],
                line=dict(color='white', width=2)
            ),
            text=[f"{v:.3f}" for v in def_epa.values],
            textposition='outside',
            textfont=dict(size=12, color='white', family='Arial Black')
        ))
        fig_def_epa.update_layout(
            title=dict(text='<b>TOP 15 DEFENSES - LOWEST EPA ALLOWED</b>', font=dict(size=22, color='white', family='Arial Black')),
            xaxis=dict(tickfont=dict(color='white', size=10), tickangle=-45),
            yaxis=dict(title='Average EPA Allowed', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#16213e',
            font=dict(color='white'),
            height=600
        )
        fig_def_epa.update_yaxes(autorange="reversed")  # Reverse to show best at top
        st.plotly_chart(fig_def_epa, use_container_width=True)
        
        # Fumbles and Turnovers
        st.markdown("### 🏈 Turnovers and Fumbles")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Fumbles recovered by defense
            fumble_data = df_filtered[df_filtered['fumble_lost'] == 1]
            team_fumbles = fumble_data.groupby('defteam')['fumble_lost'].sum().nlargest(15)
            fig_fumbles = go.Figure()
            fig_fumbles.add_trace(go.Bar(
                y=team_fumbles.index,
                x=team_fumbles.values,
                orientation='h',
                marker=dict(
                    color='#A78BFA',
                    line=dict(color='white', width=2)
                ),
                text=team_fumbles.values,
                textposition='outside',
                textfont=dict(size=12, color='white', family='Arial Black')
            ))
            fig_fumbles.update_layout(
                title=dict(text='<b>TOP 15 - FUMBLES RECOVERED</b>', font=dict(size=18, color='white', family='Arial Black')),
                xaxis=dict(title='Fumbles', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
                yaxis=dict(tickfont=dict(color='white', size=10)),
                plot_bgcolor='#1a1a2e',
                paper_bgcolor='#16213e',
                font=dict(color='white'),
                height=500
            )
            st.plotly_chart(fig_fumbles, use_container_width=True)
        
        with col2:
            # Total Turnovers forced
            turnovers = df_filtered.copy()
            turnovers['turnover'] = (turnovers['interception'] == 1) | (turnovers['fumble_lost'] == 1)
            team_turnovers = turnovers.groupby('defteam')['turnover'].sum().nlargest(15)
            fig_turnovers = go.Figure()
            fig_turnovers.add_trace(go.Bar(
                x=[NFL_NAMES.get(t, t) for t in team_turnovers.index],
                y=team_turnovers.values,
                marker=dict(
                    color=[NFL_COLORS.get(t, '#FFA500') for t in team_turnovers.index],
                    line=dict(color='white', width=2)
                ),
                text=team_turnovers.values,
                textposition='outside',
                textfont=dict(size=12, color='white', family='Arial Black')
            ))
            fig_turnovers.update_layout(
                title=dict(text='<b>TOP 15 - TOTAL TURNOVERS FORCED</b>', font=dict(size=18, color='white', family='Arial Black')),
                xaxis=dict(tickfont=dict(color='white', size=9), tickangle=-45),
                yaxis=dict(title='Turnovers', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white')),
                plot_bgcolor='#1a1a2e',
                paper_bgcolor='#16213e',
                font=dict(color='white'),
                height=500
            )
            st.plotly_chart(fig_turnovers, use_container_width=True)
    
    # TAB 6: SEABORN ANALYSIS
    with tab6:
        st.markdown("## 🎨 SEABORN STATISTICAL ANALYSIS")
        
        # Set seaborn style
        sns.set_style("darkgrid")
        
        # Create figure with seaborn plots
        fig, axes = plt.subplots(2, 3, figsize=(22, 14))
        fig.patch.set_facecolor('#16213e')
        
        # 1. Boxplot - EPA by Play Type
        ax1 = axes[0, 0]
        play_types_top = df_filtered['play_type'].value_counts().head(5).index
        plot_data = df_filtered[df_filtered['play_type'].isin(play_types_top)]
        sns.boxplot(data=plot_data, x='play_type', y='epa', palette='Set2', ax=ax1, linewidth=2.5)
        ax1.set_title('Boxplot: EPA Distribution by Play Type', fontsize=16, color='#FFD700', fontweight='bold', pad=15)
        ax1.set_xlabel('Play Type', fontsize=14, color='white', fontweight='bold')
        ax1.set_ylabel('EPA', fontsize=14, color='white', fontweight='bold')
        ax1.set_facecolor('#1a1a2e')
        ax1.tick_params(colors='white', labelsize=11)
        ax1.grid(True, alpha=0.2, color='white', linestyle='--')
        for label in ax1.get_xticklabels():
            label.set_rotation(15)
        
        # 2. Violinplot - Yards by Down
        ax2 = axes[0, 1]
        down_data = df_filtered[df_filtered['down'].isin([1, 2, 3, 4])]
        sns.violinplot(data=down_data, x='down', y='yards_gained', palette='muted', ax=ax2, linewidth=2)
        ax2.set_title('Violinplot: Yards Distribution by Down', fontsize=16, color='#FFD700', fontweight='bold', pad=15)
        ax2.set_xlabel('Down', fontsize=14, color='white', fontweight='bold')
        ax2.set_ylabel('Yards Gained', fontsize=14, color='white', fontweight='bold')
        ax2.set_facecolor('#1a1a2e')
        ax2.tick_params(colors='white', labelsize=11)
        ax2.grid(True, alpha=0.2, color='white', axis='y', linestyle='--')
        ax2.set_ylim(-20, 60)
        
        # 3. Heatmap - Correlation Matrix
        ax3 = axes[0, 2]
        corr_cols = ['yards_gained', 'epa', 'wp', 'wpa', 'air_yards']
        corr_data = df_filtered[corr_cols].corr()
        sns.heatmap(corr_data, annot=True, cmap='RdYlGn', center=0, ax=ax3,
                   cbar_kws={'label': 'Correlation'}, fmt='.3f', linewidths=2, linecolor='white',
                   annot_kws={'size': 11, 'weight': 'bold'})
        ax3.set_title('Heatmap: Correlation Matrix', fontsize=16, color='#FFD700', fontweight='bold', pad=15)
        ax3.tick_params(colors='white', labelsize=10)
        
        # 4. Regplot - EPA vs Air Yards
        ax4 = axes[1, 0]
        reg_data = df_filtered[df_filtered['air_yards'].notna()].sample(min(1500, len(df_filtered)))
        sns.regplot(data=reg_data, x='air_yards', y='epa', scatter_kws={'alpha':0.4, 's':40, 'edgecolor':'white'},
                   line_kws={'color':'#FFD700', 'linewidth':4}, ax=ax4, color='#00D9FF')
        ax4.set_title('Regression Plot: EPA vs Air Yards', fontsize=16, color='#FFD700', fontweight='bold', pad=15)
        ax4.set_xlabel('Air Yards', fontsize=14, color='white', fontweight='bold')
        ax4.set_ylabel('EPA', fontsize=14, color='white', fontweight='bold')
        ax4.set_facecolor('#1a1a2e')
        ax4.tick_params(colors='white', labelsize=11)
        ax4.grid(True, alpha=0.2, color='white', linestyle='--')
        
        # 5. KDE Plot - Yards Distribution
        ax5 = axes[1, 1]
        yards_data = df_filtered[df_filtered['yards_gained'].between(-10, 50)]['yards_gained']
        sns.kdeplot(data=yards_data, fill=True, color='#4ECDC4', alpha=0.7, ax=ax5, linewidth=3)
        ax5.set_title('KDE Plot: Yards Gained Distribution', fontsize=16, color='#FFD700', fontweight='bold', pad=15)
        ax5.set_xlabel('Yards Gained', fontsize=14, color='white', fontweight='bold')
        ax5.set_ylabel('Density', fontsize=14, color='white', fontweight='bold')
        ax5.set_facecolor('#1a1a2e')
        ax5.tick_params(colors='white', labelsize=11)
        ax5.grid(True, alpha=0.2, color='white', linestyle='--')
        ax5.axvline(x=yards_data.mean(), color='#FFD700', linestyle='--', linewidth=3, label=f'Mean: {yards_data.mean():.2f}')
        ax5.legend(facecolor='#1a1a2e', edgecolor='white', fontsize=11)
        
        # 6. Countplot - Plays by Quarter
        ax6 = axes[1, 2]
        sns.countplot(data=df_filtered, x='qtr', palette='rocket', ax=ax6, edgecolor='white', linewidth=2)
        ax6.set_title('Countplot: Plays by Quarter', fontsize=16, color='#FFD700', fontweight='bold', pad=15)
        ax6.set_xlabel('Quarter', fontsize=14, color='white', fontweight='bold')
        ax6.set_ylabel('Number of Plays', fontsize=14, color='white', fontweight='bold')
        ax6.set_facecolor('#1a1a2e')
        ax6.tick_params(colors='white', labelsize=11)
        ax6.grid(True, alpha=0.2, color='white', axis='y', linestyle='--')
        for container in ax6.containers:
            ax6.bar_label(container, color='white', fontweight='bold', fontsize=10)
        
        plt.tight_layout(pad=3.0)
        st.pyplot(fig)
        plt.close()
        
        # Additional Seaborn Analysis
        st.markdown("### 📊 Pass vs Rush Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pass_rush, ax = plt.subplots(figsize=(10, 6))
            fig_pass_rush.patch.set_facecolor('#16213e')
            
            pass_rush_data = df_filtered[df_filtered['play_type'].isin(['pass', 'run'])].copy()
            sns.boxplot(data=pass_rush_data, x='play_type', y='yards_gained', 
                       hue='play_type', palette=['#FF6B6B', '#4ECDC4'], ax=ax, linewidth=2.5)
            ax.set_title('Pass vs Rush: Yards Distribution', fontsize=18, color='#FFD700', fontweight='bold', pad=15)
            ax.set_xlabel('Play Type', fontsize=14, color='white', fontweight='bold')
            ax.set_ylabel('Yards Gained', fontsize=14, color='white', fontweight='bold')
            ax.set_facecolor('#1a1a2e')
            ax.tick_params(colors='white', labelsize=12)
            ax.grid(True, alpha=0.2, color='white', linestyle='--')
            ax.set_ylim(-20, 60)
            ax.legend().remove()
            
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
            ax.axhline(y=0, color='#FFD700', linestyle='--', linewidth=2)
            
            plt.tight_layout()
            st.pyplot(fig_time)
            plt.close()
    

if __name__ == "__main__":
    main()
