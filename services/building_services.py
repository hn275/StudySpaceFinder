from typing import List
from fastapi import HTTPException
from lib.get_next_class import get_next_class
from models import Building, RoomSummary, BuildingSummary, Session

from services.db import DbServices


def get_building_names() -> List[Building]:
    with DbServices() as db:
        data = db.cursor.execute(
            """
            SELECT * FROM buildings ORDER BY name ASC;
            """
        ).fetchall()
        return [Building(id=k[0], name=k[1].replace("&amp;", "and")) for k in data]


def get_building_at_time(
    bldg_id: int, hour: int, minute: int, day: str
) -> BuildingSummary:
    current_time = hour * 3600 + minute * 60

    with DbServices() as db:
        # get building name
        building_result = db.cursor.execute(
            "SELECT name FROM buildings WHERE id=?", (bldg_id,)
        ).fetchone()
        if not building_result:
            raise HTTPException(404, "Building not found")

        building_name = building_result[0]

        # get all rooms
        rooms = db.cursor.execute(
            """
                SELECT 
                    rooms.id,
                    rooms.room 
                FROM rooms 
                    JOIN buildings 
                        ON rooms.building_id=buildings.id 
                WHERE buildings.id=?
                ORDER BY rooms.room ASC;
                """,
            (bldg_id,),
        ).fetchall()

        if rooms is None:
            raise HTTPException(404, "Building not found.")

        # get all classes
        out = list()
        for room in rooms:
            (room_id, room_name) = room
            query = db.cursor.execute(
                f"""
                    SELECT
                        sections.time_start_str,
                        rooms.id,
                        rooms.room,
                        subjects.subject,
                        sections.time_start_int,
                        sections.time_end_int
                    FROM sections 
                        JOIN rooms 
                            ON sections.room_id=rooms.id
                        JOIN subjects
                            ON sections.subject_id=subjects.id
                    WHERE sections.room_id=? 
                        AND {day}=true
                    ORDER BY time_start_int ASC
                    """,
                (room_id,),
            )

            result = query.fetchall()
            if result is None or len(result) == 0:
                out.append(
                    RoomSummary(
                        room_id=room_id,
                        room=room_name,
                        next_class=None,
                        subject=None,
                    )
                )
                continue

            payload = [
                Session(
                    time_start_str=time_start_str,
                    room_id=room_id,
                    room=room,
                    subject=subject,
                    time_start_int=time_start_int,
                    time_end_int=time_end_int,
                )
                for (
                    time_start_str,
                    room_id,
                    room,
                    subject,
                    time_start_int,
                    time_end_int,
                ) in result
            ]

            next_class = get_next_class(payload, current_time)
            if next_class:
                out.append(next_class)

        return BuildingSummary(building=building_name.replace("&amp;", "&"), data=out)
