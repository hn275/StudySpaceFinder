from typing import List, Dict
from fastapi import APIRouter, HTTPException
from lib.validate_time import validate_time

from routers.buildings.services import get_all_buildings, get_building_schedules
from schemas.buildings import Building

DAY_MAP: Dict[int, str] = {
    0: "sunday",
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
}


class BuildingController:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            "/api/buildings/all",
            self.all,
            status_code=200,
            response_model=List[Building],
        )

        self.router.add_api_route(
            "/api/buildings/{bldg_id}",
            self.bldg_id,
            status_code=200,
            response_model=None,  # TODO: change this
        )

    def all(self):
        return get_all_buildings()

    def bldg_id(self, bldg_id: int, hour: int, minute: int, day: int):
        if not validate_time(hour, minute, day):
            raise HTTPException(status_code=400, detail="Invalid time query")

        return get_building_schedules(bldg_id, hour, minute, day)


building_router = BuildingController().router
