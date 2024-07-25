import matplotlib.pyplot as plt

# Graph showing team’s win streak status
def plot_win_streak(team_name):
    # Placeholder for API call to get win streak data
    win_streaks = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=10),
        'Wins': [1, 1, 0, 1, 1, 1, 0, 1, 1, 1]  # Example data
    })
    fig, ax = plt.subplots()
    ax.plot(win_streaks['Date'], win_streaks['Wins'], marker='o')
    ax.set_title(f"Win Streak for {team_name}")
    ax.set_xlabel('Date')
    ax.set_ylabel('Wins')
    st.pyplot(fig)

if selected_teams:
    selected_team_for_streak = st.selectbox("Select a team to view win streak:", selected_teams)
    plot_win_streak(selected_team_for_streak)
