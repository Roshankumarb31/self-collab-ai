from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import sys
sys.path.append("../shared")

from chat_logic import get_chat_response

app = FastAPI()

builder_session = {}
tester_session = {}

@app.post("/chat")
async def builder_chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    incoming_builder = data.get("builder_session", {})
    incoming_tester = data.get("tester_session", {})

    builder_session.update(incoming_builder)
    tester_session.update(incoming_tester)

    builder_reply = get_chat_response(user_input, builder_session)
    print(f"[BUILDER 🧱]: {builder_reply}")

    return JSONResponse({
        "response": builder_reply,
        "builder_session": builder_session,
        "tester_session": tester_session
    })