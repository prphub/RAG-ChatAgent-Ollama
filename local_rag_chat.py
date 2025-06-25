import argparse
import logging
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
# from langchain_community.llms.ollama import Ollama
from langchain_ollama import OllamaLLM
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def main():
    """Parse command-line arguments and perform RAG-based query."""
    parser = argparse.ArgumentParser(description="Query a Chroma-based RAG system.")
    parser.add_argument("query_text", type=str, help="The input question to query.")
    args = parser.parse_args()

    try:
        query_rag(args.query_text)
    except Exception as e:
        logging.error(f"An error occurred while processing the query: {e}")


def query_rag(query_text: str) -> str:
    """
    Perform a Retrieval-Augmented Generation (RAG) query using a local Chroma DB and Ollama model.

    Args:
        query_text (str): The input question.

    Returns:
        str: The generated response from the language model.
    """
    # Load vector store
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Perform similarity search
    results = db.similarity_search_with_score(query_text, k=5)

    if not results:
        logging.warning("No relevant documents found.")
        print("No relevant documents found.")
        return ""

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
        context=context_text, question=query_text
    )

    # Run model
    # model = Ollama(model="mistral")
    # model = Ollama(model="llama2")
    # model = OllamaLLM(model="llama2")
    model = OllamaLLM(model="mistral")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", "Unknown") for doc, _ in results]
    formatted_response = f"\nResponse:\n{response_text}\n\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
