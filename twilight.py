
import os
from pyrogram import Client

API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
TOKEN = os.getenv("TOKEN", "")

RiZoeL = Client(
    "RiZoeL-Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    plugins=dict(root="plugs")
    )

if __name__ == "__main__":
   print("bot started")
   RiZoeL.run()
