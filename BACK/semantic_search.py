from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
# from langchain.retrievers import BM25Retriever, EnsembleRetriever

import os


from langchain_community.embeddings import HuggingFaceBgeEmbeddings
embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",  # alternatively use "sentence-transformers/all-MiniLM-l6-v2" for a light and faster experience.
    # model_kwargs={'device':'cpu'},
    # encode_kwargs={'normalize_embeddings': True}
)
# Get the directory containing the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the FAISS index files relative to the script directory
index_file = os.path.join(script_dir, "index.faiss")
pickle_file = os.path.join(script_dir, "index.pkl")

# Ensure the index file exists
if not os.path.isfile(index_file):
    raise FileNotFoundError(f"FAISS index file not found at {index_file}")

# Load the embeddings
# embeddings = ... (your embeddings loading logic)

# Load the FAISS index with dangerous deserialization enabled (if you trust the source)
vectorstore = FAISS.load_local(script_dir, embeddings, allow_dangerous_deserialization=True)

retriever_vectordb = vectorstore.as_retriever(search_kwargs={"k": 20})
query="machine learning engineer with 5 year experience"

docs_and_scores = retriever_vectordb.invoke(query)

os.environ["COHERE_API_KEY"] ="OjjnLULlAuvZBqBFNr3CUmreGvKwOP0UnAFMhgmH"
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.llms import Cohere
compressor = CohereRerank(top_n=10)
# top_n=5
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever_vectordb
)
compressed_docs = compression_retriever.get_relevant_documents(query)
for doc in compressed_docs:
    metadata = doc.metadata
    print(metadata)
unique_docs = list(set(metadata))
print(unique_docs)