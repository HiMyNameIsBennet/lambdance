import json
import requests
import webbrowser

import lib.util as util
import lib.conn as conn


# should i really use global state like this? maybe refactor this later
CLIENT_TOKEN = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
USER_TOKEN = ""
USER_CODE = ""

def request_spotify_access_token():
    global CLIENT_TOKEN

    read_spotify_client_credentials()
    url = "https://accounts.spotify.com/api/token"

    creds_base64_string = util.encode_client_authentication_token()

    auth = {
        "headers":
        {
            "Authorization": "Basic " + creds_base64_string,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        "form": 
        {
            "grant_type": "client_credentials"
        }
    }

    # maybe refactor this into external function?
    # we have almost the same exact code down in fetch_user_access_token
    res = requests.post(url, data = auth["form"], headers = auth["headers"])
    
    if res.status_code == 200:  # i should also check if there is already a token set that still works
        data = json.loads(res.text)
        CLIENT_TOKEN = data["access_token"]

        return True

    return False


def read_spotify_client_credentials():
    global CLIENT_ID
    global CLIENT_SECRET

    f = open("creds")
    creds = f.read()
    f.close()

    creds = creds.split("\n")

    CLIENT_ID = creds[0]
    CLIENT_SECRET = creds[1]


# REWRITE THIS TO USE PKCE FLOW
# THIS IS INSECURE AND FOR DEV PURPOSES ONLY
# https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow
def request_user_authorization():
    global USER_CODE

    state = util.generate_random_string(16)
    payload = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "http://localhost:8888",
        "state": state
    }

    root_url = "https://accounts.spotify.com/authorize?"

    params = ""
    prefix = ""
    for (key, val) in payload.items():
        params = params + f"{prefix}{key}={val}"
        # do not add a prefix on first parameter but on all consecutive
        prefix = "&"

    webbrowser.open(root_url + params)

    user_code, return_state = conn.launch_callback_server()

    if return_state != state:
        return False
    
    USER_CODE = user_code

    return True


def fetch_user_access_token():
    global USER_TOKEN

    creds_base64_string = util.encode_client_authentication_token()

    url = "https://accounts.spotify.com/api/token"
    auth = {
        "headers":
        {
            "Authorization": "Basic " + creds_base64_string,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        "form":
        {
            "grant_type": "authorization_code",
            "code": USER_CODE,
            "redirect_uri": "http://localhost:8888"
        }
    }

    res = requests.post(url, data = auth["form"], headers = auth["headers"])
    
    # i should check if there is already a token set that still works
    # t.t.e, check out refresh_token
    # https://developer.spotify.com/documentation/web-api/tutorials/refreshing-tokens
    if res.status_code == 200: 
        data = json.loads(res.text)
        USER_TOKEN = data["access_token"]

        return True

    return False
