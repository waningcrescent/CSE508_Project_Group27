import pytesseract
from PIL import Image
import tempfile
import os

def ocr(img_path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    tempfile.tempdir = r'C:\Temp'
    os.makedirs(tempfile.tempdir, exist_ok=True)
    try:
        image = Image.open(img_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None