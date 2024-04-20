from Food.site_urls import urls_food_category
from database import Database
from dotenv import load_dotenv
from Food.food import scrape_food_text
from preprocessor import text_preprocessing
import os


def main():
    load_dotenv()
    uri = os.getenv('MONGO_URI')

    db = Database('Document-Classification-DB', 'Articles', uri)

    failed_urls = []

    # Iterate through each URL and category in the urls_food_category dictionary
    for url, category in urls_food_category.items():
        try:
            # Scrape and extract text from the URL
            title, article_text = scrape_food_text(url)
            preprocessed_text = text_preprocessing(article_text)
            # Check if title and article_text are not None
            if title and article_text:
                # Prepare the data to be inserted into the database
                data = {
                    "url": url,
                    "category": category,
                    "title": title,
                    "text": article_text,
                    "preprocessed-text": preprocessed_text,
                    "len-raw-text": len(article_text.split()),
                    "len-preprocessed-text": len(preprocessed_text.split())
                }
                db.insert_data(data)
                print(f"Data inserted for URL: {url}")
            else:
                print(f"Failed to scrape data from URL: {url}")
                # Add failed URL to the list
                failed_urls.append(url)
        except Exception as e:
            print(f"Exception occurred while scraping URL: {url}")
            print(f"Error message: {str(e)}")
            # Add failed URL to the list
            failed_urls.append(url)

    # Print failed URLs
    if failed_urls:
        print("\nFailed URLs:")
        for failed_url in failed_urls:
            print(failed_url)
    else:
        print("\nAll URLs scraped successfully.")


if __name__ == "__main__":
    main()
