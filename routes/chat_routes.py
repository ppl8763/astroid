from fastapi import APIRouter, Depends, HTTPException
from database.db import db
from middleware.auth import get_current_user
from pydantic import BaseModel
from datetime import datetime
from typing import List

router = APIRouter(prefix="/chat", tags=["chat"])

chat_collection = db["chat_messages"]

class ChatMessage(BaseModel):
    text: str

@router.post("/send")
async def send_message(msg: ChatMessage, current_user: dict = Depends(get_current_user)):
    new_msg = {
        "email": current_user["email"],
        "text": msg.text,
        "timestamp": datetime.now()
    }
    chat_collection.insert_one(new_msg)
    return {"message": "Message sent"}

@router.get("/messages")
async def get_messages():
    messages = list(chat_collection.find().sort("timestamp", -1).limit(50))
    for m in messages:
        m["_id"] = str(m["_id"])
    return {"messages": messages[::-1]}
