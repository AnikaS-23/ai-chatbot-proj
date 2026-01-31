from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
# Trigger reload
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
import bcrypt

from database import engine, get_db, Base
from models import User, Chat

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models (Pydantic) ---
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
    return {"status": "running", "database": "sqlite"}

@app.post("/register")
def register(user_data: UserAuth, db: Session = Depends(get_db)):
    # Check existing
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Hash password
    hashed = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create user
    new_user = User(username=user_data.username, password_hash=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user_data: UserAuth, db: Session = Depends(get_db)):
    print(f"DEBUG: Login attempt for username='{user_data.username}'")
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user:
        print(f"DEBUG: User '{user_data.username}' NOT FOUND in database.")
        raise HTTPException(status_code=401, detail="Invalid credentials (User not found)")
    
    if bcrypt.checkpw(user_data.password.encode('utf-8'), user.password_hash.encode('utf-8')):
        print(f"DEBUG: Password match for '{user_data.username}'. Login successful.")
        return {"message": "Login successful", "username": user.username}
    
    print(f"DEBUG: Password Mismatch for '{user_data.username}'.")
    raise HTTPException(status_code=401, detail="Invalid credentials (Password mismatch)")

@app.get("/history/{username}")
def get_history(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
         # Return empty if user doesn't exist yet (or handle error)
         return {}
    
    # Convert DB objects to nested dict format for frontend: {uuid: {title: ..., messages: ...}}
    history = {}
    for chat in user.chats:
        history[chat.chat_uuid] = {
            "title": chat.title,
            "messages": chat.messages
        }
    return history

@app.post("/history/save")
def save_chat(chat_data: ChatData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == chat_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if chat exists
    chat = db.query(Chat).filter(Chat.chat_uuid == chat_data.chat_id).first()
    
    if chat:
        # Update existing
        chat.title = chat_data.title
        chat.messages = chat_data.messages
    else:
        # Create new
        chat = Chat(
            chat_uuid=chat_data.chat_id,
            user_id=user.id,
            title=chat_data.title,
            messages=chat_data.messages
        )
        db.add(chat)
    
    db.commit()
    return {"status": "saved"}

@app.delete("/history/{username}")
def clear_history(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        # Delete all chats for this user
        db.query(Chat).filter(Chat.user_id == user.id).delete()
        db.commit()
        return {"status": "cleared"}
    
    raise HTTPException(status_code=404, detail="User not found")
