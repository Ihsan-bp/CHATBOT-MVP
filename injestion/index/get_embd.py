from pinecone import Pinecone
from fastapi import APIRouter
from config.config import PINECONE_API_KEY
from helpers.logger import setup_logging, get_logger
from fastapi import APIRouter, HTTPException

# Set up logging and Create a logger
setup_logging()
logger = get_logger(__name__)

# Initialize Pinecone client and index
pc = Pinecone(api_key=PINECONE_API_KEY)

# get_g_q = APIRouter()

index_name = "assessment"
index = pc.Index(index_name)

# @get_g_q.get("/fetch-g_q")
def fetch_data():
    try:
        # Convert the generator to a list of IDs
        ids = list(index.list())
        logger.info(f"Retrieved {len(ids)} IDs")

        # If the first element is a list, we might have a nested structure
        if ids and isinstance(ids[0], list):
            ids = ids[0]
            logger.info(f"Flattened to {len(ids)} IDs")

        # Process IDs in batches
        batch_size = 50
        all_data = []

        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i:i + batch_size]
            logger.info(f"Fetching batch {i // batch_size + 1} with {len(batch_ids)} IDs")

            result = index.fetch(ids=batch_ids)
            logger.info(f"Received {len(result.vectors)} vectors in batch")

            # Process and extract required fields
            batch_data = [
                {
                    "id": vector_data.id,
                    "text": vector_data.metadata.get("text", ""),
                    "title": vector_data.metadata.get("source", "")
                }
                for vector_data in result.vectors.values()
            ]

            all_data.extend(batch_data)

        return {"data": all_data}

    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))