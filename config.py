import os
from dotenv import load_dotenv

load_dotenv()

class Config:
 
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not HUGGINGFACE_TOKEN:
        raise ValueError("HUGGINGFACEHUB_API_TOKEN not set in environment or .env file")

 
    MODEL_ID = os.getenv("MODEL_ID", "mistralai/Mistral-7B-Instruct-v0.2")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 512))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))


    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./memory")
    K_RETRIEVAL = int(os.getenv("K_RETRIEVAL", 3))


    AGENT_MAX_ITERATIONS = int(os.getenv("AGENT_MAX_ITERATIONS", 5))
    AGENT_VERBOSE = os.getenv("AGENT_VERBOSE", "false").lower() == "true"

 
    AGENT_WORKSPACE = os.getenv("AGENT_WORKSPACE", "./workspace")


    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")