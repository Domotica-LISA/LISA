import re
import feedparser
import time

WORDS = ["WEER"]

def handle(text, speaker, profile):
    entries = feedparser.parse("http://www.knmi.nl/rssfeeds/knmi-rssweer.cgi")['entries']

    for entry in entries:
        date_desc = entry['title'].split()[1].strip().lower()
        if date_desc == 'verwachting':
            speaker.say(entry['summary'].replace('<br />','')[:-33])
            time.sleep(2)

def isValid(text):
    return bool(re.search(r'\b(hoe is het weer vandaag|wat voor weer wordt het vandaag)\b', text, re.IGNORECASE))