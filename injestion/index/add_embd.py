import json, os
from uuid import uuid4
from pinecone import Pinecone
from fastapi import HTTPException
from langchain_core.documents import Document
from typing import Optional, Dict, Any, Union
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from config.config import OPENAI_KEY, PINECONE_API_KEY
from langchain_community.document_loaders import TextLoader
from langchain_experimental.text_splitter import SemanticChunker
from helpers.logger import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Initialize embedding model and Pinecone client
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_KEY)
text_splitter = SemanticChunker(embedding_model)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("assessment")
vector_store = PineconeVectorStore(index=index, embedding=embedding_model)

def advnce_new_embedding(
    text: Optional[str] = None,
    title: Optional[str] = None,
    file_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Adds a single or multiple entries to Pinecone:
    - From a textbox (with optional chunking)
    - Or from an uploaded .txt file (chunked automatically)
    """
    try:
        if file_path and file_path.endswith(".json"):
            # vector_store = PineconeVectorStore(index=index, embedding=embedding_model)
            with open(file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
            documents = []
            ids = []
            for i, item in enumerate(data["questions"]):
                q = item["question"]
                a = item["answer"]
                text = f"Q: {q}\nA: {a}"
                doc = Document(page_content=text, metadata={"source": "faq"})
                documents.append(doc)
                ids.append(f"faq{i+1}")
            vector_store.add_documents(documents=documents, ids=ids)
            return {"status": "success", "id": f"{len(ids)}_docs_uploaded", "message": "✅ JSON uploaded and embedded."}

        if file_path and file_path.endswith(".txt"):
            # Handle uploaded .txt file
            logger.info(f"Processing uploaded file: {file_path}")
            if not file_path.endswith(".txt"):
                raise ValueError("Only .txt files are supported.")

            with open(file_path, encoding='utf-8') as f:
                raw_text = f.read()
            documents = text_splitter.create_documents([raw_text])
            vector_store.add_documents(documents)

            return {
                "status": "success",
                "id": str(uuid4()),
                "message": f"{len(documents)} chunks from uploaded file stored successfully."
            }

        elif text:
            word_count = len(text.strip().split())
            logger.info(f"Processing input text of {word_count} words")

            if word_count > 800:
                logger.info("Chunking input text due to large size.")
                docs = text_splitter.create_documents([text])
                vector_store.add_documents(docs)
                return {
                    "status": "success",
                    "id": str(uuid4()),
                    "message": f"Long text chunked into {len(docs)} segments and stored."
                }

            # Short text — directly embed
            entry_id = str(uuid4())
            embedding = embedding_model.embed_query(text.lower())

            if not embedding:
                raise HTTPException(status_code=500, detail="Failed to generate embedding.")

            metadata = {"text": text}
            if title:
                metadata["title"] = title

            index.upsert([(entry_id, embedding, metadata)])

            return {
                "status": "success",
                "id": entry_id,
                "message": "Short text embedded and added successfully."
            }

        else:
            raise ValueError("Either 'text' or 'file_path' must be provided.")

    except Exception as e:
        logger.error(f"Error in embedding entry: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))