import os

class Config:
    API_ID = int(os.getnev("API_ID"))  # your telegram api_id
    API_HASH = os.getenv("API_HASH")  # your telegram api_hash
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OWNER_ID = os.getenv("OWNER")  # your telegram user id
