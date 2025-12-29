## website Scraper & Flask Dashboard

This project scrapes product data (title, price, image, link) from **zelburry** website and stores it in a MySQL database. It also provides a Flask web interface to view and export scraped data.

---

## Requirements

- Python 3.13
- MySQL Database
- Virtual Environment (`env` recommended)
- Google Chrome (for Selenium)
- ChromeDriver (handled automatically via `webdriver-manager`)

---

Create & activate virtual environment

python -m venv env
# Windows
env\Scripts\activate
# macOS / Linux
source env/bin/activate

Install dependencies

pip install -r requirements.txt

Configure database

Edit config.py (or your own DB config) to match your MySQL credentials:


Run Flask App

python app.py

Open in browser

Go to: http://127.0.0.1:5000/
in input paste this sample url:
https://zellbury.com/collections/outerwear