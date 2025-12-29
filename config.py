import os
# config.py
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",         # apna MySQL password
        database="scraper_db"  # database name
    )


# For SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), "database", "data.db")

# For MySQL (Optional)
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "scraper_db"
}
