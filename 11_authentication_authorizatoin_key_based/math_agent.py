# math_agent.py

from fastapi import FastAPI
import asyncio
import requests
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
                "name": "add",
                "description": "Add two numbers",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"]
                }
            },
            {
                "name": "multiply",
                "description": "Multiply two numbers",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"]
                }
            }
        ]
    }

# -------------------------------
# A2A: Agent Info
# -------------------------------
@app.get("/agent-info")
def agent_info():
    return {
        "name": "math-agent",
        "description": "Handles basic math operations like addition and multiplication",
        "endpoint": "http://localhost:8000/invoke"
    }

# -------------------------------
# Invocation (Push-based A2A)
# -------------------------------
@app.post("/invoke")
async def invoke(payload: dict, caller=Depends(verify_api_key)):
    print(f"📥 REQUEST RECEIVED from {caller}")
    if caller != "controller":
        return {"status": "error", "message": "Unauthorized"}
    print("✅ AUTHZ SUCCESS: Controller allowed")
    try:
        tool = payload.get("tool")
        args = payload.get("args", {})
        callback_url = payload.get("callback_url")
        print(f"🧠 TOOL: {tool}, ARGS: {args}")

        # -----------------------
        # Execute Tool
        # -----------------------
        if tool == "add":
            result_value = args["a"] + args["b"]

        elif tool == "multiply":
            result_value = args["a"] * args["b"]

        else:
            raise ValueError("Unsupported tool")

        # Simulate async processing
        await asyncio.sleep(5)

        result = {
            "status": "success",
            "tool": tool,
            "result": result_value
        }

        # -----------------------
        # PUSH Result to Controller
        # -----------------------
        if callback_url:
            try:
                requests.post(
    callback_url,
    json=result,
    headers={"x-api-key": "finance-key"}
)
                print(f"📤 Callback sent to {callback_url}")
            except Exception as cb_error:
                print(f"❌ Callback failed: {cb_error}")

        # Immediate response (non-blocking)
        return {"status": "accepted"}

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
