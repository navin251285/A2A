from fastapi import FastAPI
import asyncio

app = FastAPI()

# -------------------------------
# MCP: Tool Discovery
# -------------------------------
@app.get("/tools")
def get_tools():
    return {
        "tools": [
            {
                "name": "calculate_interest",
                "description": "Calculate simple interest",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "principal": {"type": "number"},
                        "rate": {"type": "number"},
                        "time": {"type": "number"}
                    },
                    "required": ["principal", "rate", "time"]
                }
            }
        ]
    }

# -------------------------------
# A2A: Agent Info (FIXED)
# -------------------------------
@app.get("/agent-info")
def agent_info():
    return {
        "name": "finance-agent",
        "description": "Handles financial calculations like simple interest",
        "endpoint": "http://localhost:8001/invoke"
    }

# -------------------------------
# Invocation (MCP Execution)
# -------------------------------
@app.post("/invoke")
async def invoke(payload: dict):
    import requests

    try:
        args = payload.get("args", {})
        callback_url = payload.get("callback_url")

        p = args["principal"]
        r = args["rate"]
        t = args["time"]

        si = (p * r * t) / 100

        await asyncio.sleep(20)

        result = {
            "status": "success",
            "result": si
        }

        # 🔥 PUSH result back to controller
        if callback_url:
            requests.post(callback_url, json=result)

        return {"status": "accepted"}  # immediate response

    except Exception as e:
        return {"status": "error", "message": str(e)}
