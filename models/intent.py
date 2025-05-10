from langchain_openai import ChatOpenAI
from config.config import OPENAI_KEY, GOOGLE_GEMINI_API
from prompts_schemas.prompts import Intent_prompt
from prompts_schemas.schemas import Intent_schema
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatOpenAI(model="gpt-4o-mini", api_key =OPENAI_KEY)
llm_google = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=GOOGLE_GEMINI_API)


def identify_intent(user_query):
    prompt = f"""{Intent_prompt}

    User: {user_query}
    Intent:
    """
    order_llm = llm.with_structured_output(Intent_schema)
    intent = order_llm.invoke(prompt)
    return intent

def identify_intent_google(user_query):
    prompt = f"""{Intent_prompt}

    User: {user_query}
    Intent:
    """
    # Prompt the LLM to identify the intent
    order_llm = llm.with_structured_output(Intent_schema)
    intent = order_llm.invoke(prompt)
    return intent