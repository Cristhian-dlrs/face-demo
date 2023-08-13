from uuid import uuid4
from services import *
from models import *


class GuiController:
    def __init__(self, json_persister: JsonPersister, image_manager: ImageManager):
        self._json_persister = json_persister
        self._image_manager = image_manager

    def register_user(self, first_name: str, last_name: str, email: str, image: any) -> Result:
        try:
            new_user = User(first_name, last_name, email)
            user_image = ImageMetadata.from_user(new_user, image)
            self._image_manager.save_image(user_image)
            self._json_persister.save_user(new_user)
            return Result(True, f"{USER_REGISTRATION_SUCCESS_MESSAGE} {new_user.first_name} {new_user.last_name}")

        except Exception as e:
            print(e.with_traceback())
            return Result(True, USER_REGISTRATION_ERROR_MESSAGE)

    def confirm_attendance(self, image: any) -> Result:
        try:
            attendee_image = ImageMetadata.from_tmp_image(image)
            comparison = self._image_manager.compare_with_registered_images(
                attendee_image)

            if comparison.success:
                user = self._json_persister.load_user(comparison.payload)
                self._json_persister.save_attendance(user)
                return Result(True, f"{ATTENDANCE_CONFIRMED_SUCCESS_MESSAGE} {user.first_name} {user.last_name}")

            return Result(False, ATTENDANCE_CONFIRMATION_FAILED_MESSAGE)

        except Exception as e:
            print(e.with_traceback())
            return Result(False, ATTENDANCE_CONFIRMATION_ERROR_MESSAGE)
