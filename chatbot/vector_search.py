from .vector_db import collection

def search_games(query):
    result = collection.query(
        query_texts=[query],
        n_results=5
    )

    return result["documents"][0]