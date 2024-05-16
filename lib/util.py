import os
import string
import random


def bpm_to_fps(bpm):
    # we want to flicker, so multiply times 2
    return (bpm / 60) * 2


def fetch_bpm():
    # dummy for now
    return 140


def fetch_images():
    return os.listdir("img")


def generate_random_string(length):
    # see https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(length))
