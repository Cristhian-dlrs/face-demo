import uuid
import os
from services import *
from models import *


class Controller:
    def __init__(self, json_persister, image_persister):
        self.jsonPersister = json_persister
        self.imagePersister = image_persister

    def register_user(self, first_name: str, last_name: str, email: str) -> None:
        new_user = User(str(uuid.uuid4()), first_name, last_name, email)
        user_capture = self.imagePersister.capture_image(CameraOptions())
        user_capture.id = new_user.id
        user_capture.path = os.path.join("images", new_user.id) + ".jpg"
        self.imagePersister.save_image(user_capture)
        self.jsonPersister.save(new_user)

    def confirm_attendance(self) -> bool:
        image_capture = self.imagePersister.capture_image(CameraOptions())
        self.imagePersister.save_image(image_capture)

        registered_users = self.imagePersister.load_images()
        for image in registered_users:
            comparison_result = self.imagePersister.compare_images(
                image, image_capture)

            if comparison_result[0]:
                image_capture.id = comparison_result[1]
                image_capture.path = os.path.join(
                    "images", comparison_result[1]+"jpg")
                user = self.jsonPersister.load_user(comparison_result[1])
                self.jsonPersister.save_attendance(user)
                return [True, user.first_name]

        self.imagePersister.delete_image(image_capture)
        return [False, ""]
