from operator import itemgetter
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import os
from dotenv import load_dotenv
load_dotenv()

# Authentication - without user
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id= CLIENT_ID,
                                                      client_secret= CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# test playlist
playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_items(playlist_URI)["items"]]

# mapping for song key
key_dict = {
    -1: "No Key Detected",
    0: "C",
    1: "C#/Db",
    2: "D",
    3: "D#/Eb",
    4: "E",
    5: "F",
    6: "F#/Gb",
    7: "G",
    8: "G#/Ab",
    9: "A",
    10: "A#/Bb",
    11: "B"
}

playlist = sp.playlist(playlist_id="37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f", fields="name")
# print("Songs taken from playlist: " + playlist["name"])

# for track in sp.playlist_items(playlist_URI)["items"]:
#     # URI
#     track_uri = track["track"]["uri"]
#     # Track name
#     track_name = track["track"]["name"]
#     # Main Artist
#     artist_uri = track["track"]["artists"][0]["uri"]
#     artist_info = sp.artist(artist_uri)
#     # Name, popularity, genre
#     artist_name = track["track"]["artists"][0]["name"]
#     artist_pop = artist_info["popularity"]
#     artist_genres = artist_info["genres"]
#     # Album
#     album = track["track"]["album"]["name"]
#     # Popularity of the track
#     track_pop = track["track"]["popularity"]

    # The key of the track
    # track_key_raw = sp.audio_features(track_uri)[0]['key']
    # track_key_conversion = key_dict[track_key_raw]
    

def get_song_key(input_uri):
    artist_name = sp.track(input_uri)["artists"][0]["name"]
    track_name = sp.track(input_uri)["name"]
    actual_uri = sp.track(input_uri)["uri"]
    track_key_raw = sp.audio_features(actual_uri)[0]['key']
    track_key_conversion = key_dict[track_key_raw]
    list = [artist_name, track_name, track_key_conversion]
    return list


def get_playlist_uri(playlist_link):
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    return playlist_URI

    
def get_playlist_name(playlist_link):
    uri = get_playlist_uri(playlist_link)
    playlist = sp.playlist(playlist_id=uri, fields="name")
    return playlist["name"]


def get_playlist_keys(playlist_link):
    all_songs = []
    for track in sp.playlist_items(get_playlist_uri(playlist_link))["items"]:
        track_uri = track["track"]["uri"]
        song_details = get_song_key(track_uri)
        artist = song_details[0]
        tr = song_details[1]
        key = song_details[2]
        details_list = [artist, tr, key]
        all_songs.append(details_list)
    return sorted(all_songs, key=itemgetter(2))


