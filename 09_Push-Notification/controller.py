from fastapi import FastAPI, BackgroundTasks
from typing import Dict
import uuid
import requests
import re

app = FastAPI()

# In-memory task store
TASKS: Dict[str, dict] = {}

# Agent endpoints
AGENTS = {
    "math": "http://localhost:8001/invoke",
    "finance": "http://localhost:8002/invoke"
}

# -------------------------------
# 🔍 ROUTER
# -------------------------------
def route(query: str):
    if "add" in query:
        return "math"
    if "interest" in query:
        return "finance"
    return None

# -------------------------------
# 🧠 PAYLOAD BUILDER
# -------------------------------
def build_payload(query: str):
    nums = list(map(float, re.findall(r'\d+', query)))

    if "add" in query:
        return {"tool": "add", "args": {"a": nums[0], "b": nums[1]}}

    if "interest" in query:
        return {
            "tool": "calculate_interest",
            "args": {
                "principal": nums[0],
                "rate": nums[1],
                "time": nums[2]
            }
        }

    return {}

# -------------------------------
# 🚀 EXECUTE TASK (ASYNC FIRE)
# -------------------------------
def execute_task(task_id: str, agent: str, payload: dict):
    try:
        # 🔥 Add callback URL
        payload["callback_url"] = f"http://localhost:9000/callback/{task_id}"

        # 🔥 Fire-and-forget (NO WAIT)
        requests.post(AGENTS[agent], json=payload)

        TASKS[task_id]["status"] = "in_progress"

    except Exception as e:
        TASKS[task_id]["status"] = "failed"
        TASKS[task_id]["result"] = str(e)

# -------------------------------
# 📩 EXECUTE API
# -------------------------------
@app.post("/execute")
def execute(query: str, background_tasks: BackgroundTasks):

    agent = route(query)

    if not agent:
        return {"error": "No suitable agent found"}

    payload = build_payload(query)

    task_id = str(uuid.uuid4())

    TASKS[task_id] = {
        "status": "submitted",
        "query": query,
        "agent": agent
    }

    background_tasks.add_task(execute_task, task_id, agent, payload)

    return {
        "task_id": task_id,
        "status": "submitted"
    }

# -------------------------------
# 📢 CALLBACK (🔥 CORE OF PUSH)
# -------------------------------
@app.post("/callback/{task_id}")
def callback(task_id: str, result: dict):

    if task_id not in TASKS:
        return {"error": "Invalid task_id"}

    TASKS[task_id]["status"] = "completed"
    TASKS[task_id]["result"] = result

    print(f"\n📢 PUSH RECEIVED → {task_id}")
    print(f"✅ RESULT: {result}")

    return {"status": "received"}

# -------------------------------
# 📊 RESULT API (optional fallback)
# -------------------------------
@app.get("/result/{task_id}")
def get_result(task_id: str):
    return TASKS.get(task_id, {"error": "Invalid task_id"})from fastapi import FastAPI, BackgroundTasks
from typing import Dict
import uuid
import requests
import re

app = FastAPI()

# In-memory task store
TASKS: Dict[str, dict] = {}

# Agent endpoints
AGENTS = {
    "math": "http://localhost:8001/invoke",
    "finance": "http://localhost:8002/invoke"
}

# -------------------------------
# 🔍 ROUTER
# -------------------------------
def route(query: str):
    if "add" in query:
        return "math"
    if "interest" in query:
        return "finance"
    return None

# -------------------------------
# 🧠 PAYLOAD BUILDER
# -------------------------------
def build_payload(query: str):
    nums = list(map(float, re.findall(r'\d+', query)))

    if "add" in query:
        return {"tool": "add", "args": {"a": nums[0], "b": nums[1]}}

    if "interest" in query:
        return {
            "tool": "calculate_interest",
            "args": {
                "principal": nums[0],
                "rate": nums[1],
                "time": nums[2]
            }
        }

    return {}

# -------------------------------
# 🚀 EXECUTE TASK (ASYNC FIRE)
# -------------------------------
def execute_task(task_id: str, agent: str, payload: dict):
    try:
        # 🔥 Add callback URL
        payload["callback_url"] = f"http://localhost:9000/callback/{task_id}"

        # 🔥 Fire-and-forget (NO WAIT)
        requests.post(AGENTS[agent], json=payload)

        TASKS[task_id]["status"] = "in_progress"

    except Exception as e:
        TASKS[task_id]["status"] = "failed"
        TASKS[task_id]["result"] = str(e)

# -------------------------------
# 📩 EXECUTE API
# -------------------------------
@app.post("/execute")
def execute(query: str, background_tasks: BackgroundTasks):

    agent = route(query)

    if not agent:
        return {"error": "No suitable agent found"}

    payload = build_payload(query)

    task_id = str(uuid.uuid4())

    TASKS[task_id] = {
        "status": "submitted",
        "query": query,
        "agent": agent
    }

    background_tasks.add_task(execute_task, task_id, agent, payload)

    return {
        "task_id": task_id,
        "status": "submitted"
    }

# -------------------------------
# 📢 CALLBACK (🔥 CORE OF PUSH)
# -------------------------------
@app.post("/callback/{task_id}")
def callback(task_id: str, result: dict):

    if task_id not in TASKS:
        return {"error": "Invalid task_id"}

    TASKS[task_id]["status"] = "completed"
    TASKS[task_id]["result"] = result

    print(f"\n📢 PUSH RECEIVED → {task_id}")
    print(f"✅ RESULT: {result}")

    return {"status": "received"}

# -------------------------------
# 📊 RESULT API (optional fallback)
# -------------------------------
@app.get("/result/{task_id}")
def get_result(task_id: str):
    return TASKS.get(task_id, {"error": "Invalid task_id"})