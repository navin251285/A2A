from fastapi import FastAPI
import asyncio
from fastapi import Depends
from auth import verify_api_key

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
async def invoke(payload: dict, caller=Depends(verify_api_key)):
    print(f"📥 CALLBACK RECEIVED from {caller}")
    if caller != "controller":
        return {"status": "error", "message": "Unauthorized"}
    print("✅ AUTHZ SUCCESS (callback)")
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

        TASKS["latest"] = result

        print(f"📦 FINAL RESULT: {result}")
    

        # 🔥 PUSH result back to controller
        if callback_url:
            requests.post(
    callback_url,
    json=result,
    headers={"x-api-key": "finance-key"}
)

        return {"status": "accepted"}  # immediate response

    except Exception as e:
        return {"status": "error", "message": str(e)}
