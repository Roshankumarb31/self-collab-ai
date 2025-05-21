import os
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

load_dotenv()

INITIAL_INSTRUCTION = "You are an AI that just replies to the queries and prompts given to you"

def initialize_llm(api_key):
    if not api_key:
        raise ValueError("API key is missing.")
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        google_api_key=api_key
    )


def create_bot(api_key, initial_instruction):
    llm = initialize_llm(api_key)
    memory = ConversationEntityMemory(llm=llm, k=5, input_key="input")
    memory.chat_memory.messages = [HumanMessage(content=initial_instruction)]
    chain = ConversationChain(llm=llm, prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE, memory=memory)
    return chain



def get_response(bot, user_input):
    return bot.run(input=user_input)
