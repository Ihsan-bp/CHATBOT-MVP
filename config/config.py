import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
GOOGLE_GEMINI_API = os.getenv('GOOGLE_GEMINI_API')