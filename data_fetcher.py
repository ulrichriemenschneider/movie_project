import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")
REQUEST_URL = "http://www.omdbapi.com/?t="
KEYS = ["Title", "Year", "imdbRating", "Poster", "Error"]


def fetch_data(movie_title):
    """
    Fetches the movie data for the movie 'movie_title'.
    """
    url = f"{REQUEST_URL}{movie_title}&apikey={API_KEY}"
    try:
        res = requests.get(url)
        if res.status_code == requests.codes.ok:
            return res.json()
        else:
            return {"Error": f"Error: {res.status_code}"}
    except requests.exceptions.RequestException:
        return {"Error": "Connection failed (Network Error)"}

def get_needed_data_from_dict(data_dict):
    needed_values = {}
    for key in KEYS:
        try:
            needed_values[key] = data_dict[key]
        except KeyError:
            needed_values[key] = None
    return needed_values
