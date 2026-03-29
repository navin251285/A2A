from fastapi import Header, HTTPException

VALID_API_KEYS = {
    "controller-key": "controller",
    "math-key": "math-agent",
    "finance-key": "finance-agent"
}

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in VALID_API_KEYS:
        print("❌ AUTH FAILED: Invalid API Key")
        raise HTTPException(status_code=401, detail="Invalid API Key")

    caller = VALID_API_KEYS[x_api_key]
    print(f"✅ AUTH SUCCESS: {caller}")
    return caller