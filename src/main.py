import os
import json
from config import *
from services import *
from controller import *
from gui import *


def main():

    # setup startup
    if not os.path.exists(IMAGES_DIRECTORY):
        os.makedirs(IMAGES_DIRECTORY)

    if not os.path.exists(TEMP_DIRECTORY):
        os.makedirs(TEMP_DIRECTORY)

    if not os.path.exists(ATTENDANCE_STORAGE):
        with open(ATTENDANCE_STORAGE, "w") as file:
            json.dump([], file, indent=JSON_IDENT)

    if not os.path.exists(USERS_STORAGE):
        with open(USERS_STORAGE, "w") as file:
            json.dump([], file, indent=JSON_IDENT)

    # setup dependencies
    jsonPersister = JsonPersister()
    imagePersister = ImageManager()
    controller = GuiController(jsonPersister, imagePersister)
    app = GUI(controller)

    app.run()


main()
