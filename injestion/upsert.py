# import os
import json
import openai
# from dotenv import load_dotenv
from pinecone import Pinecone
from config.config import OPENAI_KEY, PINECONE_API_KEY

# OPENAI_KEY = os.getenv('OPENAI_API_KEY')
# PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
# load_dotenv()

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("wissen")


# Load your JSON data
with open("data/Ecommerce_FAQ_Chatbot_dataset.json", "r") as f:
    mydata = json.load(f)

# Prepare the texts for embedding (combine question + answer)
faq_data = []
for i, item in enumerate(mydata["questions"]):
    text = f"Q: {item['question']}\nA: {item['answer']}"
    faq_data.append({
        "id": f"faq{i+1}",
        "text": text,
        "metadata": {
            "datatype": "faq",
            "data": text
        }
    })

# Embed function
def embed(docs: list[str]) -> list[list[float]]:
    res = openai.embeddings.create(
        input=docs,
        model="text-embedding-3-large"
    )
    return [r.embedding for r in res.data]

# Generate embeddings
texts = [item["text"] for item in faq_data]
embeddings = embed(texts)

# Prepare vector list
vectors = []
for item, embedding in zip(faq_data, embeddings):
    vectors.append({
        "id": item["id"],
        "values": embedding,
        "metadata": item["metadata"]
    })

# Upsert into Pinecone
index.upsert(vectors=vectors)