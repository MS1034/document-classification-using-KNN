from database import Database
from dotenv import load_dotenv

import os

def main():
    load_dotenv()
    uri = os.getenv('MONGO_URI')

    db = Database('Document-Classification-DB', 'Articles', uri)
    documents = db.get_all_data()
    print(documents)

if __name__ == "__main__":
    main()