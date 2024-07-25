import streamlit as st
import requests

# Replace 'YOUR_TOKEN' with your actual API token
API_TOKEN = 'YOUR_TOKEN'

# Function to get the list of teams
def get_teams():
    url = f"https://api.sportmonks.com/api/v3/football/teams?api_token={API_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        teams = response.json()['data']
        return {team['name']: team['id'] for team in teams}
    else:
        st.error('Unable to fetch teams')
        return {}

# Function to get live scores
def get_live_scores(team_id):
    api_url = f"https://api.sportmonks.com/api/v3/football/livescores?api_token={API_TOKEN}&team_id={team_id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Streamlit app
st.title('Live Sports Scores')

# Fetch and display teams in dropdown menu
teams = get_teams()
if teams:
    selected_team = st.selectbox('Select your team', list(teams.keys()))

    # Mode selection buttons
    mode = st.radio('Select mode', ['Team vs. Team', '1 Team'])

    if st.button('Get Scores'):
        team_id = teams[selected_team]
        scores = get_live_scores(team_id)
        
        if scores:
            if mode == 'Team vs. Team':
                st.subheader(f"Scores for {selected_team} vs. Opponent")
                st.json(scores)  # Display the raw JSON response for now
            else:
                st.subheader(f"Scores for {selected_team}")
                st.json(scores)  # Display the raw JSON response for now
        else:
            st.error('Unable to fetch scores')
else:
    st.warning('No teams available. Please check the API token and try again.')
