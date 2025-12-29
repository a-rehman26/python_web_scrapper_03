from flask import Flask, render_template, request, redirect, send_file
from scraper import scrape_website
from models import get_db_connection
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        url = request.form.get("url")
        scrape_website(url)

    cursor.execute("SELECT * FROM products")
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
