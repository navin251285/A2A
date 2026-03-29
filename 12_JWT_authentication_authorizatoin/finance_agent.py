from fastapi import FastAPI, Depends
import asyncio
import requests
from auth import verify_jwt
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

def generate_agent_token():
    payload = {
        "sub": "finance-agent",
        "role": "executor",
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/invoke")
async def invoke(payload: dict, user=Depends(verify_jwt)):

    if user["role"] != "orchestrator":
        return {"status": "error", "message": "Unauthorized"}

    args = payload.get("args", {})
    callback_url = payload.get("callback_url")

    p = args["principal"]
    r = args["rate"]
    t = args["time"]

    si = (p * r * t) / 100

    await asyncio.sleep(5)

    result = {"status": "success", "result": si}

    requests.post(
        callback_url,
        json=result,
        headers={"Authorization": f"Bearer {generate_agent_token()}"}
    )

    return {"status": "accepted"}