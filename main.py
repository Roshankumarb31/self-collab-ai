import asyncio
import httpx

builder_url = "http://localhost:8000/chat"
tester_url = "http://localhost:8001/chat"

builder_session = {}
tester_session = {}

async def talk_to_bot(url, message):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={
            "message": message,
            "builder_session": builder_session,
            "tester_session": tester_session
        })
        return response.json()

async def chat_loop(start_message, rounds=5):
    message = start_message
    global builder_session, tester_session

    for i in range(rounds):
        print(f"\n🧱 Round {i+1} — Builder")
        builder_response = await talk_to_bot(builder_url, message)
        message = builder_response["response"]
        builder_session = builder_response["builder_session"]
        tester_session = builder_response["tester_session"]

        print(f"Builder: {message}")

        print(f"\n🧪 Round {i+1} — Tester")
        tester_response = await talk_to_bot(tester_url, message)
        message = tester_response["response"]
        builder_session = tester_response["builder_session"]
        tester_session = tester_response["tester_session"]

        print(f"Tester: {message}")

if __name__ == "__main__":
    asyncio.run(chat_loop("Here is the new product idea: A smart wearable for dogs."))
