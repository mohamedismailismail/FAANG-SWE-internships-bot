import os    # make the code speak with the Operating system
from dotenv import load_dotenv    # Read any file named .env

load_dotenv()    # Load environment variables from .env

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:    # Fail fast principle
    raise ValueError("Error: BOT_TOKEN or CHAT_ID is missing from .env file!")