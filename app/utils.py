import os
from dotenv import load_dotenv

def load_credentials():
    load_dotenv()
    return os.getenv("PESU_USERNAME"), os.getenv("PESU_PASSWORD")  

def clean_string(text): # we define this function to get a clean version of the semester id that we retreive
    if not text:
        return ""
    return text.replace('\\', '').replace('"', '').strip()
