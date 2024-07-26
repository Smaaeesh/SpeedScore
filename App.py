import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Function to simulate win streak data
def get_win_streak_data(team_id, season_year):
    # Simulating API data for now
    matches = [
        {'utcDate': '2023-01-15T12:00:00Z', 'score': {'fullTime': {'home': random.choice([1, None]), 'away': random.choice([1, None])}}},
        {'utcDate': '2023-02-20T15:00:00Z', 'score': {'fullTime': {'home': random.choice([1, None]), 'away': random.choice([1, None])}}},
        # Add more simulated match data as needed
    ]

    if matches:
        dates = [pd.to_datetime(match['utcDate']) for match in matches]
        results = []

        for match in matches:
            home_score = match['score']['fullTime'].get('home', 0)
            away_score = match['score']['fullTime'].get('away', 0)
            
            # Ensure we handle NoneType
            if home_score is None:
                home_score = 0
            if away_score is None:
                away_score = 0
            
            if home_score > away_score:
                results.append(1)
            elif home_score < away_score:
                results.append(0)
            else:
                results.append(0.5)
        
        win_streaks = []
        current_streak = 0
        
        for result in results:
            if result == 1:
                current_streak += 1
            else:
                current_streak = 0
            win_streaks.append(current_streak)

        # Print lengths for debugging
        print(f"Length of dates: {len(dates)}")
        print(f"Length of win_streaks: {len(win_streaks)}")
        
        if len(dates) != len(win_streaks):
            min_length = min(len(dates), len(win_streaks))
            dates = dates[:min_length]
            win_streaks = win_streaks[:min_length]

        return pd.DataFrame({
            'Date': dates,
            'Streak': win_streaks
        }).set_index('Date')
    
    return pd.DataFrame(columns=['Date', 'Streak']).set_index('Date')

# Streamlit app setup
st.set_page_config(page_title="Football Win Streaks", page_icon="⚽️")

st.title("Football Win Streaks")

# Sidebar for mode selection
mode = st.sidebar.selectbox("Select Mode", ["1 team", "team vs. team"])

# Get team options from API or other source
team_options = {
    'Borussia Dortmund': 1,
    'FC Bayern Munich': 2,
    'RB Leipzig': 3
}

if mode == "1 team":
    selected_team = st.selectbox("Select a team:", list(team_options.keys()), index=0)
    season_year = st.date_input("Select a season year:", datetime.now()).year

    team_id = team_options.get(selected_team)

    if team_id:
        win_streak_data = get_win_streak_data(team_id, season_year)
        
        # Display the DataFrame to check its contents
        st.write("Win Streak Data:")
        st.dataframe(win_streak_data)
        
        # Plot the data
        st.subheader("Win Streak Over Time")
        st.line_chart(win_streak_data)
else:
    selected_team_1 = st.selectbox("Select the first team:", list(team_options.keys()), index=0)
    selected_team_2 = st.selectbox("Select the second team:", list(team_options.keys()), index=1)
    season_year = st.date_input("Select a season year:", datetime.now()).year

    team_id_1 = team_options.get(selected_team_1)
    team_id_2 = team_options.get(selected_team_2)

    if team_id_1 and team_id_2:
        win_streak_data_1 = get_win_streak_data(team_id_1, season_year)
        win_streak_data_2 = get_win_streak_data(team_id_2, season_year)
        
        # Display the DataFrames to check their contents
        st.write("Win Streak Data for Team 1:")
        st.dataframe(win_streak_data_1)
        
        st.write("Win Streak Data for Team 2:")
        st.dataframe(win_streak_data_2)
        
        # Plot the data
        st.subheader("Win Streak Over Time")
        st.line_chart(win_streak_data_1)
        st.line_chart(win_streak_data_2)

# Additional Streamlit components as needed
background_color = st.color_picker("Pick a background color", "#ffffff")
st.write("You selected:", background_color)
