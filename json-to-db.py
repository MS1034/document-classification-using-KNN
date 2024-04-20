import json
from Preprocessing.preprocessor import text_preprocessing
import os
from dotenv import load_dotenv
from database import Database
# Function to read JSON file


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


load_dotenv()
uri = os.getenv('MONGO_URI')

db = Database('Document-Classification-DB', 'Articles', uri)

# Load articles from JSON file
articles = read_json_file(
    '/media/subhan/New Volume/BSCS/6.SIXTH SEM/CS-380 GT/Project/Scrapping/Sports/scraped_articles.json')

# Iterate over each article
for article in articles:
    # Extract article information
    article_text = article['Article']
    category = article['Category']
    title = ""

    # Scrape the article text

    # Check if title and article text are not None
    if article_text:
        # Preprocess the article text
        preprocessed_text = text_preprocessing(article_text)

        # Prepare the data to be inserted into the database
        data = {
            "url": "",
            "category": category,
            "title": title,
            "text": article_text,
            "preprocessed-text": preprocessed_text,
            "len-raw-text": len(article_text.split()),
            "len-preprocessed-text": len(preprocessed_text.split())
        }

        db.insert_data(data)
