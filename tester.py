from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import sys
sys.path.append("../shared")

from chat_logic import get_chat_response

app = FastAPI()

builder_session = {}
tester_session = {}

@app.post("/chat")
async def tester_chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    incoming_builder = data.get("builder_session", {})
    incoming_tester = data.get("tester_session", {})

    builder_session.update(incoming_builder)
    tester_session.update(incoming_tester)

    tester_reply = get_chat_response(user_input, tester_session)
    print(f"[TESTER 🧪]: {tester_reply}")

    return JSONResponse({
        "response": tester_reply,
        "builder_session": builder_session,
        "tester_session": tester_session
    })
