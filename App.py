import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time

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

# Sidebar for mode selection using buttons
st.sidebar.header("Select Mode")
mode = st.sidebar.radio("", ["1 team", "team vs. team"])

# Add larger soccer emoji to the sidebar
st.sidebar.markdown(
    """
    <div style="font-size: 1500px; text-align: center;">⚽️</div>
    """, unsafe_allow_html=True
)

)

# Get team options from API or other source
team_options = {
    'Borussia Dortmund': 1,
    'FC Bayern Munich': 2,
    'RB Leipzig': 3
}

def display_success_box():
    success_box = st.empty()
    success_box.success("Team(s) selected successfully!", icon="✅")
    time.sleep(5)
    success_box.empty()

if mode == "1 team":
    selected_team = st.selectbox("Select a team:", list(team_options.keys()), index=0)
    season_year = st.date_input("Select a season year:", datetime.now()).year

    team_id = team_options.get(selected_team)

    if team_id:
        display_success_box()
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
        display_success_box()
        win_streak_data_1 = get_win_streak_data(team_id_1, season_year)
        win_streak_data_2 = get_win_streak_data(team_id_2, season_year)
        
        # Display the DataFrames to check their contents
        st.write("Win Streak Data for Team 1:")
        st.dataframe(win_streak_data_1)
        
        st.write("Win Streak Data for Team 2:")
        st.dataframe(win_streak_data_2)
        
        # Plot the data side by side
        st.subheader("Win Streak Over Time")
        col1, col2 = st.columns(2)
        
        with col1:
            st.line_chart(win_streak_data_1, width=350, height=250)
            st.markdown(f"**{selected_team_1} Win Streak**")
        
        with col2:
            st.line_chart(win_streak_data_2, width=350, height=250)
            st.markdown(f"**{selected_team_2} Win Streak**")
        
        # Create an interactive table
        st.subheader("Interactive Results Table")
        
        # Combine data for the table
        table_data = pd.DataFrame({
            'Date': win_streak_data_1.index,
            selected_team_1: win_streak_data_1['Streak'].values,
            selected_team_2: win_streak_data_2['Streak'].values
        }).set_index('Date')

        # Interactive table
        st.dataframe(table_data.style.set_properties(**{'cursor': 'pointer'}))

        # Add CSS for highlighting
        st.markdown(
            """
            <style>
            .highlighted {
                background-color: yellow;
            }
            </style>
            """, unsafe_allow_html=True
        )

        # JavaScript for interactivity
        st.markdown(
            """
            <script>
            const elements = Array.from(document.getElementsByClassName('dataframe')).flatMap(df => Array.from(df.querySelectorAll('tbody tr td')));
            elements.forEach(el => {
                el.addEventListener('click', () => {
                    elements.forEach(e => e.classList.remove('highlighted'));
                    el.classList.add('highlighted');
                });
            });
            </script>
            """, unsafe_allow_html=True
        )

# Background color and text color control
bg_color = st.color_picker("Pick a background color", "#ffffff")
text_color = st.color_picker("Pick a text color", "#000000")

st.markdown(f"""
    <style>
    .reportview-container {{
        background-color: {bg_color};
    }}
    .css-18e3th9 {{
        color: {text_color};
    }}
    </style>
    """, unsafe_allow_html=True)

# Additional Streamlit components as needed
st.write("You selected background color:", bg_color)
st.write("You selected text color:", text_color)
