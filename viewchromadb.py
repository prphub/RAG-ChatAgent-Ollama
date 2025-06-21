import logging
from langchain_chroma import Chroma
from get_embedding_function import get_embedding_function

# Constants
CHROMA_PATH = "chroma"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def view_chroma_data(limit: int = 10):
    """
    View stored documents from ChromaDB up to a specified limit.
    """
    logging.info("🔍 Connecting to Chroma DB")

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function(),
    )

    data = db.get()
    ids = data.get("ids", [])
    documents = data.get("documents", [])
    metadatas = data.get("metadatas", [])

    logging.info(f"📦 Total documents in DB: {len(ids)}")

    for i in range(min(limit, len(ids))):
        print(f"\n--- Document {i + 1} ---")
        print(f"ID: {ids[i]}")
        print(f"Metadata: {metadatas[i]}")
        print(f"Content: {documents[i][:300]}...")  # Show preview

if __name__ == "__main__":
    view_chroma_data(limit=10)  # Change limit as needed

