import json
from typing import Dict
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from models import RoomDetail
from routers.buildings import building_router
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


app.include_router(building_router)


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
