from fastapi import APIRouter, Depends, HTTPException, status
from database.db import users_collection
from middleware.auth import get_current_user
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/asteroids", tags=["watchlist"])

class WatchlistRequest(BaseModel):
    neo_id: str
    name: str
    risk_score: float
    is_hazardous: bool
    miss_distance: int
    velocity: int
    diameter: float

@router.post("/watch")
async def watch_asteroid(asteroid: WatchlistRequest, current_user: dict = Depends(get_current_user)):
    user_email = current_user["email"]
    
    # Check if already watched
    existing = users_collection.find_one({
        "email": user_email,
        "watchlist.neo_id": asteroid.neo_id
    })
    
    if existing:
        return {"message": "Asteroid already in watchlist"}
    
    users_collection.update_one(
        {"email": user_email},
        {"$push": {"watchlist": asteroid.model_dump()}}
    )
    
    return {"message": "Asteroid added to watchlist"}

@router.get("/watched")
async def get_watched_asteroids(current_user: dict = Depends(get_current_user)):
    watchlist = current_user.get("watchlist", [])
    # Ensure all items are serializable (though they should be already)
    return {"watchlist": list(watchlist)}

@router.delete("/watch/{neo_id}")
async def unwatch_asteroid(neo_id: str, current_user: dict = Depends(get_current_user)):
    users_collection.update_one(
        {"email": current_user["email"]},
        {"$pull": {"watchlist": {"neo_id": neo_id}}}
    )
    return {"message": "Asteroid removed from watchlist"}
