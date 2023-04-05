from fastapi import APIRouter

from routers.rooms.services import get_room_details


class RoomRouter:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            "/api/rooms/{room_id}", self.room_details, status_code=200
        )

    def room_details(self, room_id: int):
        return get_room_details(room_id)


room_router = RoomRouter().router
