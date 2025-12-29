import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",        # replace with your MySQL username
        password="",        # replace with your MySQL password
        database="scraper_db"
    )
    return conn

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        price VARCHAR(50),
        link TEXT,
        image TEXT
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("MySQL database initialized!")

if __name__ == "__main__":
    initialize_db()
