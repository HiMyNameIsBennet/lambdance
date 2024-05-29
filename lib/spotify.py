import json
import requests

import lib.auth as auth


def fetch_current_song():
    payload = {
        "headers": 
        {
            "Authorization": f"Bearer {auth.USER_TOKEN}"
        }
    }

    url = "https://api.spotify.com/v1/me/player/currently-playing"

    song_data = requests.get(url, headers = payload["headers"]).json()

    # construct player string
    # can probably be made more efficient
    print_string = f"Currently playing: {song_data["item"]["name"]} by"
    if len(song_data["item"]["artists"]) != 1:
        for i in range(len(song_data["item"]["artists"]) - 1):
            print_string += f" {song_data["item"]["artists"][i]["name"]},"
        
        print_string += f" and {song_data["item"]["artists"][-1]["name"]}"
    else:
        print_string += f" {song_data["item"]["artists"][0]["name"]}"

    print(print_string + "...")

    return song_data


def fetch_current_song_bpm():
    song_data = fetch_current_song()
    song_id = song_data["item"]["id"]

    # TODO
    # i HAVE to abstract requests. they all look the same
    payload = {
        "headers": 
        {
            "Authorization": f"Bearer {auth.USER_TOKEN}"
        }
    }

    url = f"https://api.spotify.com/v1/audio-features/{song_id}"

    # TODO
    # there are places where request responses aren't directly chained with .json()
    # this might be more concise all over the place
    song_audio_features = requests.get(url, headers = payload["headers"]).json()

    bpm = song_audio_features["tempo"]

    print(f"...running at ~{bpm}BPM")

    return float(bpm)
