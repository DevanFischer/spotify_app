import requests
import json
import base64
import sys
from secrets import clientId, clientSecret


def get_access_token(clientId, clientSecret):
    authUrl = "https://accounts.spotify.com/api/token"
    authHead = {}
    authBody = {}

    message = f"{clientId}:{clientSecret}"
    message_bytes = message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")

    authBody["grant_type"] = "client_credentials"
    authHead["Authorization"] = "Basic " + base64_message

    res = requests.post(authUrl, headers=authHead, data=authBody)
    resObj = res.json()

    return resObj["access_token"]


def search(token, params):
    url = "https://api.spotify.com/v1/search"
    req_head = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
    }
    res = requests.get(url, headers=req_head, params=params)
    return res.text


def parse_artist_uri(obj):
    obj = json.loads(obj)
    uri = obj["artists"]["items"][0]["uri"]
    return uri.split(":")[2]


def get_top_tracks(token, uri):
    url = "https://api.spotify.com/v1/artists/" + uri + "/top-tracks?market=ES"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
    }

    res = requests.get(url, headers=headers)
    return res.text


def index_in_list(a_list, index):
    return index < len(a_list)


def create_playlist(user_id):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    body = {"name": "New Playlist"}
    res = requests.post(url, data=body)
    print(res.text)


def main(artist):
    token = get_access_token(clientId, clientSecret)
    artist_obj = search(token, params={"q": artist, "type": "artist"})
    artist_uri = parse_artist_uri(artist_obj)
    top_tracks = get_top_tracks(token, artist_uri)
    create_playlist()


if __name__ == "__main__":
    if index_in_list(sys.argv, 1):
        main(sys.argv[1])
    else:
        print(f"Please give artist name as argument.")
