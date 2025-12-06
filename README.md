# NFL Decade Analytics Dashboard (2009-2018)

A comprehensive Streamlit dashboard analyzing NFL play-by-play data from 2009 to 2018, featuring interactive racing bar charts, statistical analysis, and geographic visualizations.

## Features

- **Interactive Racing Bars:** Animated visualizations tracking team performance, QB passing yards, RB rushing yards, and WR receiving yards over time
- **Geographic Mapping:** Visual representation of NFL teams across the United States
- **Statistical Analysis:** Deep dive into player and team performance metrics including EPA, touchdowns, yards, and more
- **Game Highlights:** Elite single-game performances with field visualizations
- **Defensive Analysis:** Comprehensive defensive metrics and playmaker statistics

## Deployment Options

### Option 1: Local Deployment (Recommended for Testing)

1. **Download the dataset:**
   - Go to https://www.kaggle.com/datasets/maxhorowitz/nflplaybyplay2009to2016
   - Download "NFL Play by Play 2009-2018 (v5).csv"
   - Place it in the same directory as `nfl_streamlit_app.py`

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run nfl_streamlit_app.py
   ```

### Option 2: Streamlit Cloud Deployment (Public Hosting)

Since the dataset is ~274MB, there are two approaches:

#### A. Using Git LFS (Recommended)

1. **Install Git LFS:**
   ```bash
   git lfs install
   ```

2. **Track the CSV file:**
   ```bash
   git lfs track "*.csv"
   git add .gitattributes
   ```

3. **Add and commit the dataset:**
   ```bash
   git add "NFL Play by Play 2009-2018 (v5).csv"
   git commit -m "Add NFL dataset with Git LFS"
   git push origin master
   ```

4. **Deploy to Streamlit Cloud:**
   - Go to https://share.streamlit.io/
   - Connect your GitHub repository
   - Streamlit will automatically install requirements and load the dataset

#### B. Using External Hosting

1. Upload the CSV to a cloud storage service (Google Drive, Dropbox, AWS S3, etc.)
2. Get a direct download link
3. Modify the `load_data()` function to download from that URL
4. Deploy to Streamlit Cloud

## Requirements

- Python 3.8+
- streamlit >= 1.28.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- plotly >= 5.17.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- geopandas >= 0.14.0
- shapely >= 2.0.0

## Project Structure

```
NFL_Analysis_Dashboard/
├── nfl_streamlit_app.py      # Main Streamlit application
├── requirements.txt           # Python dependencies
├── NFL_Logos/                 # Team logos directory
│   └── *.png                  # Individual team logo files
├── NFL Play by Play 2009-2018 (v5).csv  # Dataset (download separately)
└── README.md                  # This file
```

## Data Source

Dataset: [NFL Play by Play 2009-2016 (includes 2017-2018)](https://www.kaggle.com/datasets/maxhorowitz/nflplaybyplay2009to2016)

## License

This project uses publicly available NFL data from Kaggle for educational purposes.
