import requests
import time
from bs4 import BeautifulSoup
from .utils import clean_string

class PESUWrapper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = "https://www.pesuacademy.com/Academy/"   #it is the root url of pesu academy website
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        })
        self.csrf = None
        self.semester_id = None

    def login(self):
        try:
            res = self.session.get(self.base_url)
            soup = BeautifulSoup(res.text, "html.parser")
            initial_csrf = soup.find("meta", {"name": "csrf-token"})["content"]

            login_payload = {
                "_csrf": initial_csrf,                #Pesu academy uses two csrf tokens,  one to initialize the login process, and another final csrf token after we are redirected
                "j_username": self.username,          #for the login payload alone, we need the initial_csrf
                "j_password": self.password
            }
            self.session.post(f"{self.base_url}j_spring_security_check", data=login_payload)

            profile_res = self.session.get(f"{self.base_url}s/studentProfilePESU")
            profile_soup = BeautifulSoup(profile_res.text, "html.parser")
            csrf_tag = profile_soup.find("meta", {"name": "csrf-token"})  #got the format by manually going through the html 
            
            if not csrf_tag:
                return False
                
            self.csrf = csrf_tag["content"]
            return True
        except Exception:
            return False

    def get_semester_id(self):
        try:
            ts = int(time.time() * 1000)
            url = f"{self.base_url}a/studentProfilePESU/getStudentSemestersPESU?_={ts}"
            res = self.session.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            option = soup.find("option", value=True)
            if option:
                self.semester_id = clean_string(option.get("value"))  #using the clean_string function that we created to retreive the clean semester id
                return True
            return False
        except Exception:
            return False

    def fetch_attendance_raw(self):
        if not self.csrf or not self.semester_id:
            return None

        payload = {
            "controllerMode": "6407",        #used http client to retreive the below values
            "actionType": "8",
            "batchClassId": str(self.semester_id),  #use the retreived value of sem id
            "menuId": "660",
            "_csrf": str(self.csrf) # use the new csrf token that we get after the login process
        }
        headers = {
            "x-csrf-token": str(self.csrf),
            "Referer": f"{self.base_url}s/studentProfilePESU"
        }

        res = self.session.post(f"{self.base_url}s/studentProfilePESUAdmin", data=payload, headers=headers)
        return res.text if res.status_code == 200 else None
