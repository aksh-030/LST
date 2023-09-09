# Imports
import fitz
from PIL import Image
import pytesseract
import zipfile
from bs4 import BeautifulSoup
from docx import Document
from ebooklib import epub
import requests
import json
import os
import re

# Function to split large string
def splitter(n, s):
    pieces = s.split()
    return (" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n))

# Function to extract text from PDF
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to extract text from image
def extract_text_from_image(path):
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    
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

    # Function to detect script
    def detect_image_lang(path):
        osd = pytesseract.image_to_osd(path, config='--psm 0 -c min_characters_to_try=10')
        script_name = re.search("Script: ([a-zA-Z]+)\n", osd).group(1)
        #conf = re.search("Script confidence: (\d+\.?(\d+)?)", osd).group(1)
        return script_name

    # Function to extract script
    def tesseract(code):
        i = Image.open(path)
        i.load()
        t = pytesseract.image_to_string(i, lang=code)
        return t

    script_name = detect_image_lang(path)
    code = script[script_name]

    # Extracted text
    text = tesseract(code)
    return text

# Function to extract text from text files
def extract_text_from_text_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Function to extract text from .odt files
def extract_text_from_odt(path):
    text = ""
    with zipfile.ZipFile(path, "r") as zip_file:
        content = zip_file.read("content.xml")
        soup = BeautifulSoup(content, "xml")
        for paragraph in soup.find_all("text:p"):
            text += paragraph.get_text() + "\n"
    return text

# Function to extract text from .docx files
def extract_text_from_docx(path):
    doc = Document(path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

# Function to extract text from .epub files
def extract_text_from_epub(path):
    book = epub.read_epub(path)
    text = ""
    for item in book.items:
        if isinstance(item, epub.EpubHtml):
            text += item.content.decode("utf-8")

    return text

# Function to extract text from .html files
def extract_text_from_html(path):
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    # You can further process or clean the HTML content if needed
    return text

def exec_file(path):
    # Dictionary that maps file extensions to corresponding functions
    file_extension_handlers = {
        ".pdf": extract_text_from_pdf,
        ".txt": extract_text_from_text_file,
        ".odt": extract_text_from_odt,
        ".docx": extract_text_from_docx,
        ".epub": extract_text_from_epub,
        ".html": extract_text_from_html,
        ".jpg": extract_text_from_image,
        ".jpeg": extract_text_from_image,
        ".png": extract_text_from_image,
        ".gif": extract_text_from_image,
        ".bmp": extract_text_from_image,
    }

    # Process a file based on its extension
    file_extension = os.path.splitext(path)[-1].lower()
    handler = file_extension_handlers.get(file_extension)
    if handler:
        text = handler(path)
    else:
        # Handle unsupported file types
        return "Unsupported file type"

    # Translated
    translated = ""
    for piece in splitter(500, text):
        r = requests.post('http://127.0.0.1:5000/translate', data={'q': piece,'source': "auto",'target': "en",'format': "text",'api_key': ""})
        data = json.loads(r.text)
        translated += data["translatedText"]
    return translated
