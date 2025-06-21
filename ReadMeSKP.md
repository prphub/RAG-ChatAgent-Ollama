# Youtube Link
https://www.youtube.com/watch?v=2TJxpyO3ei4

# Github link
https://github.com/pixegami/rag-tutorial-v2

# Create venv vragtut
C:\WS\ollama\RAG\rag-tutorial-v2> python -m venv ragvenv

# Activate
(vragtut) C:\WS\ollama\RAG\rag-tutorial-v2>ragvenv\Scripts\activate

# Install libraries

(vragtut) C:\WS\ollama\RAG\rag-tutorial-v2>  

pip install -U langchain-community
pip install -U langchain-chroma
pip install -U langchain-ollama


(vragtut) C:\WS\ollama\RAG\rag-tutorial-v2> pip install -r requirements.txt
###  pip install langchain   # LLM Library
### pip install chromdb     # Vector Storage
### pip install pypdf       # Loading PDFs
### pip install pytest      # Unit Testing



# Process 
Original Text-->Text Splitter (Chunks of Text into Vector Database)--> Embeddings

# Ollama Setup - currently using mistral model
-- ollama pull llama2
ollama pull mistral

ollama serve

http://localhost:11434


PROMPT_TEMPLATE = """
Answer the question based only on the following context:
{context}

---
Answer the question based on the above context: {context}
---


# Commands
Make changes to the ollma data model  name in the below two files
(mistral or llama2)

get_embedding_function.py
query_data.py

# to populate the database
python populate_database.py

# to query the data from generated/populated database

python query_data.py "How do I build a hotel in Monopoly?"

python query_data.py "How many clues can I give in Codenames?"

python query_data.py "How do I get out of jail in Monopoly?"

# to view data from chroma vector db
python viewchromadb.py