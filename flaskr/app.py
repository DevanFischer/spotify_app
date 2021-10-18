from flask import Flask, render_template, request, url_for, session, redirect
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from os import environ
import spotipy
import time


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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/getTracks")
def getTracks():
    sp = auth.connect()

    all_songs = []
    iter = 0
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=iter * 50)[
            "items"
        ]
        iter += 1
        all_songs += items
        if len(items) < 50:
            break
    return str(len(all_songs))


def create_playlist(name="New Playlist"):
    try:
        token_info = auth.get_token()
    except:
        print("User not logged in.")
        return redirect("/")
    sp = spotipy.Spotify(auth=token_info["access_token"])
    user_id = sp.me()["id"]
    return sp.user_playlist_create(
        user=user_id,
        name=name,
        public=True,
        collaborative=False,
        description="Testing App",
    )


# Get the id of an artist
@app.route("/getId")
def get_artist_id():
    artist = request.args.get("artist")
    sp = auth.connect()
    response = sp.search(
        q=artist, limit=10, offset=0, type="artist", market=None
    )
    id = response["artists"]["items"][0]["id"]
    top_tracks = get_top_100(id)

    return top_tracks


# Get top 100 songs of artist
def get_top_100(id):
    sp = auth.connect()
    top_tracks = sp.artist_top_tracks(artist_id=id, limit=50, country="US")
    return top_tracks


# Add songs to playlist
# playlist_add_items(playlist_id, items, position=None)


# AUTH FLOW
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
    return redirect(url_for("getTracks", _external=True))


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
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
