import os
import time
import json
from dotenv import load_dotenv
from bot import create_bot, get_response

load_dotenv()

API_KEY_1 = os.getenv("MODEL_API_KEY_1")
API_KEY_2 = os.getenv("MODEL_API_KEY_2")

# Load initial instructions from JSON
with open("bot_instructions.json", "r", encoding="utf-8") as f:
    instructions = json.load(f)

bot1 = create_bot(API_KEY_1, instructions["bot1"])
bot2 = create_bot(API_KEY_2, instructions["bot2"])

LOG_FILE = "ace_vs_akainu_3.json"
with open(LOG_FILE, "w", encoding="utf-8") as f:
    json.dump([], f)

def log_message(sender, message):
    with open(LOG_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data.append({"sender": sender, "message": message})
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.truncate()

message = "What do you think about Monkey D. Luffy's rise in the New World?"
print("Bot1:", message)
log_message("Bot1", message)

while True:
    response1 = get_response(bot1, message)
    print("Bot2:", response1)
    log_message("Bot2", response1)
    time.sleep(1)

    response2 = get_response(bot2, response1)
    print("Bot1:", response2)
    log_message("Bot1", response2)
    time.sleep(1)

    message = response2
    time.sleep(1)
