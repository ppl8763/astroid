from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.userroute import router as user
from routes.astroidshow import router as asteroid
from routes.watchlist_routes import router as watchlist
from routes.chat_routes import router as chat

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Get allowed origins from environment or use default for development
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://astroid-backend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app.include_router(user)
app.include_router(asteroid)
app.include_router(watchlist)
app.include_router(chat)
