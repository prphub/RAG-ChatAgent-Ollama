# Python RAG Tutorial (with Local LLMs): AI For Your PDFs

## Youtube Link
https://www.youtube.com/watch?v=2TJxpyO3ei4

## Github link
https://github.com/pixegami/rag-tutorial-v2

## Create venv ragvenv
D:\ws\ai\rag-tutorial-v2> `python -m venv ragvenv`

## Activate
D:\ws\ai\rag-tutorial-v2> `ragvenv\Scripts\activate` <br/>
(ragvenv) PS D:\ws\ai\rag-tutorial-v2>

## Install libraries

(ragvenv) PS D:\ws\ai\rag-tutorial-v2> `pip install -r requirements.txt`

## Process 
Original Text --> Text Splitter (Chunks of Text into Vector Database) --> Embeddings

## Download Ollama for Windows
1. Download Ollama installer --> https://ollama.com/download/windows
   
2. Open Command Prompt as Administrator
    
3. Navigate to download folder where `OllamaSetup.exe` is downloaded --> `cd D:\downloads\ai`
    
4. Execute following command with your desired path --> `.\OllamaSetup.exe /DIR="D:\sw\Ollama"`

## Ollama Setup: Using mistral model
-- ollama pull llama2 <br/>
`ollama pull mistral`

`ollama serve`

http://localhost:11434

# Note:
PROMPT_TEMPLATE = """
Answer the question based only on the following context:
{context}

Answer the question based on the above context: {context}

## Commands
Make changes to the ollma data model  name in the below two files
(mistral or llama2)

get_embedding_function.py
query_data.py

## to populate the database
`python populate_database.py`

## to query the data from generated/populated database

python query_data.py "How do I build a hotel in Monopoly?"

python query_data.py "How many clues can I give in Codenames?"

python query_data.py "How do I get out of jail in Monopoly?"

## to view data from chroma vector db
python viewchromadb.py