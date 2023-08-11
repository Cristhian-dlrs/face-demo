from uuid import uuid4
import os
from services import *
from models import *


class GuiController:
    def __init__(self, json_persister: JsonPersister, image_manager: ImageManager):
        self._json_persister = json_persister
        self._image_manager = image_manager

    def register_user(self, first_name: str, last_name: str, email: str) -> None:
        new_user = User(uuid4(), first_name, last_name, email)
        self._image_manager.register_image(new_user.id)
        self._json_persister.save_user(new_user)

    def confirm_attendance(self) -> Result:
        attendee_image = self._image_manager.capture_attendee_image()
        registered_user_images = self._image_manager.load_images()
        for registered_user_image in registered_user_images:
            comparison = self._image_manager.compare_images(
                registered_user_image, attendee_image)

            if comparison.success:
                user = self._json_persister.load_user(comparison.payload)
                self._json_persister.save_attendance(user)
                self._image_manager.delete_image(attendee_image)
                return Result(True, user)

        self._image_manager.delete_image(attendee_image)
        return Result(False, "")
