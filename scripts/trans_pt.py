# Imports
import requests
import json

# Function to split large string
def splitter(n, s):
    pieces = s.split()
    return (" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n))

# HTTP request
def exec_text(text):
    translated=""
    for piece in splitter(1000, text):
        r = requests.post('http://127.0.0.1:5000/translate', data={'q': piece,'source': "auto",'target': "en",'format': "text",'api_key': ""})
        data = json.loads(r.text)
        translated+=(data["translatedText"])
    return translated