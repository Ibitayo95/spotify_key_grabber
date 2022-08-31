
from flask import Flask, render_template, request
import music

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
def home():
    input_url = request.form["trURL"]

    song_details = music.get_song_key(input_url)
    artist = song_details[0]
    track = song_details[1]
    key = song_details[2]
    image = music.get_album_art(input_url)
    return render_template('key.html', artst=artist, tr=track, k=key, artwork=image)


@app.route("/playlist")
def index2():
    return render_template("playlist.html")


@app.route("/playlist", methods=["GET", "POST"])
def playlist_home():
    input_url = request.form["plURL"]
    playlist_name = music.get_playlist_name(input_url)
    playlist_data = music.get_playlist_keys(input_url)
    return render_template("playlistKey.html", name=playlist_name, playlist=playlist_data)
