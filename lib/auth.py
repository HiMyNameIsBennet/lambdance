import json
import base64
import requests
import webbrowser

import lib.util as util
import lib.conn as conn


TOKEN = ""
CLIENT_ID = ""
USER_TOKEN = ""

def request_spotify_access_token():
    global TOKEN
    global CLIENT_ID

    creds = read_spotify_client_credentials()
    CLIENT_ID = creds[0]
    url = "https://accounts.spotify.com/api/token"

    creds_formatted = f"{creds[0]}:{creds[1]}"
    creds_ascii = creds_formatted.encode("ascii")

    creds_base64_bytes = base64.b64encode(creds_ascii)
    creds_base64_string = creds_base64_bytes.decode("ascii")

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

    res = requests.post(url, data = auth["form"], headers = auth["headers"])
    
    if res.status_code == 200:  # i should also check if there is already a token set that still works
        data = json.loads(res.text)
        TOKEN = data["access_token"]

        return True

    return False


def read_spotify_client_credentials():
    f = open("creds")
    creds = f.read()
    f.close()

    return creds.split("\n")


# REWRITE THIS TO USE PKCE FLOW
# THIS IS INSECURE AND FOR DEV PURPOSES ONLY
# https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow
def request_user_authorization():
    global USER_TOKEN

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
    
    USER_TOKEN = user_code

    return True
