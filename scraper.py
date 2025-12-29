from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from config import get_db_connection  # ✅ import from config

def scrape_website(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(1)

    # Scroll to bottom (dynamic content)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    products = []
    items = driver.find_elements(By.CSS_SELECTOR, "div.swiper-slide")

    for item in items:
        try:
            title = item.find_element(By.CSS_SELECTOR, "img.media-image").get_attribute("alt")
        except:
            title = ""
        try:
            link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            link = ""
        try:
            image = item.find_element(By.CSS_SELECTOR, "img.media-image").get_attribute("src")
        except:
            image = ""
        try:
            price = item.find_element(By.CSS_SELECTOR, ".price-item--regular").text
        except:
            price = ""

        products.append({
            "title": title.strip(),
            "price": price.strip(),
            "link": link.strip(),
            "image": image.strip()
        })

    driver.quit()

    # Save to DB
    conn = get_db_connection()  # ✅ yahi sahi hai
    cursor = conn.cursor()
    for p in products:
        cursor.execute("""
            INSERT INTO products (title, price, link, image)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE price=%s, image=%s
        """, (p["title"], p["price"], p["link"], p["image"], p["price"], p["image"]))
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(products)} products scraped and saved to database.")
