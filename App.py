def get_win_streak_data(team_id):
    url = f"{base_url}teams/{team_id}/matches/"
    headers = {"X-Auth-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        matches = data.get('matches', [])
        if matches:
            # Ensure that the score fields are present and not None
            win_streaks = pd.DataFrame({
                'Date': [pd.to_datetime(match['utcDate']) for match in matches],
                'Result': [
                    1 if (match['score']['fullTime']['home'] is not None and
                          match['score']['fullTime']['away'] is not None and
                          match['score']['fullTime']['home'] > match['score']['fullTime']['away'])
                    else 0 for match in matches
                ]
            })
            return win_streaks
        else:
            return pd.DataFrame(columns=['Date', 'Result'])
    else:
        st.error("Failed to fetch win streak data from API.")
        return pd.DataFrame(columns=['Date', 'Result'])
