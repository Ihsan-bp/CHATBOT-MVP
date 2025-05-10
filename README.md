# CHATBOT-MVP

# Multilingual Chatbot MVP

This project implements a multilingual chatbot using a RAG (Retrieval Augmented Generation) framework with Large Language Models. The chatbot handles multiple Indic languages, maintains conversation context, performs sentiment analysis, and provides knowledge-based responses.

## Overview

The chatbot MVP integrates several key technologies:
- **RAG Framework**: Utilizes retrieval-augmented generation to provide accurate and contextual responses
- **Vector Database**: Stores embeddings for efficient knowledge retrieval
- **LLM Integration**: Powers natural language understanding and generation
- **Multilingual Support**: Handles queries in various Indic languages
- **Sentiment Analysis**: Detects user emotions during conversations

## Features

- **Natural Language Understanding**: Identifies user intents and extracts entities
- **Contextual Conversations**: Maintains conversation state across sessions
- **Knowledge-Based Responses**: Retrieves relevant information from vector databases
- **Sentiment Analysis**: Detects if users are angry, neutral, or happy
- **Agent Handoff**: Politely transfers angry customers to human agents
- **Admin Interface**: Allows administrators to manage knowledge base and system settings

## Project Structure

```
CHATBOT MVP/
│   .env                    # Environment variables and API keys
│   .gitignore              # Git ignore file
│   admin.py                # Admin interface for knowledge management
│   app.py                  # Main chatbot application
│   readme.md               # This documentation file
│   requirement.txt         # Python dependencies
│   test.ipynb              # Testing notebook
│
├───config                  # Configuration settings
│       config.py
│
├───data                    # Knowledge base datasets
│       Ecommerce_FAQ_Chatbot_dataset.json
│       state_of_the_union.txt
│
├───helpers                 # Helper functions
│       logger.py
│
├───injestion               # Data ingestion components
│   │   upsert.py
│   │   upsert_langchain.py
│   │
│   └───index               # Vector database indexing
│           add_embd.py
│           edit_embd.py
│           get_embd.py
│
├───models                  # Model definitions
│       graph.py
│       intent.py
│
└───prompts_schemas         # LLM prompts and schemas
        prompts.py
        schemas.py
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- pip package manager
- Virtual environment (recommended)

### Installation

1. cd CHATBOT\ MVP/
   ```

2. Create and activate a virtual environment (optional)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirement.txt
   ```

4. Set up environment variables
   - Create a `.env` file based on the provided template
   - Add necessary API keys for LLM services and vector database connections

### Running the Application

1. Start the chatbot interface
   ```bash
   python app.py
   ```

2. Launch the admin interface
   ```bash
   python admin.py
   ```

## User Interfaces

### Chatbot Interface
The main chatbot interface allows users to:
- Interact with the chatbot in multiple languages
- Get answers from knowledge base related queries(knowledge base - data\Ecommerce_FAQ_Chatbot_dataset.json)
- Experience continuous conversation with context preservation

### Admin Interface
The admin panel provides functionality to:
- Upload and index new knowledge documents
- View and manage embedded data

## Technologies Used
- **LangChain**: Framework for LLM application development
- **Vector Database**: For knowledge storage and retrieval
- **Gradio**: For web interface development
- **Natural Language Processing**: For intent recognition and entity extraction
- **Sentiment Analysis**: For detecting user emotions

## Testing

The system includes tests for:
1. Intent recognition across multiple languages
2. Context maintenance throughout conversations
3. Knowledge retrieval accuracy
4. Multilingual response generation
5. Sentiment analysis and agent handoff

## Future Enhancements

- Enhanced retrieval techniques with metadata filters
- Voice interface integration
- Expanded language support
- Enhanced personalization features
- Integration with e-commerce platforms for order tracking
- Advanced analytics dashboard
