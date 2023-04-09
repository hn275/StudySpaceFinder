from typing import List
from db.database import Database
from db.get_data.banner.schemas import BannerSection


class DB(Database):
    def __init__(self, fetched: List[BannerSection]):
        super().__init__()
        self.data = fetched

    def save_subjects(self):
        buf = list()
        for i in self.data:
            subject = i.subject
            desc = i.subject_description
            buf.append((subject, desc))

        sql = """
        INSERT INTO subjects(subject, description)
            VALUES(?,?)
            ON CONFLICT DO NOTHING
        """
        self.cursor.executemany(sql, buf)
        self.connection.commit()

    def save_buildings(self):
        buf = set()
        for i in self.data:
            for j in i.meetings_faculty:
                meeting_time = j.meeting_time
                bldg_desc = meeting_time.building_description
                if bldg_desc:
                    try:
                        buf.add(bldg_desc)
                    except KeyError:
                        continue

        sql = """
        INSERT INTO buildings(name) 
            VALUES(?)
            ON CONFLICT DO NOTHING;
        """
        self.cursor.executemany(sql, buf)
        self.connection.commit()

    def save_rooms(self):
        buf = set()
        for i in self.data:
            if len(i.meetings_faculty) == 0:
                continue

            for j in i.meetings_faculty:
                meeting_time = j.meeting_time
                room = meeting_time.room
                bldg_desc = meeting_time.building_description
                if not room or not bldg_desc:
                    continue

                q = "SELECT id FROM buildings WHERE name = ?;"
                bldg_id = self.cursor.execute(q, bldg_desc)
                try:
                    buf.add((room, bldg_id))
                except KeyError:
                    continue

        sql = """
        INSERT INTO rooms(room, building_id) VALUES(?, ?)
            ON CONFLICT DO NOTHING;
        """
        self.cursor.executemany(sql, buf)
        self.connection.commit()
