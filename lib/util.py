import os
import base64
import string
import random

import lib.auth as auth


def bpm_to_fps(bpm):
    # we want to flicker, so multiply times 2
    return (bpm / 60) * 2


def fetch_images():
    return os.listdir("img")


def generate_random_string(length):
    # see https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(length))


def encode_client_authentication_token():
    creds_formatted = f"{auth.CLIENT_ID}:{auth.CLIENT_SECRET}"
    creds_ascii = creds_formatted.encode("ascii")

    creds_base64_bytes = base64.b64encode(creds_ascii)

    return creds_base64_bytes.decode("ascii")
