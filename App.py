import streamlit as st
import requests
import pandas as pd
import altair as alt

api_key = "8fce32c29bc344c9b3380c526a43d768"
base_url = "https://api.football-data.org/v4/"

# Configure the page
st.set_page_config(page_title="Football Score Tracker", page_icon="🏆")

# Title and header
st.title("Football Score Tracker")
st.header("Top Players and More")

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

# Function to get the most recent competition ID
def get_recent_competition_id():
    url = f"{base_url}competitions/"
    headers = {"X-Auth-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        competitions = response.json().get("competitions", [])
        most_recent = sorted(competitions, key=lambda x: x['currentSeason']['startDate'], reverse=True)[0]
        return most_recent['id']
    else:
        st.error("Failed to fetch competitions from API.")
        return None

# Function to fetch top players from a competition
def get_top_players(competition_id, season_year):
    url = f"{base_url}competitions/{competition_id}/scorers?limit=3&season={season_year}"
    headers = {"X-Auth-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        players = response.json().get("scorers", [])
        return players
    else:
        st.error("Failed to fetch top players from API.")
        return []

# Function to plot top players
def plot_top_players(players):
    df = pd.DataFrame({
        'Player': [player['player']['name'] for player in players],
        'Goals': [player['goals'] for player in players]
    })

    chart = alt.Chart(df).mark_bar().encode(
        x='Player',
        y='Goals',
        color='Player',
        tooltip=['Player', 'Goals']
    ).properties(
        title='Top 3 Players'
    )

    st.altair_chart(chart)

# Sidebar for team selection
team_options = get_teams()
selected_team = st.selectbox("Select a team to view top players:", team_options)

if selected_team:
    # Get recent competition and top players
    competition_id = get_recent_competition_id()
    if competition_id:
        season_year = pd.Timestamp.now().year
        top_players = get_top_players(competition_id, season_year)
        if top_players:
            st.write(f"### Top 3 Players for {selected_team}")
            plot_top_players(top_players)
        else:
            st.write("No top players data available.")
    else:
        st.write("Failed to get recent competition ID.")

# Email updates
email = st.text_input("Enter your email for regular updates:")
if st.button("Subscribe"):
    if email:
        st.success(f"Subscribed successfully with {email}")
        # Placeholder for email subscription logic
    else:
        st.warning("Please enter a valid email address.")
