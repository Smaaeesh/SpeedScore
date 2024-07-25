import streamlit as st
import requests
import pydeck as pdk
import pandas as pd
import plotly.express as px

api_key = "sXEjCjQh3vCYZoGbQgEekBX9bmN1EVJRmVilK25JkdVprFEQ6foUwrbW0zTt"

# Configure the page
st.set_page_config(page_title="Sports Score Tracker", page_icon="🏆")

# Title and header
st.title("Sports Score Tracker")
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

# Sidebar for team selection
team_options = ["Team A", "Team B", "Team C"]  # Replace with your teams
selected_teams = st.multiselect("Select teams to track:", team_options)

# Function to fetch and display real-time scores
def fetch_scores():
    # Placeholder for API call to get scores
    url = f"https://api.sportmonks.com/v3/fixtures?api_token={api_key}"
    response = requests.get(url)
    scores = response.json()  # Replace with actual API response handling
    return scores

# Display real-time scores
if selected_teams:
    scores = fetch_scores()
    st.write("### Real-Time Scores")
    for team in selected_teams:
        st.write(f"Scores for {team}: {scores.get(team, 'No data available')}")

# Graph showing team’s win streak status
def plot_win_streak(team_name):
    # Placeholder for API call to get win streak data
    win_streaks = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=10),
        'Wins': [1, 1, 0, 1, 1, 1, 0, 1, 1, 1]  # Example data
    })
    fig = px.line(win_streaks, 
