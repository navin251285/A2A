from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import requests
import json

app = FastAPI()

AGENTS = [
    "http://localhost:8000",
    "http://localhost:8001"
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
def plan(user_input: str):
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
# 🔥 SSE FORMATTER
# =========================
def sse_event(data: dict):
    return f"data: {json.dumps(data)}\n\n"


# =========================
# 🔥 STREAM PIPELINE (SSE)
# =========================
async def a2a_sse(user_input: str):

    # 🔍 DISCOVERY
    yield sse_event({"step": "discovery", "message": "Discovering agents..."})
    registry = await discover()
    await asyncio.sleep(1)

    yield sse_event({"step": "discovery", "message": f"Found {len(registry)} agents"})

    # 🧠 PLAN
    yield sse_event({"step": "plan", "message": "Planning..."})
    await asyncio.sleep(1)

    tool = plan(user_input)

    if not tool:
        yield sse_event({"error": "Could not understand query"})
        return

    yield sse_event({"step": "plan", "tool": tool})

    # 🤝 NEGOTIATE
    yield sse_event({"step": "negotiation", "message": "Selecting agent..."})
    await asyncio.sleep(1)

    agent = select_agent(tool, registry)

    if not agent:
        yield sse_event({"error": "No agent found"})
        return

    yield sse_event({"step": "negotiation", "agent": agent["agent"]})

    # 📦 BUILD
    yield sse_event({"step": "payload", "message": "Building payload..."})
    await asyncio.sleep(1)

    payload = build_payload(tool)

    yield sse_event({"step": "payload", "payload": payload})

    # 🚀 EXECUTE
    yield sse_event({"step": "execution", "message": "Calling agent..."})

    try:
        response = await asyncio.to_thread(
            requests.post,
            agent["endpoint"],
            json=payload
        )

        yield sse_event({"step": "execution", "message": "Processing..."})

        await asyncio.sleep(1)

        result = response.json()

        yield sse_event({"step": "result", "result": result})

    except Exception as e:
        yield sse_event({"error": str(e)})


# =========================
# 🌐 SSE ENDPOINT
# =========================
@app.get("/stream")
async def stream(user_input: str):
    return StreamingResponse(
        a2a_sse(user_input),
        media_type="text/event-stream"
    )