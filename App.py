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
def get_win_streak_data(team_name):
    # Placeholder for API call to get win streak data
    url = f"{base_url}matches?team={team_name}&dateFrom={pd.Timestamp.now() - pd.DateOffset(years=1)}&dateTo={pd.Timestamp.now()}"
    headers = {"X-Auth-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        matches = data.get('matches', [])
        if matches:
            win_streaks = pd.DataFrame({
                'Date': [pd.to_datetime(match['utcDate']) for match in matches],
                'Result': [1 if match['score']['fullTime']['home'] > match['score']['fullTime']['away'] else 0 for match in matches]
            })
            return win_streaks
        else:
            return pd.DataFrame(columns=['Date', 'Result'])
    else:
        st.error("Failed to fetch win streak data from API.")
        return pd.DataFrame(columns=['Date', 'Result'])

# Sidebar for team selection
team_options = get_teams()
selected_team = st.selectbox("Select a team to view win streak:", team_options)

# Fetch and display win streak data
if selected_team:
    win_streak_data = get_win_streak_data(selected_team)
    
    if not win_streak_data.empty:
        st.write(f"### Win Streak Data for {selected_team}")
        
        # Create a comparison feature
        if st.button("Compare with another team"):
            # Show a second selectbox for team comparison
            comparison_team = st.selectbox("Select a team to compare:", team_options)
            
            if comparison_team and comparison_team != selected_team:
                comparison_data = get_win_streak_data(comparison_team)
                
                if not comparison_data.empty:
                    st.write(f"### Comparison of Win Streaks: {selected_team} vs {comparison_team}")
                    
                    # Plot comparison
                    st.line_chart({
                        f'{selected_team} Win Streak': win_streak_data.groupby('Date').sum()['Result'],
                        f'{comparison_team} Win Streak': comparison_data.groupby('Date').sum()['Result']
                    })
                else:
                    st.write(f"No win streak data available for {comparison_team}.")
            else:
                st.write("Please select a different team to compare.")
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
