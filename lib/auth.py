import json
import base64
import requests


TOKEN = ""

def request_spotify_access_token():
    global TOKEN

    creds = read_spotify_client_credentials()
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
