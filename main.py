import json
from typing import Dict
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from routers.buildings import building_router
from routers.rooms import room_router


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
app.include_router(room_router)
