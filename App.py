import streamlit as st
import http.client
import json

# Function to fetch teams from SportMonks API using http.client
def get_teams(api_token):
    try:
        conn = http.client.HTTPSConnection("api.sportmonks.com")
        # Check the correct endpoint for fetching teams
        conn.request("GET", f"/api/v3/football/teams?api_token={api_token}")
        res = conn.getresponse()
        
        if res.status == 200:
            data = res.read().decode("utf-8")
            teams_data = json.loads(data)
            teams = teams_data.get('data', [])
            return [(team['id'], team['name']) for team in teams]
        else:
            st.error(f"Failed to fetch teams. Status code: {res.status}. Message: {res.reason}")
            return []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# Function to fetch scores based on selected team and mode
def get_scores(team_id, mode, api_token):
    try:
        conn = http.client.HTTPSConnection("api.sportmonks.com")
        if mode == "Team vs. Team":
            url = f"/api/v3/football/matches?team_id={team_id}&api_token={api_token}"
        else:  # "1 Team"
            url = f"/api/v3/football/scores?team_id={team_id}&api_token={api_token}"
        
        conn.request("GET", url)
        res = conn.getresponse()
        
        if res.status == 200:
            data = res.read().decode("utf-8")
            scores_data = json.loads(data)
            return scores_data.get('data', [])
        else:
            st.error(f"Failed to fetch scores. Status code: {res.status}. Message: {res.reason}")
            return []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# Streamlit app
st.title("Live Sports Score")

# Dropdown menu to select team
api_token = "sXEjCjQh3vCYZoGbQgEekBX9bmN1EVJRmVilK25JkdVprFEQ6foUwrbW0zTt"  # Updated API token
teams = get_teams(api_token)
if teams:
    team_options = {name: id for id, name in teams}
    team_name = st.selectbox("Select your team", list(team_options.keys()))
else:
    team_name = None

# Buttons to select mode
mode = st.radio("Select mode", ["Team vs. Team", "1 Team"])

if st.button("Show Scores") and team_name:
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
            height: 400px;
            overflow: hidden;
        }
        .lightning {
            position: absolute;
            top: 0;
            left: 50%;
            width: 100px;
            height: 200px;
            background: url('https://upload.wikimedia.org/wikipedia/commons/0/0e/Lightning.svg') no-repeat center center;
            background-size: cover;
            transform: translateX(-50%);
            animation: lightning 1s infinite;
        }
        .helmet {
            position: absolute;
            width: 100px;
            height: 100px;
            background: url('https://upload.wikimedia.org/wikipedia/commons/1/14/Football_helmet_2.svg') no-repeat center center;
            background-size: cover;
            animation: fly 1s forwards;
        }
        .helmet.left {
            left: -100px;
            animation-delay: 0s;
        }
        .helmet.right {
            right: -100px;
            animation-delay: 0s;
        }
        @keyframes lightning {
            0% { opacity: 0; }
            50% { opacity: 1; }
            100% { opacity: 0; }
        }
        @keyframes fly {
            0% { transform: translateX(0); }
            50% { transform: translateX(200px); }
            100% { transform: translateX(100px); }
        }
        </style>
        <div class="animation-container">
            <div class="lightning"></div>
            <div class="helmet left"></div>
            <div class="helmet right"></div>
        </div>
        """
        st.markdown(animation_html, unsafe_allow_html=True)
        
        # Fetch and display scores
        scores = get_scores(team_id, mode, api_token)
        st.write(scores)  # Adjust this to match your data format
