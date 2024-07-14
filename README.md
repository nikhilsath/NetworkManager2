# Network Device Manager

A tool to test the accessibility of devices on a local network based on provided MAC addresses. This tool allows users to input MAC addresses and check if the corresponding devices are accessible on the local network.

## Features

- Input multiple MAC addresses to check their accessibility.
- Uses `arp-scan` to detect devices on the local network.
- Simple web interface to input MAC addresses and view results.

## Requirements

- Python 3.6 or higher
- Flask
- `arp-scan` tool (for network scanning)

## Installation

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/nikhilsath/NetworkManager2.git
cd NetworkManager2

Step 2: Set Up a Virtual Environment

Create and activate a virtual environment (optional but recommended):

bash

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Step 3: Install Dependencies

Install the required Python packages using pip:

bash

pip install -r requirements.txt

Step 4: Install arp-scan

Ensure that arp-scan is installed on your system. You can install it using Homebrew on macOS:

bash

brew install arp-scan

Usage
Step 1: Run the Flask Application

Start the Flask development server:

bash

sudo python3 run.py

The application will be available at http://127.0.0.1:5000.
Step 2: Access the Web Interface

Open your web browser and navigate to http://127.0.0.1:5000. You should see a form where you can input MAC addresses.
Step 3: Check Device Accessibility

    Enter MAC Addresses: Input one or more MAC addresses, separated by commas.
    Submit the Form: Click the "Check Devices" button to check the accessibility of the provided MAC addresses.
    View Results: The results will display the reachability status of each MAC address.

Project Structure

plaintext

NetworkManager2/
├── README.md
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── routes.py
│   ├── static/
│   │   └── styles.css
│   ├── templates/
│   │   └── index.html
├── data/
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── run.py
├── requirements.txt

File Descriptions

    app/__init__.py: Initializes the Flask application.
    app/config.py: Configuration settings for the application.
    app/routes.py: Contains the routes and logic for checking device accessibility.
    app/static/styles.css: Stylesheet for the web interface.
    app/templates/index.html: HTML template for the web interface.
    run.py: Entry point to run the Flask application.
    requirements.txt: List of Python dependencies.
    README.md: This readme file.
    .gitignore: Specifies files and directories to be ignored by Git.
    data/: Directory to store data files (currently empty).
    tests/: Directory containing test files.