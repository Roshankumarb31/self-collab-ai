# import json
# import pyttsx3

# with open("bot_instructions.json", "r", encoding="utf-8") as f:
#     instructions = json.load(f)

# engine = pyttsx3.init()

# for bot, instruction in instructions.items():
#     print(f"{bot}: {instruction}")
#     engine.say(f"{bot} says: {instruction}")

# engine.runAndWait()

import json
import pyttsx3

import json
import pyttsx3
import time

with open("ace_vs_akainu_2.json", "r", encoding="utf-8") as f:
    conversation = json.load(f)

engine = pyttsx3.init()
engine.setProperty('rate', 160)

for entry in conversation:
    sender = entry["sender"]
    message = entry["message"]
    line = f"{sender} says: {message}"
    
    print(line)
    engine.say(line)
    engine.runAndWait()
    
    time.sleep(0.3)