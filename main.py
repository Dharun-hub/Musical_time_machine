import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from pprint import pprint   # Helps to print nested objects prettier.

CLIENT_ID = "22dda6c8d3b34cfa8e9080b8cf8385e1"
CLIENT_SECRET = "4799e284888b4dfc9c8627c30dd52ae8"
REDIRECT_URI = "http://example.com"
SPOTIFY_USERNAME = "31z3chm4bpm4xec636zcrjzzye6i"
SPOTIFY_ENDPOINT = f"https://api.spotify.com/v1/users/{SPOTIFY_USERNAME}/playlists"

year = input("Enter the year you wanna travel to? Enter the year in yyyy-mm-dd : ")

# Gathering the data from the billboard website
response = requests.get(f"https://www.billboard.com/charts/hot-100/{year}/")
billboard_data = response.text

soup = BeautifulSoup(billboard_data, "html.parser")
song_list = soup.select("li ul li h3")
top_songs = [song.getText().strip() for song in song_list]
print(top_songs)

# Authenticating Spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
         scope = "playlist-modify-private",
         redirect_uri = REDIRECT_URI,
         client_id = CLIENT_ID,
         client_secret = CLIENT_SECRET,
         show_dialog = True,
         cache_path = "token.txt",
         username = SPOTIFY_USERNAME,
    )
)
user_id = sp.current_user()["id"]

# Getting songs URI
songs_uri = []
year_param = year.split("-")[0]
for song in top_songs:
    result = sp.search(q=f"track:{song} year:{year_param}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print(f"{song} not found on spotify, Skipped..")

# Creating playlists and adding songs to the playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{year} Top 100s", public=False)
# print(playlist["id"])
sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uri)