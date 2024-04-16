import requests
from bs4 import BeautifulSoup


def scrape_food_text(url):
    # Make a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the article tag with class "single"
        article = soup.find('article', class_='single')

        if article:
            # Remove elements by ID
            for elem_id in ['inpageEssb', 'meta2', 'newfo-Content']:
                element = article.find(id=elem_id)
                if element:
                    element.extract()

            # Remove elements by class name
            for class_name in ['crossPromo', 'box']:
                elements = article.find_all(class_=class_name)
                for element in elements:
                    element.extract()

            # Remove elements by tag
            for tag in article.find_all(True):
                # Keep only h1-h6 and p tags
                if tag.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']:
                    tag.extract()

            # Extract text content from the cleaned article
            article_text = article.get_text(separator='\n')
            title = article.find('h1').get_text().strip()
            return title, article_text.strip()

        else:
            print("Article not found on the page")
            return None

    else:
        print("Failed to retrieve the webpage")
        return None
