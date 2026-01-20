import sys
from app.wrapper import PESUWrapper
from app.utils import load_credentials

def main():
    # 1. Load credentials from .env for security
    username, password = load_credentials()
    
    if not username or not password:
        print("Error: Credentials not found. Ensure your .env file is set up correctly.")
        sys.exit(1)

    # 2. Initialize the wrapper with your credentials
    print(f"--- PESU Academy Connection Test ---")
    print(f"User: {username}")
    wrapper = PESUWrapper(username, password)

    # 3. Step 1: Test Login Handshake
    print("\n[1/2] Attempting login...")
    if wrapper.login():
        print("✅ Login successful! Session established.")
        
        # 4. Step 2: Test Semester ID Retrieval
        print("[2/2] Fetching semester ID...")
        if wrapper.get_semester_id():
            print(f"✅ Semester ID retrieved: {wrapper.semester_id}")
            print("\nSuccess: Your credentials and authentication logic are working.")
        else:
            print("❌ Failed to retrieve Semester ID. Check the HTML tags in wrapper.py.")
    else:
        print("❌ Login failed. Check your credentials or initial CSRF token extraction.")

if __name__ == "__main__":
    main()
