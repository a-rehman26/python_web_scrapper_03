from flask import Flask, render_template, request, send_file
from scraper import scrape_website
from models import get_db_connection
import pandas as pd

app = Flask(__name__)

def save_to_db(products):
    conn = get_db_connection()
    cursor = conn.cursor()
    for p in products:
        title = p.get("title", "")
        price = p.get("price", "")
        link = p.get("link", "")
        image = p.get("image", "")  # ensure this exists

        cursor.execute("""
            INSERT INTO products (title, price, link, image)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE price=%s, image=%s
        """, (title, price, link, image, price, image))
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    products = []
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            scraped = scrape_website(url)
            save_to_db(scraped)

    # Fetch all products from DB
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("index.html", products=products)

@app.route("/export")
def export():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM products", conn)
    conn.close()
    df.to_excel("scraped_data.xlsx", index=False)
    return send_file("scraped_data.xlsx", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
