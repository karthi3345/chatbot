import chromadb

client = chromadb.PersistentClient(
    path="./vectordb"
)

collection = client.get_or_create_collection(
    name="games"
)