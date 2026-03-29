from fastapi import FastAPI, Header, HTTPException
import requests
from jose import jwt, JWTError

app = FastAPI()

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

TASKS = {}

# 🔐 Verify JWT (callback)
def verify_jwt(authorization: str):
    try:
        scheme, token = authorization.split()

        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401)

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        raise HTTPException(status_code=401)


# 🔹 Get controller token from auth service
def get_controller_token():
    res = requests.post(
        "http://localhost:7000/token",
        params={"agent_name": "controller"}
    )
    return res.json()["access_token"]


@app.post("/execute")
def execute(query: str):

    print(f"\n🔍 QUERY: {query}")

    if "add" in query:
        agent_url = "http://localhost:8000/invoke"
        payload = {
            "tool": "add",
            "args": {"a": 10, "b": 20},
            "callback_url": "http://localhost:9000/callback"
        }

    elif "interest" in query:
        agent_url = "http://localhost:8001/invoke"
        payload = {
            "args": {"principal": 1000, "rate": 5, "time": 2},
            "callback_url": "http://localhost:9000/callback"
        }

    else:
        return {"error": "Unsupported query"}

    token = get_controller_token()

    res = requests.post(
        agent_url,
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    return {"status": "submitted", "agent_response": res.text}


@app.post("/callback")
def callback(result: dict, authorization: str = Header(...)):

    user = verify_jwt(authorization)

    print(f"\n📥 CALLBACK FROM: {user['sub']}")

    if user["role"] != "executor":
        return {"status": "error"}

    TASKS["latest"] = result

    print(f"📦 RESULT: {result}")

    return {"status": "received"}


@app.get("/result")
def get_result():
    return TASKS.get("latest", {"status": "no result yet"})