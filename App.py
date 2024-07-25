import streamlit as st
import requests

# Set up the API endpoints
BASE_URL = "https://soccer.sportmonks.com/api/v3.0"
API_KEY = "sXEjCjQh3vCYZoGbQgEekBX9bmN1EVJRmVilK25JkdVprFEQ6foUwrbW0zTt"

# Function to get the list of countries from the API
def get_countries():
    response = requests.get(f"{BASE_URL}/countries?api_token={API_KEY}")
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        st.error("Failed to fetch countries")
        return []

# Function to get the list of regions for a given country from the API
def get_regions(country_id):
    response = requests.get(f"{BASE_URL}/countries/{country_id}?api_token={API_KEY}")
    if response.status_code == 200:
        return response.json().get('data', {}).get('regions', [])
    else:
        st.error("Failed to fetch regions")
        return []

# Get the list of countries
countries = get_countries()

# Streamlit app layout
st.title("Country and Region Selector")

# Create a select box for countries
country_names = [country['name'] for country in countries]
selected_country = st.selectbox("Select a country", country_names)

# Find the selected country's ID
selected_country_id = next((country['id'] for country in countries if country['name'] == selected_country), None)

# Display regions if a country is selected
if selected_country_id:
    regions = get_regions(selected_country_id)
    if regions:
        region_names = [region['name'] for region in regions]
        selected_region = st.selectbox("Select a region", region_names)
        st.write(f"You selected: {selected_country} - {selected_region}")
    else:
        st.write("No regions available for the selected country.")
else:
    st.write("Please select a country.")
