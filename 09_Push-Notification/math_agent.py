from fastapi import FastAPI
import asyncio
import requests

app = FastAPI()

@app.post("/invoke")
async def invoke(payload: dict):
    try:
        tool = payload.get("tool")
        args = payload.get("args", {})
        callback_url = payload.get("callback_url")

        if tool == "add":
            result_value = args["a"] + args["b"]

        elif tool == "multiply":
            result_value = args["a"] * args["b"]

        else:
            raise ValueError("Unsupported tool")

        # simulate async
        await asyncio.sleep(3)

        result = {
            "status": "success",
            "tool": tool,
            "result": result_value
        }

        # 🔥 PUSH BACK
        if callback_url:
            requests.post(callback_url, json=result)

        return {"status": "accepted"}

    except Exception as e:
        return {"status": "error", "message": str(e)}