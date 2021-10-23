from flask import Flask, render_template, request, url_for, session, redirect, jsonify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from os import environ
import spotipy
import time
import json

load_dotenv()  # take environment variables from .env.

# Flask Configuration
CLIENT_ID = environ.get("CLIENT_ID")
CLIENT_SECRET = environ.get("CLIENT_SECRET")
COOKIE_NAME = environ.get("COOKIE_NAME")
SECRET_KEY = environ.get("SECRET_KEY")

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["SESSION_COOKIE_NAME"] = COOKIE_NAME

TOKEN_INFO = "token_info"


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for("redirectPage", _external=True),
        scope=[
            "user-library-read",
            "playlist-modify-private",
            "playlist-modify-public",
        ],
    )


@app.route("/login")
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route("/redirect")
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for("index", _external=True))


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception
    now = int(time.time())
    is_expired = token_info["expires_at"] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info


def connect():
    try:
        token_info = get_token()
        return spotipy.Spotify(auth=token_info["access_token"])
    except:
        print("User not logged in.")
        return redirect("/login")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.json
        return jsonify(data)
    else:
        return render_template("createPlaylist.html")


@app.route("/created", methods=["GET", "POST"])
def created():
    data = request.json
    print(data)
    # return jsonify(data)
    return redirect(url_for("success"))


@app.route("/success", methods=["GET", "POST"])
def success():
    print("success")
    # data = request.json
    # print(data)
    # return jsonify(data)
    return render_template("success.html")


# Gets the users saved songs
@app.route("/getTracks")
def getTracks():
    sp = connect()
    all_songs = []
    iter = 0
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=iter * 50)["items"]
        iter += 1
        all_songs += items
        if len(items) < 50:
            break
    return jsonify(all_songs)


# Create a playlist with `name="name"` and return the id and url.
# @app.route("/create")
def create_playlist(name="New Playlist"):
    sp = connect()
    user_id = sp.me()["id"]
    playlist = sp.user_playlist_create(
        user=user_id,
        name=name,
        public=True,
        collaborative=False,
        description="Testing App",
    )
    playlist_id = playlist["id"]
    playlist_url = playlist["external_urls"]["spotify"]
    return playlist_id, playlist_url


# Get the id of an artist
# @app.route("/getTopSongs", methods=["GET", "POST"])
def get_artist_id(artist):
    # artist = request.args.get("artist")
    sp = connect()
    response = sp.search(q=artist, limit=10, offset=0, type="artist", market=None)
    return response["artists"]["items"][0]["id"]


def main(artist_id, artist):
    top_tracks = get_top_10(artist_id)
    playlist_id, playlist_url = create_playlist(name=artist)
    add_songs_playlist(playlist_id, top_tracks)
    return playlist_url


# Takes in a list of artists names and creates a playlist of their top ten songs.
def make_playlist(artists):
    songs = []
    for i in artists:
        top_tracks = get_top_10(artists[i])
        songs.append(top_tracks)

    playlist_id, playlist_url = create_playlist(name="WICKED 2021")
    add_songs_playlist(playlist_id, songs)
    return playlist_url


# Takes in an artists id and returns the uri's for their top ten songs.
def get_top_10(id):
    sp = connect()
    top_tracks = sp.artist_top_tracks(artist_id=id, country="US")
    uris = []
    for track in top_tracks["tracks"]:
        track_uri = track["uri"]
        uris.append(track_uri)
    return uris


# Takes in a playlist id and a list of songs and adds the songs to the playlist.
def add_songs_playlist(pl_id, songs):
    sp = connect()
    return sp.playlist_add_items(playlist_id=pl_id, items=songs, position=None)


if __name__ == "__main__":
    app.run(debug=True)
