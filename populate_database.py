import argparse
import os
import shutil
import logging
from typing import List

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
# from langchain_chroma import Chroma
from langchain.vectorstores import Chroma

from tqdm import tqdm  # Add this import at the top

from get_embedding_function import get_embedding_function

# Constants
CHROMA_PATH = "chroma"
DATA_PATH = "data"

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def main():
    args = parse_arguments()

    if args.reset:
        logging.info("✨ Clearing Chroma database")
        clear_database()

    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Chroma Vector Store Loader")
    parser.add_argument("--reset", action="store_true", help="Reset the vector store database.")
    return parser.parse_args()


def load_documents() -> List[Document]:
    logging.info(f"📂 Loading documents from '{DATA_PATH}'")
    loader = PyPDFDirectoryLoader(DATA_PATH)
    return loader.load()


def split_documents(documents: List[Document]) -> List[Document]:
    logging.info(f"✂️ Splitting {len(documents)} documents into chunks")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return splitter.split_documents(documents)


def add_to_chroma(chunks: List[Document]) -> None:
    logging.info("🔗 Initializing Chroma DB")
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function(),
    )

    chunks = assign_unique_chunk_ids(chunks)

    existing_ids = set(db.get(include=[])["ids"])
    logging.info(f"📦 Existing documents in DB: {len(existing_ids)}")

    new_chunks = [chunk for chunk in chunks if chunk.metadata["id"] not in existing_ids]

    if new_chunks:
        logging.info(f"🆕 Adding {len(new_chunks)} new documents to DB")

        # Show progress with tqdm
        new_chunk_ids = []
        for chunk in tqdm(new_chunks, desc="📥 Adding to DB", unit="doc"):
            new_chunk_ids.append(chunk.metadata["id"])
            db.add_documents([chunk], ids=[chunk.metadata["id"]])

        db.persist()
        logging.info("💾 Database persisted with new documents.")
    else:
        logging.info("✅ No new documents to add")
    

def assign_unique_chunk_ids(chunks: List[Document]) -> List[Document]:
    last_page_id = None
    chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source", "unknown")
        page = chunk.metadata.get("page", 0)
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            chunk_index += 1
        else:
            chunk_index = 0

        chunk.metadata["id"] = f"{current_page_id}:{chunk_index}"
        last_page_id = current_page_id

    return chunks


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        logging.info("🗑️ Database directory removed.")
    else:
        logging.info("⚠️ No database directory to remove.")


if __name__ == "__main__":
    main()

