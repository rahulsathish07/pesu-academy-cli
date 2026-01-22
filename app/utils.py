import os
from dotenv import load_dotenv
import json

def load_credentials():
    load_dotenv()
    return os.getenv("PESU_USERNAME"), os.getenv("PESU_PASSWORD")  

def clean_string(text): # we define this function to get a clean version of the semester id that we retreive
    if not text:
        return ""
    return text.replace('\\', '').replace('"', '').strip()

def save_cache(data, filename="marks_cache.json"):
    with open(filename, "w") as f:
        json.dump(data,f)

def load_cache(filename = "marks_cache.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return None


