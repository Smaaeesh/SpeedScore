import streamlit as st
import pandas as pd
import requests

api_key = "8fce32c29bc344c9b3380c526a43d768"
base_url = "https://api.football-data.org/v4/"

# Configure the page
st.set_page_config(page_title="Football Score Tracker", page_icon="🏆")

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
        return [team["name"] for team in teams]
    else:
        st.error("Failed to fetch teams from API.")
        return []

# Function to get win streak data for a specific team
def get_win_streak_data(team_id):
    url = f"{base_url}teams/{team_id}/matches/"
    headers = {"X-Auth-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        matches = data.get('matches', [])
        if matches:
            # Initialize variables for tracking streak
            streak = 0
            streaks = []
            dates = []

            for match in matches:
                match_date = pd.to_datetime(match['utcDate'])
                home_score = match['score']['fullTime'].get('home', 0)
                away_score = match['score']['fullTime'].get('away', 0)

                # Update streak based on match result
                if home_score > away_score:
                    streak += 1
                else:
                    streak = 0
                
                streaks.append(streak)
                dates.append(match_date)
            
            # Create a DataFrame for plotting
            win_streaks = pd.DataFrame({'Date': dates, 'Streak': streaks})
            return win_streaks
        else:
            return pd.DataFrame(columns=['Date', 'Streak'])
    else:
        st.error("Failed to fetch win streak data from API.")
        return pd.DataFrame(columns=['Date', 'Streak'])

# Sidebar for team selection
team_options = get_teams()
selected_team = st.selectbox("Select a team to view win streak:", team_options)

# Fetch and display win streak data
if selected_team:
    # Fetch team ID based on selected team name
    team_id = [team['id'] for team in get_teams() if team['name'] == selected_team][0]
    
    win_streak_data = get_win_streak_data(team_id)
    
    if not win_streak_data.empty:
        st.write(f"### Win Streak Data for {selected_team}")
        
        # Plot win streak data
        st.line_chart(win_streak_data.set_index('Date')['Streak'])
    else:
        st.write("No win streak data available for the selected team.")

# Email updates
email = st.text_input("Enter your email for regular updates:")
if st.button("Subscribe"):
    if email:
        st.success(f"Subscribed successfully with {email}")
        # Placeholder for email subscription logic
    else:
        st.warning("Please enter a valid email address.")
