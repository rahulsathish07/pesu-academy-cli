import requests
from bs4 import BeautifulSoup
import time
from .utils import clean_string

class PESUWrapper:
    def __init__(self, username, password):
        """
        Initializes the PESU Academy Session.
        The username and password are passed dynamically from main.py.
        """
        self.username = username
        self.password = password
        self.base_url = "https://www.pesuacademy.com/Academy/"
        self.session = requests.Session()
        
        # Standard headers to mimic a real browser session
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        })
        
        self.csrf = None
        self.semester_id = None

    def login(self):
        """
        Handles the authentication flow:
        1. Fetches initial login page for the landing CSRF.
        2. Submits credentials to j_spring_security_check.
        3. Visits the profile page to capture the authenticated CSRF token.
        """
        try:
            # Step 1: Get initial landing page CSRF
            landing_res = self.session.get(self.base_url)
            soup = BeautifulSoup(landing_res.text, "html.parser")
            initial_csrf = soup.find("meta", {"name": "csrf-token"})["content"]

            # Step 2: POST Login Credentials
            login_payload = {
                "_csrf": initial_csrf,
                "j_username": self.username,
                "j_password": self.password
            }
            login_url = f"{self.base_url}j_spring_security_check"
            self.session.post(login_url, data=login_payload)

            # Step 3: Token Refresh - Get the authenticated session CSRF
            profile_url = f"{self.base_url}s/studentProfilePESU"
            profile_res = self.session.get(profile_url)
            profile_soup = BeautifulSoup(profile_res.text, "html.parser")
            
            csrf_tag = profile_soup.find("meta", {"name": "csrf-token"})
            if not csrf_tag:
                # If no CSRF tag is found on the profile page, login likely failed
                return False
                
            self.csrf = csrf_tag["content"]
            return True
        except Exception as e:
            print(f"Login failed during network request: {e}")
            return False

    def get_semester_id(self):
        """
        Fetches the latest semester ID from the dropdown list.
        Uses a timestamp to avoid cached responses.
        """
        try:
            timestamp = int(time.time() * 1000)
            url = f"{self.base_url}a/studentProfilePESU/getStudentSemestersPESU?_={timestamp}"
            res = self.session.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            
            option = soup.find("option", value=True)
            if option:
                # Use utility function to sanitize the ID string
                self.semester_id = clean_string(option.get("value"))
                return True
            return False
        except Exception:
            return False

    def fetch_attendance_raw(self):
        """
        Executes the POST request to the admin endpoint.
        Returns the raw HTML string for the attendance table.
        """
        if not self.csrf or not self.semester_id:
            return None

        url = f"{self.base_url}s/studentProfilePESUAdmin"
        
        # This payload corresponds to the 'Attendance' module
        payload = {
            "controllerMode": "6407",
            "actionType": "8",
            "batchClassId": str(self.semester_id),
            "menuId": "660",
            "_csrf": str(self.csrf)
        }
        
        headers = {
            "x-csrf-token": str(self.csrf),
            "Referer": f"{self.base_url}s/studentProfilePESU"
        }

        response = self.session.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
