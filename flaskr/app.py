from flask import Flask, render_template, request, url_for, session, redirect, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from spotipy.oauth2 import SpotifyOAuth
import spotipy
from dotenv import load_dotenv
from os import environ

import time
import json
import itertools

load_dotenv()  # take environment variables from .env.

# Load environment variables
CLIENT_ID = environ.get("CLIENT_ID")
CLIENT_SECRET = environ.get("CLIENT_SECRET")
COOKIE_NAME = environ.get("COOKIE_NAME")
SECRET_KEY = environ.get("SECRET_KEY")

# Flask-WTF requires an encryption key - the string can be anything
# app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask Configuration
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["SESSION_COOKIE_NAME"] = COOKIE_NAME

TOKEN_INFO = "token_info"

Bootstrap(app)


class ArtistForm(FlaskForm):
    name = StringField("Which actor is your favorite?", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Takes in a list of artists names and creates a playlist of their top ten songs.
@app.route("/makeplaylist")
def make_playlist():
    name = request.args.get("name")
    artists = request.args.get("artists")
    artists_list = artists.split(",")
    print("ARTISTS LIST", artists_list)
    songs = []
    for i in range(len(artists_list)):
        id = get_artist_id(artists_list[i])
        tracks_list = get_top_10(id)
        songs.append(tracks_list)

    flat_list = list(itertools.chain(*songs))

    playlist_id, playlist_url = create_playlist(name=name)
    add_songs_playlist(playlist_id, flat_list)
    return f"<a href={playlist_url}>Playlist Link</a>"


@app.route("/", methods=["GET", "POST"])
def index():

    form = ArtistForm()

    if form.validate_on_submit():

        name = form.name.data
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


# Create a playlist with 'name="name"' and returns the id and url.
def create_playlist(name="New Playlist", description=""):
    sp = connect()
    user_id = sp.me()["id"]
    playlist = sp.user_playlist_create(
        user=user_id,
        name=name,
        public=True,
        collaborative=False,
        description=description,
    )
    playlist_id = playlist["id"]
    playlist_url = playlist["external_urls"]["spotify"]
    return playlist_id, playlist_url


# Get the id of an artist
def get_artist_id(artist):
    # TODO Return no artist found if no artist
    # artist = request.args.get("artist")
    sp = connect()
    response = sp.search(q=artist, limit=10, offset=0, type="artist", market=None)
    return response["artists"]["items"][0]["id"]


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
