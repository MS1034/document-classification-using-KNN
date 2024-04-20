from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

urls = ['https://www.businessblogshub.com/category/content-marketing/',
        'https://www.businessblogshub.com/category/accounting-finance/']
scraped_cleaned_articles = []

def clean(div):
    driver.execute_script("""
    var content = arguments[0];
    var removeElements = ['div.shared-counts-wrap', 'div.ez-toc-container'];
    removeElements.forEach(function(selector) {
        var toRemove = content.querySelector(selector);
        if (toRemove) {
            toRemove.remove();
        }
    });
    """, div)


def extract_links(url):
    driver.get(url)
    list_items = driver.find_elements(By.CSS_SELECTOR, "li.mvp-blog-story-wrap")
    links = []

    for item in list_items:
        link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
        links.append(link)

    return links

def scrap(url):
    driver.get(url)

    title = driver.find_element(By.CSS_SELECTOR, "h1.mvp-post-title").text
    content_div = driver.find_element(By.ID, "mvp-content-main")
    clean(content_div)

    content_text = content_div.text
    article_data = {
                'Category': 'Business & Finance',
                'Article': title + " \n " + content_text
            }
    
    return article_data

def save(data):
    with open("scraped_articles1.json", "a", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def scrap_all():    
    for url in urls:
        data = []

        for link in extract_links(url):
            article = scrap(link)
            data.append(article)
        
        save(data=data)


driver = webdriver.Chrome()
scrap_all()
driver.quit()
