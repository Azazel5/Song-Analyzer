# Song Lyrics Analyzer


import json
import sys 
import re
import urllib.request
import config 
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from bs4 import BeautifulSoup
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    KeywordsOptions,
    EmotionOptions,
    ConceptsOptions,
    RelationsOptions,
    MetadataOptions
)

authenticator = IAMAuthenticator(
    config.api_key)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version=config.version,
    authenticator=authenticator
)

natural_language_understanding.set_service_url(
    config.url)

def song_stripper(artist, song_title):
    artist = artist.strip()
    song_title = song_title.strip()
    artist = artist.lower()
    song_title = song_title.lower()
    artist = re.sub('[^a-zA-Z0-9]+', "", artist)
    song_title = re.sub('[^a-zA-Z0-9]+', "", song_title)
    if artist.startswith("the"):
        artist = artist[3:]
    return "https://www.azlyrics.com/lyrics/" + artist + "/" + song_title + ".html"

def get_lyrics_from_AZwebsite(artist, song_title):
    url = song_stripper(artist, song_title)
    try:
        az_lyrics = urllib.request.urlopen(url).read()
        bs4 = BeautifulSoup(az_lyrics, 'html.parser')
        div_elem = bs4.find("div", attrs={"id": None, "class": None})
        song_lyrics = str(div_elem).replace("<br>", "").replace(
            "<br/>", "").replace("<div>", "").replace("</div>", "").replace("<i>", "").replace("</i>", "")
        return song_lyrics.split("<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->")[1].strip()
    except Exception as error:
        print("Error occurred: " + str(error))
        sys.exit()

def get_song_metadata(artist, song_title):
    url = song_stripper(artist, song_title)
    response = natural_language_understanding.analyze(
    url=url,
    features=Features(metadata=MetadataOptions())).get_result()
    print(json.dumps(response, indent=2))
    return None


def analyze_emotion(lyrics):
    response = natural_language_understanding.analyze(
        text=lyrics,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=5),
            keywords=KeywordsOptions(emotion=True, sentiment=True, limit=10),
            concepts=ConceptsOptions(limit=5),
            relations=RelationsOptions())
    ).get_result()

    print(json.dumps(response, indent=2))




