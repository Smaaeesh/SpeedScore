import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import time
import requests

def get_teams_from_api():
    api_key = "8fce32c29bc344c9b3380c526a43d768"
    headers = {"X-Auth-Token": api_key}
    response = requests.get("https://api.football-data.org/v4/teams", headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    data = response.json()
    teams = {team['name']: team['id'] for team in data['teams']}
    return teams

def get_win_streak_data(team_id, season_year):
    start_date = datetime(year=season_year, month=1, day=1)
    end_date = datetime(year=season_year, month=12, day=31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    results = []
    for _ in dates:
        results.append(random.choice([1, 0, 0.5]))
    
    win_streaks = []
    current_streak = 0
    for result in results:
        if result == 1:
            current_streak += 1
        else:
            current_streak = 0
        win_streaks.append(current_streak)
    
    if len(dates) != len(win_streaks):
        min_length = min(len(dates), len(win_streaks))
        dates = dates[:min_length]
        win_streaks = win_streaks[:min_length]
    
    return pd.DataFrame({
        'Date': dates,
        'Streak': win_streaks
    }).set_index('Date')

st.set_page_config(page_title="Football Win Streaks", page_icon="⚽️")

st.title("Football Win Streaks")

team_options = get_teams_from_api()

st.sidebar.header("Select Mode")
mode = st.sidebar.radio("Mode:", ["1 team", "team vs. team"], label_visibility="collapsed")

def display_success_box():
    success_box = st.empty()
    success_box.success("Team(s) selected successfully!", icon="✅")
    time.sleep(5)
    success_box.empty()

if mode == "1 team":
    selected_team = st.selectbox("Select a team:", list(team_options.keys()), index=0, label_visibility="collapsed")
    season_year = st.date_input("Select a season year:", datetime.now()).year

    team_id = team_options.get(selected_team)

    if team_id:
        display_success_box()
        win_streak_data = get_win_streak_data(team_id, season_year)
        
        st.write("Win Streak Data:")
        st.dataframe(win_streak_data)
        
        st.subheader("Win Streak Over Time")
        st.line_chart(win_streak_data)
else:
    selected_team_1 = st.selectbox("Select the first team:", list(team_options.keys()), index=0, label_visibility="collapsed")
    selected_team_2 = st.selectbox("Select the second team:", list(team_options.keys()), index=1, label_visibility="collapsed")
    season_year = st.date_input("Select a season year:", datetime.now()).year

    team_id_1 = team_options.get(selected_team_1)
    team_id_2 = team_options.get(selected_team_2)

    if team_id_1 and team_id_2:
        display_success_box()
        win_streak_data_1 = get_win_streak_data(team_id_1, season_year)
        win_streak_data_2 = get_win_streak_data(team_id_2, season_year)
        
        st.write("Win Streak Data for Team 1:")
        st.dataframe(win_streak_data_1)
        
        st.write("Win Streak Data for Team 2:")
        st.dataframe(win_streak_data_2)
        
        st.subheader("Win Streak Over Time")
        col1, col2 = st.columns(2)
        
        with col1:
            st.line_chart(win_streak_data_1, width=350, height=250)
            st.markdown(f"**{selected_team_1} Win Streak**")
        
        with col2:
            st.line_chart(win_streak_data_2, width=350, height=250)
            st.markdown(f"**{selected_team_2} Win Streak**")
        
        st.subheader("Interactive Results Table")
        
        table_data = pd.DataFrame({
            'Date': win_streak_data_1.index,
            selected_team_1: win_streak_data_1['Streak'].values,
            selected_team_2: win_streak_data_2['Streak'].values
        }).set_index('Date')

        st.dataframe(table_data.style.set_properties(**{'cursor': 'pointer'}))

        st.markdown(
            """
            <style>
            .highlighted {
                background-color: yellow;
            }
            </style>
            """, unsafe_allow_html=True
        )

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

st.subheader("Leave a Review")

rating = st.slider(
    "Rating (1 to 10):",
    min_value=1,
    max_value=10,
    value=5
)

review = st.text_area(
    "Your Review:",
    placeholder="Write your review here...",
    height=200
)

if st.button("Submit Review"):
    st.success("Thank you for your review!")

st.subheader("Receive Future Updates")

email = st.text_input(
    "Enter your email:",
    placeholder="example@domain.com"
)

if st.button("Submit Email"):
    if email:
        st.success("Thank you! You will receive future updates.")
    else:
        st.warning("Please enter a valid email address.")
