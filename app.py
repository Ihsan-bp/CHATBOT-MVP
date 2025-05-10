# app.py
import os
import gradio as gr
from models.intent import identify_intent_google
from models.graph import final_response

def chatbot_pipeline(user_query):
    try:
        # Step 1: Get intent, language, sentiment
        result = identify_intent_google(user_query)
        intent = result.get('intent')
        language = result.get('language')
        sentiment = result.get('sentiment')
        
        # Optional logging or debugging
        print(f"[INFO] Intent: {intent}, Language: {language}, Sentiment: {sentiment}")

        # Step 2: Get RAG-based response
        response = final_response(user_query, language, sentiment, intent)
        return response
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Launch Gradio app
gr.Interface(
    fn=chatbot_pipeline,
    inputs=gr.Textbox(lines=2, placeholder="Ask me anything about Wissen..."),
    outputs=gr.Textbox(label="Wissen AI Response"),
    title="Wissen Multilingual Chatbot",
    description="An intelligent RAG-based assistant powered by Gemini and Pinecone."
).launch(share=True)