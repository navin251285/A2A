from fastapi import FastAPI, Depends
import asyncio
import requests
from auth import verify_jwt
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

# 🔐 Generate token for callback
def generate_agent_token():
    payload = {
        "sub": "math-agent",
        "role": "executor",
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/invoke")
async def invoke(payload: dict, user=Depends(verify_jwt)):

    print(f"🔐 AUTH: {user}")

    # 🔒 Authorization
    if user["role"] != "orchestrator":
        return {"status": "error", "message": "Unauthorized"}

    tool = payload.get("tool")
    args = payload.get("args", {})
    callback_url = payload.get("callback_url")

    if tool == "add":
        result_value = args["a"] + args["b"]

    elif tool == "multiply":
        result_value = args["a"] * args["b"]

    else:
        return {"status": "error", "message": "Invalid tool"}

    await asyncio.sleep(3)

    result = {
        "status": "success",
        "tool": tool,
        "result": result_value
    }

    # 🔁 Callback with JWT
    requests.post(
        callback_url,
        json=result,
        headers={"Authorization": f"Bearer {generate_agent_token()}"}
    )

    return {"status": "accepted"}