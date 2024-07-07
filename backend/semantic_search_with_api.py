from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

app = FastAPI()

# Load embeddings and vector store
embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
)

script_dir = os.path.dirname(os.path.abspath(__file__))
index_file = os.path.join(script_dir, "index.faiss")
pickle_file = os.path.join(script_dir, "index.pkl")

if not os.path.isfile(index_file):
    raise FileNotFoundError(f"FAISS index file not found at {index_file}")

vectorstore = FAISS.load_local(script_dir, embeddings, allow_dangerous_deserialization=True)
retriever_vectordb = vectorstore.as_retriever(search_kwargs={"k": 20})

# Set up Cohere
os.environ["COHERE_API_KEY"] = "OjjnLULlAuvZBqBFNr3CUmreGvKwOP0UnAFMhgmH"
compressor = CohereRerank(top_n=10)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever_vectordb
)

class Query(BaseModel):
    text: str

class MetadataResponse(BaseModel):
    metadata: List[Dict]

@app.post("/retrieve", response_model=MetadataResponse)
async def retrieve_documents(query: Query):
    try:
        compressed_docs = compression_retriever.get_relevant_documents(query.text)
        metadata_list = [doc.metadata for doc in compressed_docs]
        return MetadataResponse(metadata=metadata_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)