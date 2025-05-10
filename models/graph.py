from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph, MessagesState
from typing import List, TypedDict
from langchain_core.documents import Document
from config.config import OPENAI_KEY, PINECONE_API_KEY, GOOGLE_GEMINI_API
from pinecone import Pinecone
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.messages import HumanMessage, SystemMessage

from helpers.logger import setup_logging, get_logger

pc = Pinecone(api_key=PINECONE_API_KEY)
setup_logging()
logger = get_logger(__name__)

index = pc.Index("assessment")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_KEY)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17", api_key=GOOGLE_GEMINI_API)

class State(MessagesState):
    context: List[Document]
    language: str
    sentiment: str
    intent: str

def retrieve(state: State):
    # Use last human message content as query
    if state["intent"] in ["greeting", "goodbye"]: #, "other"
        return {"context": "no content available"}
    last_human_msg = next(
        (m for m in reversed(state["messages"]) if m.type == "human"), None
    )
    logger.info(f"last_human_msg is {last_human_msg}")
    query = last_human_msg.content if last_human_msg else ""
    retrieved_docs = vector_store.similarity_search(query, k=4)
    logger.info(f"retrieved_docs areeeeeee {retrieved_docs}")
    return {"context": retrieved_docs}


def call_model(state: State):
    if isinstance(state["context"], str):
        docs_content = ""  
    else:
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])

    # Get language instruction
    language_instructions = {
        "english": "Respond in English.",
        "hindi": "Respond in Hindi.",
        "tamil": "Respond in Tamil.",
        "telugu": "Respond in Telugu.",
        "malayalam": "Respond in Malayalam.",
        "kannada": "Respond in Kannada.",
        "bengali": "Respond in Bengali.",
        "manglish": "Respond in Malayalam using English letters (Manglish).",
        "hinglish": "Respond in Hindi using English letters (Hinglish).",
        "other": "Respond in the same language as the user's input."
    }
    language_instruction = language_instructions.get(state["language"].lower(), language_instructions["other"])

    # Get sentiment instruction
    sentiment_tones = {
        "happy": "Use a cheerful, friendly, and energetic tone.",
        "neutral": "Use an informative and calm tone.",
        "angry": "Use a polite, empathetic, and calming tone to de-escalate.",
        "sad": "Use a compassionate and reassuring tone.",
        "confused": "Use a clear and patient tone with step-by-step help."
    }
    sentiment_instruction = sentiment_tones.get(state["sentiment"].lower(), "Keep the tone friendly and helpful.")

    system_prompt = (
        f"You are a smart AI assistant helping users with their queries based on the available knowledge base.\n"
        f"#Rules"
        f"{language_instruction} {sentiment_instruction}\n"
        
        f"### Instructions:"
        f"- Answer the user's question using only the provided context."
        f"- If context does not contain the answer, say: 'Sorry, I couldn't find a clear answer to that. Could you please ask from the context?"
        f"Use the following context to answer:\n{docs_content}")

    if state["intent"] in ["greeting", "goodbye"]: #, "other"
        system_prompt = (
        f"You are a helpful assistant.\n"
        f"{language_instruction} {sentiment_instruction}\n")

    system_message = SystemMessage(content=system_prompt)
    messages = [system_message] + state["messages"]
    logger.info(f"-------------------final prompt is : {messages}-----------------")
    response = llm.invoke(messages)
    return {"messages": [AIMessage(content=response.content)]}


workflow = StateGraph(state_schema=State)
workflow.add_node("retrieve", retrieve)
workflow.add_node("model", call_model)
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "model")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# def final_response(message: str):
def final_response(message: str, language: str, sentiment: str, intent: str):
    logger.info(f"Inside final_resp {message} with language={language} and sentiment={sentiment}")
    config = {"configurable": {"thread_id": "abc123"}}
    input_messages = [HumanMessage(message)]

    output = app.invoke(
        {
            "messages": input_messages,
            "language": language,
            "sentiment": sentiment,
            "intent": intent,
        },
        config,
    )
    logger.info(f"output of final response: {output}")
    return output["messages"][-1].content