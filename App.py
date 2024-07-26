import streamlit as st
import pandas as pd
import requests

api_key = "8fce32c29bc344c9b3380c526a43d768"
base_url = "https://api.football-data.org/v4/"

# Configure the page
st.set_page_config(page_title="Football Score Tracker", page_icon="⚽️")

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

# Function to get win streak data for a specific team
import pandas as pd
import random
from datetime import datetime

def get_win_streak_data(team_id, season_year):
    # Simulating API data for now
    matches = [
        {'utcDate': '2023-01-15T12:00:00Z', 'score': {'fullTime': {'home': random.choice([1, None]), 'away': random.choice([1, None])}}},
        {'utcDate': '2023-02-20T15:00:00Z', 'score': {'fullTime': {'home': random.choice([1, None]), 'away': random.choice([1, None])}}},
        # Add more simulated match data as needed
    ]

    if matches:
        dates = [pd.to_datetime(match['utcDate']) for match in matches]
        results = [
            1 if match['score']['fullTime'].get('home', 0) > match['score']['fullTime'].get('away', 0) else
            0 if match['score']['fullTime'].get('home', 0) < match['score']['fullTime'].get('away', 0) else
            0.5
            for match in matches
        ]
        
        win_streaks = []
        current_streak = 0
        
        for result in results:
            if result == 1:
                current_streak += 1
            else:
                current_streak = 0
            win_streaks.append(current_streak)

        # Print lengths for debugging
        print(f"Length of dates: {len(dates)}")
        print(f"Length of win_streaks: {len(win_streaks)}")
        
        if len(dates) != len(win_streaks):
            min_length = min(len(dates), len(win_streaks))
            dates = dates[:min_length]
            win_streaks = win_streaks[:min_length]

        return pd.DataFrame({
            'Date': dates,
            'Streak': win_streaks
        }).set_index('Date')
    
    return pd.DataFrame(columns=['Date', 'Streak']).set_index('Date')

# Sidebar for team selection
team_options = get_teams()
# Set default option to Borussia Dortmund if available
default_team = "Borussia Dortmund"
if default_team in team_options:
    selected_team = st.selectbox("Select a team to view win streak:", list(team_options.keys()), index=list(team_options.keys()).index(default_team))
else:
    selected_team = st.selectbox("Select a team to view win streak:", list(team_options.keys()))

# Date input for selecting year
season_year = st.date_input("Select the season year", min_value=pd.to_datetime('2000-01-01'), max_value=pd.to_datetime('2024-12-31')).year

# Fetch and display win streak data
if selected_team:
    # Fetch team ID based on selected team name
    team_id = team_options.get(selected_team)
    
    if team_id:
        win_streak_data = get_win_streak_data(team_id, season_year)
        
        # Display the DataFrame to check its contents
        st.write("Win Streak Data:")
        st.write(win_streak_data)
        
        if not win_streak_data.empty:
            st.write(f"### Win Streak Data for {selected_team} ({season_year})")
            
            # Plot win streak data
            st.line_chart(win_streak_data['Streak'])
        else:
            st.write(f"No win streak data available for {selected_team} in {season_year}.")
    else:
        st.error("Selected team not found.")

# Email updates
email = st.text_input("Enter your email for regular updates:")
if st.button("Subscribe"):
    if email:
        st.success(f"Subscribed successfully with {email}")
        # Placeholder for email subscription logic
    else:
        st.warning("Please enter a valid email address.")
