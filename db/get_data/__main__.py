import json
import time
from typing import List
from banner.schemas import BannerSection
from banner.client import BannerClient

if __name__ == "__main__":
    time_start = time.time()

    banner = BannerClient()

    print(f"Getting latest term", end=" ")
    term = banner.get_latest_term()
    print(f"\t[ok] found {term.code} - {term.description}")

    print(f"Setting term", end=" ")
    banner.set_term()
    print(f"\t\t[ok]")

    print("Getting data")
    offset = 0
    data: List[BannerSection] = list()
    while True:
        result = banner.get_data(offset)
        if result is None:
            break
        data = data + result
        offset += 1

    with open("test_json.json", "+w") as file:
        json_data = json.dumps([i.to_dict() for i in data], indent="  ")
        file.write(json_data)

    time_end = time.time()
    print(f"[DONE]\ntook {(time_end - time_start) * 1000}ms")
