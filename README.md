# 🤖 Dual AI Bot Conversation Simulator

This project sets up a conversation between two AI agents with **contrasting personalities or belief systems**. Each bot responds based on a custom instruction set loaded from a JSON file. The conversation is saved step-by-step, and can be read aloud using text-to-speech (TTS).

---

## 📦 Features

* 🔁 Two AI bots talking to each other
* 🧠 Each bot uses a unique instruction/personality
* 📁 Full conversation saved in `bot_conversation.json`
* 🔊 Read messages out loud using `pyttsx3` (offline TTS)
* 🔐 Supports separate API keys for each bot to avoid rate limits

---

## 🛠️ Setup

1. **Install dependencies:**

   ```bash
   pip install langchain langchain-google-genai pyttsx3 python-dotenv
   ```

2. **Set your API keys:**
   Create a `.env` file with:

   ```
   MODEL_API_KEY_1=your_google_api_key_1
   MODEL_API_KEY_2=your_google_api_key_2
   ```

3. **Add bot instructions:**
   Create a `bot_instructions.json`:

   ```json
   {
     "bot1": "You are a calm and logical philosopher who values reason and ethics.",
     "bot2": "You are a bold realist who believes in results over ideals."
   }
   ```

---

## 🚀 Running the Bots

Run the main simulation:

```bash
python dual_bot_simulator.py
```

Run TTS to hear the conversation:

```bash
python read_conversation_tts.py
```

---

## 📂 Files

| File                       | Purpose                                       |
| -------------------------- | --------------------------------------------- |
| `dual_bot_simulator.py`    | Main script to make both bots talk            |
| `bot_instructions.json`    | Defines personality/instructions for each bot |
| `bot_conversation.json`    | Stores the final conversation as JSON         |
| `read_conversation_tts.py` | Reads conversation aloud using TTS            |

---

## 📌 Notes

* Bots are powered by Google Generative AI (`gemini-2.0-flash`).
* Each bot can use a separate API key to avoid quota issues.
* Personalities can be modified easily via the JSON file.
