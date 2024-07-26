import streamlit as st

# Streamlit app setup
st.set_page_config(page_title="Football Win Streaks", page_icon="⚽️")

st.title("Football Win Streaks")

# Sidebar for mode selection using buttons
st.sidebar.header("Select Mode")
mode = st.sidebar.radio("", ["1 team", "team vs. team"])

# Add a large text of soccer emojis in a pile effect
st.sidebar.markdown(
    """
    <style>
    .soccer-ball {
        font-size: 100px; /* Adjust size as needed */
        display: inline-block;
        position: absolute;
        z-index: 1;
    }
    .soccer-ball:nth-of-type(1) {
        top: 0px;
        left: 0px;
        z-index: 3;
    }
    .soccer-ball:nth-of-type(2) {
        top: 20px;
        left: 20px;
        z-index: 2;
    }
    .soccer-ball:nth-of-type(3) {
        top: 40px;
        left: 40px;
        z-index: 1;
    }
    .soccer-ball:nth-of-type(4) {
        top: 60px;
        left: 60px;
        z-index: 0;
    }
    </style>
    """, unsafe_allow_html=True
)

# Insert multiple soccer ball emojis with different positioning
st.sidebar.markdown(
    """
    <div style="position: relative;">
        <div class="soccer-ball">⚽️</div>
        <div class="soccer-ball">⚽️</div>
        <div class="soccer-ball">⚽️</div>
        <div class="soccer-ball">⚽️</div>
    </div>
    """, unsafe_allow_html=True
)

# Rest of the Streamlit code
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

# Additional Streamlit components as needed
background_color = st.color_picker("Pick a background color", "#ffffff")
st.write("You selected:", background_color)

# Change the background color of the entire app and text
st.markdown(
    f"""
    <style>
    .css-1d391kg {{
        background-color: {background_color};
    }}
    .css-1v0mbdj {{
        color: {background_color};
    }}
    </style>
    """, unsafe_allow_html=True
)
