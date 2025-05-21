import os
import json
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage

load_dotenv()

INITIAL_INSTRUCTION = """
    You are an AI that just replies to the queries and prompts given to you
"""
def initialize_llm():
    API_KEY = os.getenv("MODEL_API_KEY")
    if not API_KEY:
        raise ValueError("API key is missing.")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=API_KEY)
    return llm

def initialize_entity_memory(llm, memory_data):
    messages = []
    
    if not memory_data:
        messages.append(HumanMessage(content=INITIAL_INSTRUCTION))
    
    for msg in memory_data:
        if msg["type"] == "human":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["type"] == "ai":
            messages.append(AIMessage(content=msg["content"]))
    
    entity_memory = ConversationEntityMemory(llm=llm, k=5, input_key="input")
    entity_memory.chat_memory.messages = messages
    
    return entity_memory

def get_conversation_response(entity_memory, user_input):
    conversation = ConversationChain(
        llm=entity_memory.llm,
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=entity_memory
    )

    return conversation.run(input=user_input)


def get_chat_response(user_input, session):
    llm = initialize_llm()
    memory_data = session.get("entity_memory", [])
    print("session intialized")
    
    entity_memory = initialize_entity_memory(llm, memory_data)
    print("memory intialized")
    
    response = get_conversation_response(entity_memory, user_input)
    print("got response")
    
    session["entity_memory"] = [
        {"type": "human", "content": msg.content} if isinstance(msg, HumanMessage) 
        else {"type": "ai", "content": msg.content} for msg in entity_memory.chat_memory.messages
    ]

    return response
