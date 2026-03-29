from fastapi import FastAPI
import asyncio
import requests

app = FastAPI()

@app.post("/invoke")
async def invoke(payload: dict):
    try:
        args = payload.get("args", {})
        callback_url = payload.get("callback_url")

        p = args["principal"]
        r = args["rate"]
        t = args["time"]

        # simulate async work
        await asyncio.sleep(5)

        si = (p * r * t) / 100

        result = {
            "status": "success",
            "result": si
        }

        # 🔥 PUSH BACK
        if callback_url:
            requests.post(callback_url, json=result)

        return {"status": "accepted"}  # immediate return

    except Exception as e:
        return {"status": "error", "message": str(e)}