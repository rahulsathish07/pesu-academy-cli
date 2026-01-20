import sys
import getpass
from tabulate import tabulate
from app.wrapper import PESUWrapper
from app.attendance import parse_attendance_html
from app.utils import load_credentials

def main():
    username, password = load_credentials()
    if not username or not password:
        print("PESU Academy Login")
        username = input("Enter SRN: ").strip()
        password = getpass.getpass("Enter Password: ")

    if not username or not password:
        print("Error: Username and password are required")
        sys.exit(1)

    wrapper = PESUWrapper(username, password)

    if not wrapper.login():
        print("Login failed, recheck credentials.")
        return

    if not wrapper.get_semester_id():
        print("Failed to retrieve Semester ID.")
        return

    raw_html = wrapper.fetch_attendance_raw()
    if not raw_html:
        print("Failed to fetch attendance data.")
        return

    attendance_data = parse_attendance_html(raw_html)
    if not attendance_data:
        print("No attendance records found.")
        return

    headers = ["Course Code", "Course Name", "Total Classes", "Percentage(%)"]
    table = [
        [item["course_code"], item["course_name"], item["total_classes"], item["percentage"]]
        for item in attendance_data
    ]

    print("\n" + tabulate(table, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
