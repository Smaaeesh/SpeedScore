import streamlit as st
import requests

# Function to fetch teams from SportMonks API
def get_teams(api_token):
    url = f"https://api.sportmonks.com/api/v3/football/teams?api_token={api_token}"
    response = requests.get(url)
    if response.status_code == 200:
        teams = response.json()['data']
        return [(team['id'], team['name']) for team in teams]
    else:
        st.error("Failed to fetch teams")
        return []

# Function to fetch scores based on selected team and mode
def get_scores(team_id, mode, api_token):
    # Placeholder for actual API endpoint and logic
    if mode == "Team vs. Team":
        # Replace with actual endpoint and parameters
        url = f"https://api.sportmonks.com/api/v3/football/matches?team_id={team_id}&api_token={api_token}"
    else:  # "1 Team"
        # Replace with actual endpoint and parameters
        url = f"https://api.sportmonks.com/api/v3/football/scores?team_id={team_id}&api_token={api_token}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        st.error("Failed to fetch scores")
        return []

# Streamlit app
st.title("Live Sports Score")

# Dropdown menu to select team
api_token = "YOUR_API_TOKEN"  # Replace with your actual API token
teams = get_teams(api_token)
team_options = {name: id for id, name in teams}
team_name = st.selectbox("Select your team", list(team_options.keys()))

# Buttons to select mode
mode = st.radio("Select mode", ["Team vs. Team", "1 Team"])

if st.button("Show Scores"):
    team_id = team_options[team_name]
    st.write(f"Selected Team ID: {team_id}")
    st.write(f"Selected Mode: {mode}")

    # Fetch and display scores
    scores = get_scores(team_id, mode, api_token)
    st.write(scores)  # Adjust this to match your data format
