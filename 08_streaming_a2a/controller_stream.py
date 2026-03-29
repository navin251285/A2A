from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import requests

app = FastAPI()

# 🔥 Agent registry (dynamic discovery)
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
# 🧠 PLANNING
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
# 🤝 NEGOTIATION
# =========================
def select_agent(tool, registry):
    for agent in registry:
        if tool in agent["tools"]:
            return agent
    return None


# =========================
# 📦 PAYLOAD BUILDER (FIXED)
# =========================
def build_payload(tool):
    if tool == "add":
        return {
            "tool": "add",
            "args": {"a": 10, "b": 20}
        }

    if tool == "multiply":
        return {
            "tool": "multiply",
            "args": {"a": 5, "b": 4}
        }

    if tool == "calculate_interest":
        # ✅ FIXED SCHEMA HERE
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
# 🔥 STREAMING A2A PIPELINE
# =========================
async def a2a_stream(user_input: str):

    # 🔍 DISCOVERY
    yield "🔍 Discovering agents...\n"
    registry = await discover()
    await asyncio.sleep(1)

    yield f"✅ Found {len(registry)} agents\n"

    # 🧠 PLAN
    yield "🧠 Planning...\n"
    await asyncio.sleep(1)

    tool = plan(user_input)

    if not tool:
        yield "❌ Could not understand query\n"
        return

    yield f"✅ Planned tool: {tool}\n"

    # 🤝 NEGOTIATE
    yield "🤝 Selecting agent...\n"
    await asyncio.sleep(1)

    agent = select_agent(tool, registry)

    if not agent:
        yield "❌ No agent found\n"
        return

    yield f"🏆 Selected: {agent['agent']}\n"

    # 📦 BUILD
    yield "📦 Building payload...\n"
    await asyncio.sleep(1)

    payload = build_payload(tool)

    yield f"📦 Payload ready: {payload}\n"

    # 🚀 EXECUTE
    yield "🚀 Calling agent...\n"

    try:
        # ⚠️ requests is blocking → run in thread
        response = await asyncio.to_thread(
            requests.post,
            agent["endpoint"],
            json=payload
        )

        yield "⏳ Processing...\n"
        await asyncio.sleep(1)

        result = response.json()

        yield f"✅ Final Result: {result}\n"

    except Exception as e:
        yield f"❌ Error: {str(e)}\n"


# =========================
# 🌐 STREAM ENDPOINT
# =========================
@app.get("/stream")
async def stream(user_input: str):
    return StreamingResponse(
        a2a_stream(user_input),
        media_type="text/plain"
    )