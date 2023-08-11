import os
import json
from services import *
from controller import *
from gui import *

# -----------------------------------------------------------------------------
# Config settings
# -----------------------------------------------------------------------------

IMAGES_DIRECTORY = "images"
USER_STORAGE_FILE = "storage_users.json"
ATTENDANCE_STORAGE_FILE = "storage_attendance.json"
TEMP_DIRECTORY = "tmp"


def main():

    # startup setup
    if not os.path.exists(IMAGES_DIRECTORY):
        os.makedirs(IMAGES_DIRECTORY)

    if not os.path.exists(TEMP_DIRECTORY):
        os.makedirs(TEMP_DIRECTORY)

    if not os.path.exists(ATTENDANCE_STORAGE_FILE):
        with open(ATTENDANCE_STORAGE_FILE, "w") as file:
            json.dump([], file, indent=4)

    if not os.path.exists(USER_STORAGE_FILE):
        with open(USER_STORAGE_FILE, "w") as file:
            json.dump([], file, indent=4)

    # Dependencies setup
    jsonPersister = JsonPersister(USER_STORAGE_FILE, ATTENDANCE_STORAGE_FILE)
    image_config = ImageManagerConfig()
    imagePersister = ImageManager(image_config)
    controller = GuiController(jsonPersister, imagePersister)
    app = root_window(controller)

    app.mainloop()


main()
