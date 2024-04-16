from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

scroll_times = 4
urls = ['https://www.espn.in/cricket/story/_/id/39952006/ipl-2024-rcb-vs-srh-maxwell-takes-break-refresh-asking-rested-rcb',
        'https://www.espn.in/football/story/_/id/39953714/bayern-season-failure-champions-league-title-kane',
        'https://www.espn.in/badminton/story/_/id/39757544/swiss-open-2024-lakshya-sen-pv-sindhu-kidambi-srikanth-olympic-qualification-spots',
        'https://www.espn.in/nba/story/_/id/39950411/nba-playoffs-2024-never-harder-lebron-steph',
        'https://www.espn.in/field-hockey/story/_/id/39938629/india-vs-australia-hockey-series-takeaways-fulton-harmanpreet-sreejesh-paris-olympics']

scraped_cleaned_articles = []

def scroll():
    for _ in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2.5)


def clean(article):
    driver.execute_script("""
        var article = arguments[0];
        var selectors = ['footer', 'aside', '.article-meta', '.content-reactions'];
        selectors.forEach(function(selector) {
            var elements = article.querySelectorAll(selector);
            elements.forEach(function(element) {
                element.remove(); 
            });
        });
    """, article)


def scrap_and_save(url):
    driver.get(url)
    scroll()
    articles = driver.find_elements(By.CSS_SELECTOR, "section#article-feed article")
    data = []
    with open("scraped_articles.json", "a", encoding="utf-8") as file:
        for article in articles:
            clean(article)

            article_data = {
                'Category': 'Sports',
                'Article': article.text.strip()
            }
            data.append(article_data)

        json.dump(data, file, ensure_ascii=False, indent=4)


def scrap_all():
    for url in urls:
        scrap_and_save(url)


driver = webdriver.Chrome()
scrap_all()
driver.quit()
