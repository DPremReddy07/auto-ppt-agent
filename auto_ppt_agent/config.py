import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("❌ Set GROQ_API_KEY in your .env file!")

    MODEL_ID    = os.getenv("MODEL_ID", "llama-3.1-70b-versatile")
    MAX_TOKENS  = int(os.getenv("MAX_TOKENS", 2048))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))

    AGENT_MAX_ITERATIONS = int(os.getenv("AGENT_MAX_ITERATIONS", 25))
    AGENT_VERBOSE        = os.getenv("AGENT_VERBOSE", "true").lower() == "true"
    OUTPUT_DIR           = os.getenv("OUTPUT_DIR", "./output")