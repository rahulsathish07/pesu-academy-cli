# PESU Academy CLI Tool
  
  ## Purpose
  This project is a modular Command Line Interface (CLI) tool designed to interact with the PESU Academy portal. It automates the process of authenticating with the portal, managing session-based security tokens (CSRF), and retrieving structured academic data such as attendance. The application logic is separated into distinct modules to ensure scalability and maintainability.
  
  ## Project Context
  This project was developed purely for educational purposes as a basic project including:
  * Web Scraping: Using BeautifulSoup and lxml to parse complex HTML structures.
  * Network Session Management: Utilizing the requests library to maintain persistent sessions and handle multi-step authentication handshakes.
  * Modular Software Architecture: Implementing a clean separation of concerns between network communication, data parsing, and user interface logic.
  * Security Best Practices: Managing sensitive credentials through environment variables and masked terminal inputs.
  
  ## Technical Architecture
  * app/wrapper.py: Handles the network layer, including login logic and raw data fetching.
  * app/attendance.py: Contains logic for parsing raw HTML tables into structured Python dictionaries.
  * app/utils.py: Provides helper functions for string sanitization and credential loading.
  * main.py: Serves as the entry point, coordinating the flow of the application and displaying data in a grid format.
  
  ## Installation and Usage
  1. Clone the repository and navigate to the directory. 
  2. To create a virtual environment, run `python3 -m venv venv` (on Windows, use `python -m venv venv`), then activate it using `source venv/bin/activate` for Linux/macOS or `venv\Scripts\activate` for Windows.
  3. Install dependencies: `pip install -r requirements.txt`.
  4. Ensure a `.env` file exists with `PESU_USERNAME` and `PESU_PASSWORD`, or be prepared to enter them in the terminal.
  5. Run the application: `python3 main.py`.
  
  ## Roadmap and Pending Features
  The following features are planned for future iterations of this project:
  - [x] Implement a result update detector to notify users when new grades are posted.
  - [x] Add support for internal marks data.
  - [ ] Create a tool for number of available bunks (e.g., classes needed for 75%).
  - [ ] Add a local caching mechanism to reduce redundant network requests.
  - [ ] Implement automatic `.env` creation after the first successful manual login.
  
  ## Disclaimer
  This is an unofficial tool and is not affiliated with PES University. It is intended for personal use and learning purposes.
