from fastapi import FastAPI

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
            }
        ]
    }

# -------------------------------
# A2A: Agent Info (FIXED)
# -------------------------------
@app.get("/agent-info")
def agent_info():
    return {
        "name": "math-agent",
        "description": "Handles mathematical operations like addition",
        "endpoint": "http://localhost:8000/invoke"
    }

# -------------------------------
# Invocation (MCP Execution)
# -------------------------------
@app.post("/invoke")
def invoke(payload: dict):
    try:
        tool = payload.get("tool")
        args = payload.get("args", {})

        if tool == "add":
            a = args["a"]
            b = args["b"]

            return {
                "status": "success",
                "result": a + b
            }

        return {
            "status": "error",
            "message": "Unknown tool"
        }

    except KeyError as e:
        return {
            "status": "error",
            "message": f"Missing parameter: {str(e)}"
        }
