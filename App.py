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

# Sidebar setup
st.sidebar.header("Select Mode")
mode = st.sidebar.radio("", ["1 team", "team vs. team"])

# Add image to sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Soccer_ball.svg/1200px-Soccer_ball.svg.png", width=150)

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

# Background color picker
st.subheader("Customize Background and Text Color")

# Color picker
background_color = st.color_picker("Pick a background color", "#ffffff")
text_color = st.color_picker("Pick a text color", "#000000")

# Apply background color and text color to the page
st.markdown(
    f"""
    <style>
    .color-box {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: {background_color} !important;
        z-index: -1;
        pointer-events: none;
    }}
    .text-color {{
        color: {text_color} !important;
    }}
    </style>
    """, unsafe_allow_html=True
)

# Display the color box
st.markdown('<div class="color-box"></div>', unsafe_allow_html=True)

# Apply text color to all main headers and elements
st.markdown(
    f"""
    <style>
    h1, h2, h3, p {{
        color: {text_color} !important;
    }}
    </style>
    """, unsafe_allow_html=True
)

# Main content
if mode == "1 team":
    selected_team = st.selectbox("Select a team:", list(team_options.keys()), index=0)
    season_year = st.date_input("Select a season year:", datetime.now()).year

    team_id = team_options.get(selected_team)

    if team_id:
        display_success_box()
        win_streak_data = get_win_streak_data(team_id, season_year)
        
        # Display the DataFrame to check its contents
        st.write("Win Streak Data:", key="win-streak-data", unsafe_allow_html=True)
        st.dataframe(win_streak_data)
        
        # Plot the data
        st.subheader("Win Streak Over Time", key="win-streak-over-time", unsafe_allow_html=True)
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
        st.write("Win Streak Data for Team 1:", key="team1-win-streak-data", unsafe_allow_html=True)
        st.dataframe(win_streak_data_1)
        
        st.write("Win Streak Data for Team 2:", key="team2-win-streak-data", unsafe_allow_html=True)
        st.dataframe(win_streak_data_2)
        
        # Plot the data side by side
        st.subheader("Win Streak Over Time", key="team-vs-team-win-streak-over-time", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.line_chart(win_streak_data_1, width=350, height=250)
            st.markdown(f"**{selected_team_1} Win Streak**", unsafe_allow_html=True)
        
        with col2:
            st.line_chart(win_streak_data_2, width=350, height=250)
            st.markdown(f"**{selected_team_2} Win Streak**", unsafe_allow_html=True)
        
        # Create an interactive table
        st.subheader("Interactive Results Table", key="interactive-results-table", unsafe_allow_html=True)
        
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

# Additional Streamlit components for user feedback
st.subheader("Leave Your Feedback", key="leave-feedback", unsafe_allow_html=True)

# Slider for rating
rating = st.slider("Rate us (1-10):", min_value=1, max_value=10, step=1)

# Textbox for review
review = st.text_area("Write your review:")

# Display the feedback
if st.button("Submit Feedback"):
    st.write(f"**Rating:** {rating}")
    st.write(f"**Review:** {review}")
