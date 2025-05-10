import os
import json
from pinecone import Pinecone
# from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from config.config import OPENAI_KEY, PINECONE_API_KEY
# OPENAI_KEY = os.getenv('OPENAI_API_KEY')
# PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
# load_dotenv()

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("assessment")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key = OPENAI_KEY)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# Load FAQ JSON file
with open("data/Ecommerce_FAQ_Chatbot_dataset.json", "r") as f:
    mydata = json.load(f)

# Create LangChain documents
documents = []
ids = []

for i, item in enumerate(mydata["questions"]):
    q = item["question"]
    a = item["answer"]
    text = f"Q: {q}\nA: {a}"
    doc = Document(
        page_content=text,
        metadata={"source": "faq"}
    )
    documents.append(doc)
    ids.append(f"faq{i+1}")

# Add documents to Pinecone vector store
vector_store.add_documents(documents=documents, ids=ids)