import streamlit as st
import requests
import pandas as pd

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

# Function to fetch and display real-time scores
def fetch_scores():
    url = f"{base_url}matches/"
    headers = {"X-Auth-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        scores = response.json()  # Replace with actual API response handling
        return scores
    else:
        st.error("Failed to fetch scores from API.")
        return {}

# Function to get win streak data for a specific team
def get_win_streak(team_id):
    url = f"{base_url}matches/?teamId={team_id}&season=2023"  # Adjust for the season
    headers = {"X-Auth-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        matches = response.json().get("matches", [])
        data = pd.DataFrame(matches)
        return data
    else:
        st.error("Failed to fetch win streak data from API.")
        return pd.DataFrame()

# Sidebar for team selection
team_options = get_teams()
selected_teams = st.multiselect("Select teams to track:", team_options)

# Display real-time scores
if selected_teams:
    scores = fetch_scores()
    st.write("### Real-Time Scores")
    for team in selected_teams:
        st.write(f"Scores for {team}: {scores.get(team, 'No data available')}")

# Function to fetch win streak data
def fetch_win_streak_data(team_name):
    url = f"{base_url}matches?team={team_name}&dateFrom={pd.Timestamp.now() - pd.DateOffset(years=1)}&dateTo={pd.Timestamp.now()}"
    headers = {"X-Auth-Token": api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Process data into a DataFrame
    matches = data.get('matches', [])
    win_streaks = pd.DataFrame({
        'Date': [pd.to_datetime(match['utcDate']) for match in matches],
        'Result': [match['score']['fullTime']['home'] > match['score']['fullTime']['away'] for match in matches]
    })
    
    return win_streaks

# Plotting the win streak data using Streamlit's built-in chart
def plot_win_streak(team_name):
    win_streaks = fetch_win_streak_data(team_name)
    
    # Filter for the last year
    one_year_ago = pd.Timestamp.now() - pd.DateOffset(years=1)
    win_streaks = win_streaks[win_streaks['Date'] >= one_year_ago]
    
    # Ensure 'Date' column is in datetime format
    win_streaks['Date'] = pd.to_datetime(win_streaks['Date'])
    
    # Plot the data
    if not win_streaks.empty:
        st.line_chart(
            win_streaks.set_index('Date')['Result'].astype(int)  # Convert boolean to integer (1/0)
        )
    else:
        st.write("No win streak data available for the selected team.")

if selected_teams:
    selected_team_for_streak = st.selectbox("Select a team to view win streak:", selected_teams)
    plot_win_streak(selected_team_for_streak)

# Email updates
email = st.text_input("Enter your email for regular updates:")
if st.button("Subscribe"):
    if email:
        st.success(f"Subscribed successfully with {email}")
        # Placeholder for email subscription logic
    else:
        st.warning("Please enter a valid email address.")
