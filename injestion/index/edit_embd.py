from pinecone import Pinecone
from typing import Optional, Dict, Any
from fastapi import HTTPException
from config.config import PINECONE_API_KEY
from helpers.logger import setup_logging, get_logger

# Setup logger
setup_logging()
logger = get_logger(__name__)

def update_metadata_for_index(
    entry_id: str,
    new_text: str,
    new_title: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update metadata (text and optionally title) for a given entry in a Pinecone index.
    
    Args:
        pinecone_api_key (str): Pinecone API key.
        index_name (str): Name of the Pinecone index.
        entry_id (str): ID of the entry to update.
        new_text (str): Updated text value.
        new_title (Optional[str]): Updated title (optional).
    
    Returns:
        dict: Update status and message.
    """
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index("assessment")

        logger.info(f"Processing metadata update for ID: {entry_id} in index: {"assessment"}")

        # Query existing entry
        result = index.query(
            id=entry_id,
            top_k=1,
            include_metadata=True,
            include_values=True
        )

        existing_entries = result.get("matches", [])
        if not existing_entries:
            logger.error(f"Entry ID {entry_id} not found.")
            raise HTTPException(status_code=404, detail=f"Entry with ID {entry_id} not found.")

        existing = existing_entries[0]
        existing_metadata = existing.get("metadata", {})
        existing_embedding = existing.get("values", None)

        # Compare updates
        text_needs_update = existing_metadata.get("text") != new_text
        title_needs_update = new_title is not None and existing_metadata.get("title") != new_title

        if not text_needs_update and not title_needs_update:
            logger.info("No changes detected.")
            return {"message": f"Entry {entry_id} is already up to date."}

        # Prepare updated metadata
        updated_metadata = existing_metadata.copy()
        updated_metadata["text"] = new_text
        if new_title is not None:
            updated_metadata["title"] = new_title

        if existing_embedding is not None:
            index.upsert([(entry_id, existing_embedding, updated_metadata)])
            logger.info(f"Updated metadata for ID {entry_id}.")
            return {
                "status": "success",
                "message": f"Updated {'text and title' if new_title else 'text'} for entry {entry_id}"
            }
        else:
            logger.error("No embedding found to update.")
            raise HTTPException(status_code=500, detail="No embedding found to update.")

    except Exception as e:
        logger.error(f"Update error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))