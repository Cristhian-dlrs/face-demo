import os
import json


def on_init() -> None:
    if not os.path.exists("images"):
        os.makedirs("images")

    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    if not os.path.exists("attendance_storage.json"):
        with open("attendance_storage.json", "w") as file:
            json.dump([], file, indent=4)


if __name__ == "__main__":
    on_init()
