"""
Prepare a cloud-compatible version of the NFL dataset
This script samples and compresses the data to fit within Streamlit Cloud's constraints
"""

import pandas as pd
import pickle
from pathlib import Path

def create_cloud_dataset():
    """Create a compressed, sampled dataset for cloud deployment"""
    
    print("Loading full dataset...")
    df = pd.read_csv("datasets/NFL Play by Play 2009-2018 (v5).csv", low_memory=False)
    
    print(f"Original dataset: {len(df):,} rows, {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    # Strategy: Keep all games but optimize data types and columns
    # Remove columns that aren't used in visualizations
    
    # Essential columns for the dashboard (comprehensive list - updated v3)
    essential_columns = [
        # Game identifiers
        'game_id', 'play_id', 'game_date', 'qtr', 'posteam', 'defteam', 'home_team', 'away_team',
        
        # Play details
        'yards_gained', 'play_type', 'down', 'ydstogo', 'yardline_100',
        
        # Scoring
        'touchdown', 'pass_touchdown', 'rush_touchdown',
        'field_goal_result', 'extra_point_result', 'two_point_conv_result',
        
        # Turnovers and defense
        'interception', 'fumble', 'fumble_lost', 'fumble_recovery_1_team', 
        'sack', 'qb_hit', 'safety',
        
        # Pass specific
        'pass_attempt', 'complete_pass', 'incomplete_pass', 'air_yards', 'yards_after_catch',
        
        # Rush specific
        'rush_attempt',
        
        # Offensive players
        'passer_player_name', 'rusher_player_name', 'receiver_player_name',
        
        # Defensive players
        'interception_player_name', 
        'solo_tackle_1_player_name', 'solo_tackle_2_player_name',
        'assist_tackle_1_player_name', 'assist_tackle_2_player_name',
        
        # Advanced metrics
        'epa', 'wpa', 'wp',
        
        # Time
        'quarter_seconds_remaining', 'half_seconds_remaining', 'game_seconds_remaining',
        
        # Score
        'score_differential'
    ]
    
    # Keep only essential columns that exist
    available_columns = [col for col in essential_columns if col in df.columns]
    df_sampled = df[available_columns].copy()
    
    # Convert datetime
    df_sampled['game_date'] = pd.to_datetime(df_sampled['game_date'])
    df_sampled['year'] = df_sampled['game_date'].dt.year
    
    # Filter years
    df_sampled = df_sampled[(df_sampled['year'] >= 2009) & (df_sampled['year'] <= 2018)]
    
    # Consolidate SD to LAC
    df_sampled['posteam'] = df_sampled['posteam'].replace('SD', 'LAC')
    df_sampled['defteam'] = df_sampled['defteam'].replace('SD', 'LAC')
    
    # Optimize dtypes
    # Convert object columns to category where appropriate
    for col in ['posteam', 'defteam', 'home_team', 'away_team', 'play_type']:
        if col in df_sampled.columns:
            df_sampled[col] = df_sampled[col].astype('category')
    
    # Convert float64 to float32 where possible
    float_cols = df_sampled.select_dtypes(include=['float64']).columns
    for col in float_cols:
        df_sampled[col] = df_sampled[col].astype('float32')
    
    # Convert int64 to int32 where possible
    int_cols = df_sampled.select_dtypes(include=['int64']).columns
    for col in int_cols:
        if df_sampled[col].min() >= -2147483648 and df_sampled[col].max() <= 2147483647:
            df_sampled[col] = df_sampled[col].astype('int32')
    
    print(f"Optimized dataset: {len(df_sampled):,} rows, {df_sampled.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    # Save as compressed pickle (much smaller than CSV)
    output_file = Path("datasets/nfl_data_cloud.pkl.gz")
    output_file.parent.mkdir(exist_ok=True)
    
    df_sampled.to_pickle(output_file, compression='gzip')
    
    file_size_mb = output_file.stat().st_size / 1024**2
    print(f"Saved to {output_file}")
    print(f"File size: {file_size_mb:.1f} MB")
    
    # Also create a parquet version (even more efficient)
    output_parquet = Path("datasets/nfl_data_cloud.parquet")
    df_sampled.to_parquet(output_parquet, compression='gzip', index=False)
    
    parquet_size_mb = output_parquet.stat().st_size / 1024**2
    print(f"Parquet file size: {parquet_size_mb:.1f} MB")
    
    return df_sampled

if __name__ == "__main__":
    create_cloud_dataset()
    print("\n✅ Cloud dataset created successfully!")
    print("\nNext steps:")
    print("1. Commit the .parquet file to git")
    print("2. Update nfl_streamlit_app.py to use the parquet file")
    print("3. Deploy to Streamlit Cloud")
