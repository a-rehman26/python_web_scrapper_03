from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_website(url):
    options = Options()
    options.add_argument("--headless=new")  # newer headless mode is more reliable
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # Wait until at least one product loads
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.card__content"))
    )

    # Scroll to bottom to load lazy content
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Trigger all swiper slides
    driver.execute_script("""
    document.querySelectorAll('.swiper-container').forEach(swiper => {
        if (swiper.swiper) {
            swiper.swiper.update();
            for (let i = 0; i < swiper.swiper.slides.length; i++) {
                swiper.swiper.slideTo(i, 0, false);
            }
        }
    });
    """)
    time.sleep(2)  # give time for images to load

    products = []
    items = driver.find_elements(By.CSS_SELECTOR, "div.card.card--standard")

    for item in items:
            # Title
        try:
            title = item.find_element(By.CSS_SELECTOR, "div.card__content.hi2 h3.card__heading a").text
        except:
            title = ""
        
        # Link
        try:
            link = item.find_element(By.CSS_SELECTOR, "h3.card__heading a").get_attribute("href")
        except:
            link = ""
        
        # Price
        try:
            price = item.find_element(By.CSS_SELECTOR, ".price-item--regular").text
        except:
            price = ""
        
        # Image (first one from hidden divs)
        try:
            img_div = item.find_element(By.CSS_SELECTOR, "div.item-swatch > div[data-image]")
            image = img_div.get_attribute("data-image")
            if image.startswith("//"):
                image = "https:" + image
        except:
            image = ""

        products.append({
            "title": title.strip(),
            "price": price.strip(),
            "link": link.strip(),
            "image": image.strip()
        })


    driver.quit()
    return products
