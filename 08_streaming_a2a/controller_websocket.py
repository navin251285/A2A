from fastapi import FastAPI, WebSocket
import asyncio
import requests
import json

from fastapi import FastAPI, WebSocket
import asyncio
import requests
import json




app = FastAPI()

AGENTS = [
    "http://localhost:8000",  # math-agent
    "http://localhost:8001"   # finance-agent
]


# =========================
# 🔍 DISCOVERY
# =========================
async def discover():
    registry = []

    for url in AGENTS:
        info = requests.get(f"{url}/agent-info").json()
        tools = requests.get(f"{url}/tools").json()

        registry.append({
            "agent": info["name"],
            "endpoint": info["endpoint"],
            "tools": [t["name"] for t in tools["tools"]]
        })

    return registry


# =========================
# 🧠 PLAN
# =========================
def plan(user_input):
    if "interest" in user_input:
        return "calculate_interest"
    if "add" in user_input:
        return "add"
    if "multiply" in user_input:
        return "multiply"
    return None


# =========================
# 🤝 NEGOTIATE
# =========================
def select_agent(tool, registry):
    for agent in registry:
        if tool in agent["tools"]:
            return agent
    return None


# =========================
# 📦 PAYLOAD
# =========================
def build_payload(tool):
    if tool == "add":
        return {"tool": "add", "args": {"a": 10, "b": 20}}

    if tool == "multiply":
        return {"tool": "multiply", "args": {"a": 5, "b": 4}}

    if tool == "calculate_interest":
        return {
            "tool": "calculate_interest",
            "args": {
                "principal": 1000,
                "rate": 5,
                "time": 2
            }
        }

    return None


# =========================
# 🔥 WEBSOCKET ENDPOINT
# =========================


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    # 🔥 Accept ALL connections (fixes 403)
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            user_input = message.get("user_input")

            await websocket.send_text(json.dumps({
                "step": "start",
                "message": f"Received: {user_input}"
            }))

            # simple test response first
            await asyncio.sleep(1)

            await websocket.send_text(json.dumps({
                "step": "result",
                "result": 123
            }))

    except Exception:
        await websocket.close()