import streamlit as st
import http.client
import json

# Function to fetch teams from SportMonks API using http.client
def get_teams(api_token):
    conn = http.client.HTTPSConnection("api.sportmonks.com")
    conn.request("GET", f"/api/v3/football/teams?api_token={api_token}")
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    teams_data = json.loads(data)
    
    if res.status == 200:
        teams = teams_data['data']
        return [(team['id'], team['name']) for team in teams]
    else:
        st.error("Failed to fetch teams")
        return []

# Function to fetch scores based on selected team and mode
def get_scores(team_id, mode, api_token):
    # Placeholder for actual API endpoint and logic
    if mode == "Team vs. Team":
        # Replace with actual endpoint and parameters
        url = f"/api/v3/football/matches?team_id={team_id}&api_token={api_token}"
    else:  # "1 Team"
        # Replace with actual endpoint and parameters
        url = f"/api/v3/football/scores?team_id={team_id}&api_token={api_token}"
    
    conn = http.client.HTTPSConnection("api.sportmonks.com")
    conn.request("GET", url)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    scores_data = json.loads(data)
    
    if res.status == 200:
        return scores_data['data']
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

    # Show animation while loading
    with st.spinner("Loading scores..."):
        # Insert animation HTML
        animation_html = """
        <style>
        .animation-container {
            position: relative;
            width: 100%;
          
