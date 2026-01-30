from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import bcrypt
from typing import Dict, List, Optional

app = FastAPI()

# --- In-Memory Storage ---
# Dictionary structure: { username: { "password": "hashed_pw", "chats": { chat_id: { ... } } } }
APP_DATA: Dict[str, Dict] = {}

# --- Data Models ---
class UserAuth(BaseModel):
    username: str
    password: str

class ChatData(BaseModel):
    username: str
    chat_id: str
    title: str
    messages: List[Dict]

# --- Endpoints ---

@app.get("/")
def health_check():
    return {"status": "running", "users": list(APP_DATA.keys())} # Debug info

@app.post("/register")
def register(user: UserAuth):
    if user.username in APP_DATA:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    APP_DATA[user.username] = {
        "password": hashed,
        "chats": {}
    }
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserAuth):
    if user.username not in APP_DATA:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    stored_hash = APP_DATA[user.username]["password"]
    if bcrypt.checkpw(user.password.encode('utf-8'), stored_hash.encode('utf-8')):
        return {"message": "Login successful", "username": user.username}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/history/{username}")
def get_history(username: str):
    return APP_DATA.get(username, {}).get("chats", {})

@app.post("/history/save")
def save_chat(chat: ChatData):
    if chat.username in APP_DATA:
        APP_DATA[chat.username]["chats"][chat.chat_id] = {
            "title": chat.title,
            "messages": chat.messages
        }
        return {"status": "saved"}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/history/{username}")
def clear_history(username: str):
    if username in APP_DATA:
        APP_DATA[username]["chats"] = {}
        return {"status": "cleared"}
    raise HTTPException(status_code=404, detail="User not found")
