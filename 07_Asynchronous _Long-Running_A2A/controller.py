from fastapi import FastAPI
import threading
import uuid
import requests

app = FastAPI()

tasks = {}

# 🔥 Background worker
def run_task(task_id, endpoint, payload):
    try:
        response = requests.post(endpoint, json=payload).json()

        tasks[task_id] = {
            "status": "completed",
            "result": response
        }

    except Exception as e:
        tasks[task_id] = {
            "status": "failed",
            "error": str(e)
        }


# 🔥 Submit API
@app.post("/submit")
def submit(data: dict):
    task_id = str(uuid.uuid4())

    endpoint = data["endpoint"]
    payload = data["payload"]

    tasks[task_id] = {"status": "processing"}

    threading.Thread(
        target=run_task,
        args=(task_id, endpoint, payload)
    ).start()

    return {
        "task_id": task_id,
        "status": "submitted"
    }


# 🔥 Status API
@app.get("/status/{task_id}")
def status(task_id: str):
    return tasks.get(task_id, {"status": "not_found"})