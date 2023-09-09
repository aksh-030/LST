import re
import cv2 as cv
from PIL import Image
from pytesseract import pytesseract
import requests
import json
#os.environ['TESSDATA_PREFIX'] = "C:/Program Files/Tesseract-OCR/tessdata"

# Function to split large string
def splitter(n, s):
    pieces = s.split()
    return (" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n))

# Function to detect script
def detect_image_lang(path):
    osd = pytesseract.image_to_osd(path)
    #print(osd)
    script = re.search("Script: ([a-zA-Z]+)\n", osd).group(1)
    #conf = re.search("Script confidence: (\d+\.?(\d+)?)", osd).group(1)
    return script

# Function to extract script
def tesseract(code, src):
    i = Image.open(src)
    i.load()
    t = pytesseract.image_to_string(i, lang=code)
    return t

def exec_wc():
    pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # Open Webcam
    cam = cv.VideoCapture(0)
    cv.namedWindow("Capture", cv.WINDOW_NORMAL)
    cv.setWindowProperty("Capture", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

    # Capture and save
    while True:
        _,img = cam.read()
        cv.imshow("Capture",img)
        if cv.waitKey(1) & 0xFF==ord('s') :
            cv.imwrite("captured.jpg", img)
            break

    cam.release()
    cv.destroyAllWindows()

    # Codes for lang
    script = {
    "Devanagari": "hin",
    "Cyrillic": "rus",
    "Japanese": "jpn",
    "Latin": "ita",
    "Hangul": "kor",
    "Han": "chi_sim",
    "Arabic": "ara"
    }

    src = "captured.jpg"
    script_name = detect_image_lang(src)
    code = script[script_name]

    # Extracted text
    text = tesseract(code, src)
    print(text)

    # Translate
    translated=""
    for piece in splitter(200, text):
        r = requests.post('http://127.0.0.1:5000/translate', data={'q': piece,'source': "auto",'target': "en",'format': "text",'api_key': ""})
        data = json.loads(r.text)
        translated+=data["translatedText"]
    return translated