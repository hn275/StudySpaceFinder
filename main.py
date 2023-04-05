import json
from typing import List, Dict
from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware
from lib.validate_time import validate_time
from models import Building, BuildingSummary, RoomDetail
import services


DAY_MAP: Dict[int, str] = {
    0: "sunday",
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
}


app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])


@app.get("/", status_code=200)
def index():
    disclaimer: str = ""
    with open("./contents/disclaimer.txt") as f:
        disclaimer = f.read().strip()

    project: Dict[str, str] = dict()
    with open("./contents/project.json") as f:
        project = json.loads(f.read())

    return {"project": project, "disclaimer": disclaimer}


@app.get(
    "/api/buildings/all",
    status_code=200,
    response_model=List[Building],
)
def serve_building_names():
    return services.get_building_names()


# ie: /api/building/1?hour=13&minute=30&day=1
@app.get(
    "/api/buildings/{bldg_id}",
    status_code=200,
    response_model=BuildingSummary,
)
def serve_building_details(bldg_id: int, hour: int, minute: int, day: int):
    if not validate_time(hour, minute, day):
        raise HTTPException(status_code=400, detail="Invalid query time query")

    weekday = DAY_MAP.get(day)
    if not weekday:
        raise HTTPException(status_code=400, detail="Invalid day query")

    return services.get_building_at_time(bldg_id, hour, minute, weekday)


# ie: /api/room/20?day=1
@app.get(
    "/api/rooms/{room_id}",
    status_code=200,
    response_model=RoomDetail,
)
def serve_room_details(room_id: int):
    return services.get_room_details(room_id)


@app.get("/api/rooms")
def get_all_rooms(building_id: int):
    return services.get_all_rooms(building_id)
