import os
from dotenv import load_dotenv

def load_credentials():
    """Loads credentials from a .env file for security."""
    load_dotenv()
    username = os.getenv("PESU_USERNAME")
    password = os.getenv("PESU_PASSWORD")
    return username, password

def clean_string(raw_str):
    """
    to remove escape characters and quotes from server strings
    we use this to get a clean version of the semester id
    """
    if not raw_str:
        return ""
    return raw_str.replace('\\', '').replace('"', '').strip()


