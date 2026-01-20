from bs4 import BeautifulSoup

def parse_attendance_html(html_content):
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, "html.parser")
    rows = soup.find_all("tr")
    
    attendance_list = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 4:      #in pesuacademy there 0th row by itself starts with the attendance data and it is not a header row, hence we do not slice it.
            code = cols[0].get_text(strip=True)
            name = cols[1].get_text(strip=True)
            
            if "Course Code" in code or not code:
                continue
                
            attendance_list.append({
                "course_code": code,
                "course_name": name,
                "total_classes": cols[2].get_text(strip=True),
                "percentage": cols[3].get_text(strip=True)
            })
            
    return attendance_list
