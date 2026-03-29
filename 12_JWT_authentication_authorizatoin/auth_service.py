from fastapi import FastAPI, HTTPException
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

USERS = {
    "controller": {"role": "orchestrator"},
    "math-agent": {"role": "executor"},
    "finance-agent": {"role": "executor"}
}

@app.post("/token")
def generate_token(agent_name: str):
    if agent_name not in USERS:
        raise HTTPException(status_code=404, detail="Invalid agent")

    payload = {
        "sub": agent_name,
        "role": USERS[agent_name]["role"],
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}