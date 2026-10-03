from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def get_habr_news(limit=5):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://habr.com/ru/articles/")
    time.sleep(5)

    articles = driver.find_elements(By.CSS_SELECTOR, "a[class='tm-title__link']")

    news = []
    for article in articles[:limit]:
        text = article.text.strip()
        link = article.get_attribute("href")
        if text and link:
            news.append({"article": text, "link": link})

    driver.quit()
    return news

news = get_habr_news(limit=5)

for n in news:
    print(n["article"])
    print(n["link"])
    print()