import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

api_key = "8fce32c29bc344c9b3380c526a43d768"
base_url = "https://api.football-data.org/v4/"

# Configure the page
st.set_page_config(page_title="Football Score Tracker", page_icon="O")

# Title and header
st.title("Football Score Tracker")
st.header("Live Scores, Win Streaks, and More")

# Color picker for background
bg_color = st.color_picker("Choose Background Color", "#f0f0f0")
st.markdown(f"""
    <style>
    .reportview-container {{
        background-color: {bg_color};
    }}
    </style>
""", unsafe_allow_html=True)

# Function to fetch teams from Football Data API
def get_teams():
    url = f"{base_url}teams/"
    headers = {"X-Auth-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        teams = response.json().get("teams", [])
        return {team["name"]: team["id"] for team in teams}
    else:
        st.error("Failed to fetch teams from API.")
        return {}

# Function to simulate win streak data for a specific team
def simulate_win_streak_data(season_year):
    # Generate a date range for each month in the selected year
    start_date = datetime(season_year, 1, 1)
    end_date = datetime(season_year, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='M')

    # Generate random win/loss/tie data
    streaks = []
    current_streak = 0

    for _ in date_range:
        result = random.choice(['win', 'loss', 'tie'])
        
        if result == 'win':
            current_streak += 1
        else:
            streaks.append(current_streak)
            current_streak = 0
    
    streaks.append(current_streak)  # Append final streak
    
    # Create a DataFrame with simulated data
    return pd.DataFrame({
        'Date': date_range,
        'Streak': streaks
    }).set_index('Date')

# Sidebar for team selection
team_options = get_teams()
selected_team = st.selectbox("Select a team to view win streak:", list(team_options.keys()))

# Date input for selecting year
season_year = st.date_input("Select the season year", min_value=pd.to_datetime('2000-01-01'), max_value=pd.to_datetime('2024-12-31')).year

# Fetch and display win streak data
if selected_team:
    # Simulate win streak data
    win_streak_data = simulate_win_streak_data(season_year)
    
    if not win_streak_data.empty:
        st.write(f"### Win Streak Data for {selected_team} ({season_year})")
        
        # Plot win streak data
        st.line_chart(win_streak_data['Streak'])
    else:
        st.write(f"No win streak data available for {selected_team} in {season_year}.")

# Email updates
email = st.text_input("Enter your email for regular updates:")
if st.button("Subscribe"):
    if email:
        st.success(f"Subscribed successfully with {email}")
        # Placeholder for email subscription logic
    else:
        st.warning("Please enter a valid email address.")
