from fastapi import APIRouter, Request, HTTPException
import httpx
import asyncio
import json
from datetime import datetime
from sse_starlette.sse import EventSourceResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

NASA_API_KEY = os.getenv("NASA_API_KEY")

def calculate_risk_score(neo):
    try:
        diameter = neo['estimated_diameter']['kilometers']['estimated_diameter_max']
        velocity = float(neo['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'])
        miss_distance = float(neo['close_approach_data'][0]['miss_distance']['kilometers'])
        score = (diameter * 25) + (velocity / 12000) - (miss_distance / 10000000)
        if neo.get('is_potentially_hazardous_asteroid'):
            score += 15
        return round(max(10, min(score, 99)), 1)
    except:
        return 10.0

@router.get("/asteroids")
async def stream_asteroids(request: Request):
    async def event_generator():
        print("🛰️  RADAR ONLINE: Satellite link established.")
        
        # Initial ping to clear any proxy buffers (Ngrok/Cloudflare)
        yield {"event": "info", "data": "SIGNAL_STABLE"}

        async with httpx.AsyncClient() as client:
            while True:
                # CRITICAL: Check if client disconnected to prevent ASGI errors
                if await request.is_disconnected():
                    print("📡 SIGNAL LOST: Client disconnected.")
                    break

                today = datetime.now().strftime('%Y-%m-%d')
                url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&api_key={NASA_API_KEY}"
                
                try:
                    print(f"🔭 SCANNING: Fetching NASA Sector {today}...")
                    response = await client.get(url, timeout=15.0)
                    
                    if response.status_code == 200:
                        raw_data = response.json()
                        flat_list = []
                        
                        for date in raw_data.get('near_earth_objects', {}):
                            for neo in raw_data['near_earth_objects'][date]:
                                risk = calculate_risk_score(neo)
                                flat_list.append({
                                    "neo_id": neo['id'],
                                    "name": neo['name'].replace("(", "").replace(")", ""),
                                    "risk_score": risk,
                                    "is_hazardous": neo['is_potentially_hazardous_asteroid'],
                                    "miss_distance": round(float(neo['close_approach_data'][0]['miss_distance']['kilometers'])),
                                    "velocity": round(float(neo['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'])),
                                    "diameter": round(neo['estimated_diameter']['meters']['estimated_diameter_max'], 2),
                                    "last_observed": today
                                })
                        
                        print(f"✅ DATA SECURED: {len(flat_list)} objects mapped.")
                        yield {
                            "event": "update",
                            "data": json.dumps(flat_list)
                        }
                    else:
                        print(f"❌ NASA REJECTED: Status {response.status_code}")
                
                except Exception as e:
                    print(f"⚠️  SUBSYSTEM ERROR: {str(e)}")
                    yield {"event": "error", "data": "RECALIBRATING_SENSORS"}

                # Wait 60 seconds. Using a loop with shorter sleeps 
                # makes the app more responsive to shutdowns.
                for _ in range(60):
                    if await request.is_disconnected():
                        return
                    await asyncio.sleep(1)

    return EventSourceResponse(event_generator())

@router.get("/asteroids/{neo_id}")
async def get_asteroid_details(neo_id: str):
    url = f"https://api.nasa.gov/neo/rest/v1/neo/{neo_id}?api_key={NASA_API_KEY}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                neo = response.json()
                risk = calculate_risk_score(neo)
                return {
                    "neo_id": neo['id'],
                    "name": neo['name'].replace("(", "").replace(")", ""),
                    "risk_score": risk,
                    "is_hazardous": neo['is_potentially_hazardous_asteroid'],
                    "miss_distance": round(float(neo['close_approach_data'][0]['miss_distance']['kilometers'])),
                    "velocity": round(float(neo['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'])),
                    "diameter": round(neo['estimated_diameter']['meters']['estimated_diameter_max'], 2),
                    "orbital_data": neo.get("orbital_data", {})
                }
            else:
                raise HTTPException(status_code=response.status_code, detail="NASA API error")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
