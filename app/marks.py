from bs4 import BeautifulSoup

def parse_marks_html(html_content):
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, "html.parser")
    subjects = soup.find_all("div", class_="header-info")
    
    marks_list = []
    for sub in subjects:
        course_title = " ".join(sub.get_text().split()) #cleaning it here itself so i dont need to do it in the main.py 
        
        info_bar = sub.find_next("div", class_="dashboard-info-bar")
        if not info_bar:
            continue

        def get_val(label):
            label_node = info_bar.find("h6", string=lambda x: x and label in x) #im looking for label in <h6>
            if label_node:
                ''' Find the nearest span that contains the actual score
                Final ISA uses 'f-size-semi-big' without 'dark-text' '''
                val_node = label_node.parent.find("span", class_=lambda x: x and 'f-size' in x)
                if val_node:
                    return val_node.get_text(strip=True)
            return "NA"

        marks_list.append({
            "course": course_title,
            "isa1": get_val("ISA 1"),
            "isa2": get_val("ISA 2"),
            "assignment": get_val("Assignment"),
            "final_isa": get_val("FINAL ISA"),
            "esa": get_val("ESA")
        })
            
    return marks_list
