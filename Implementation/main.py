from database import Database
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os
import nltk
from nltk.tokenize import word_tokenize
import networkx as nx
from gspan_mining import gSpan
from gspan_mining.graph import Graph

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
Graph.__init__()

def main():
    load_dotenv()
    uri = os.getenv('MONGO_URI')

    db = Database('Document-Classification-DB', 'Articles', uri)
    documents = db.get_all_data()
    document = documents[1]['preprocessed-text']

    DAGs = []
    count = 0
    for document in documents:
        G = nx.DiGraph()

        # Step 3: Add nodes and edges
        previous_word = None
        for word in word_tokenize(document['preprocessed-text']):
            if word not in G:
                G.add_node(word)
            if previous_word:
                # Add an edge from previous word to current word
                if G.has_edge(previous_word, word):
                    # we added this one before, just increase the weight by one
                    G[previous_word][word]['weight'] += 1
                else:
                    # new edge. add with weight=1
                    G.add_edge(previous_word, word, weight=1)
            previous_word = word

        count += 1
        DAGs.append(G)

    # graph_database = GraphDatabase()    
    # for G in DAGs:
    #     graph_database.add_graph(G)
    
    # # Create an instance of the gSpan algorithm
    # gspan_instance = gSpan(
    #     graph_database=graph_database,
    #     min_support=2  # Minimum support for a subgraph to be considered frequent
    # )
    
    # # Find frequent subgraphs
    # frequent_subgraphs = gspan_instance.run()
    # print("Frequent Subgraphs Found:")
    # for subgraph in frequent_subgraphs:
    #     print(subgraph)
    

if __name__ == "__main__":
    main()