from langchain_core.language_models import LLM
from langchain_core.prompts import PromptTemplate
import requests
from typing import List, Optional
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
import httpx
from langchain_openai import ChatOpenAI

load_dotenv(override=True)
config = os.environ
openai_api_key = os.getenv("OPENAI_API_KEY")




def get_llm_agent(model_name=config['MODEL_NAME'], temperature=0.1, top_p=1.0, max_tokens=16000,
                  is_chat_gpt=True):

    if is_chat_gpt:
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key, temperature=temperature,
                         max_tokens=max_tokens, top_p=top_p
                         )

    else:
        llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=temperature,
            model_kwargs={"top_p": top_p, "seed": 1337},
            # api_key=groq_api_key,
            http_client=httpx.Client(verify=False)

        )
    return llm
