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
def get_win_streak_data(team_id, season_year):
    url = f"{base_url}teams/{team_id}/matches?season={season_year}"
    headers = {"X-Auth-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        matches = data.get('matches', [])
        
        if matches:
            win_streaks = []
            current_streak = 0
            for match in matches:
                home_score = match['score']['fullTime'].get('home', 0)
                away_score = match['score']['fullTime'].get('away', 0)
                result = 1 if home_score > away_score else 0
                
                if result == 1:
                    current_streak += 1
                else:
                    win_streaks.append(current_streak)
                    current_streak = 0
            win_streaks.append(current_streak)  # Append final streak
            return pd.DataFrame({
                'Date': [pd.to_datetime(match['utcDate']) for match in matches],
                'Streak': win_streaks
            }).set_index('Date')
        else:
            return pd.DataFrame(columns=['Date', 'Streak'])
    else:
        st.error("Failed to fetch win streak data from API.")
        return pd.DataFrame(columns=['Date', 'Streak'])

# Sidebar for team selection
team_options = get_teams()
selected_team = st.selectbox("Select a team to view win streak:", list(team_options.keys()))

# Date input for selecting year
season_year = st.date_input("Select the season year", min_value=pd.to_datetime('2000-01-01'), max_value=pd.to_datetime('2024-12-31')).year

# Fetch and display win streak data
if selected_team:
    # Fetch team ID based on selected team name
    team_id = team_options.get(selected_team)
    
    if team_id:
        win_streak_data = get_win_streak_data(team_id, season_year)
        
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
