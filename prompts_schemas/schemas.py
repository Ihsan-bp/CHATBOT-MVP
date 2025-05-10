# Intent_schema = " "
Intent_schema = {
    "title": "rag_bot_intent_schema",
    "description": "Identifies the user's intent, language, and sentiment based on their query to the RAG-based support chatbot.",
    "type": "object",
    "properties": {
        "intent": {
            "type": "string",
            "description": "The inferred user intent based on the query.",
            "enum": [
                "greeting",     
                "ask_faq",           
                "ask_overview",          
                "ask_customer_service",    
                "complaint_or_feedback", 
                "handover_to_agent",       
                "goodbye",                
                "other"                    
            ]
        },
        "language": {
            "type": "string",
            "description": "The language in which the user has expressed their query.",
            "enum": ["english", "hindi", "tamil", "telugu", "malayalam", "kannada", "bengali", "manglish", "hinglish", "other"]
        },
        "sentiment": {
            "type": "string",
            "description": "The detected emotional sentiment in the user query.",
            "enum": ["happy", "neutral", "angry", "sad", "confused"]
        }
    },
    "required": ["intent", "language", "sentiment"]
}