import os
from dotenv import load_dotenv

def load_credentials():
    load_dotenv()
    return os.getenv("PESU_USERNAME"), os.getenv("PESU_PASSWORD")

def clean_string(text):
    if not text:
        return ""
    return text.replace('\\', '').replace('"', '').strip()
