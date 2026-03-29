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
    try:
        args = payload.get("args", {})

        p = args["principal"]
        r = args["rate"]
        t = args["time"]

        si = (p * r * t) / 100
        await asyncio.sleep(20)

        return {
            "status": "success",
            "result": si
        }

    except KeyError as e:
        return {
            "status": "error",
            "message": f"Missing parameter: {str(e)}"
        }
