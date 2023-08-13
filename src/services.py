import json
import os
import cv2
from deepface import DeepFace
from models import *
from config import *


import time


class ImageManager:

    def compare_with_registered_images(self, attendee_image: ImageMetadata) -> Result:
        self.save_image(attendee_image)
        registered_user_images = self.load_images()
        for registered_user_image in registered_user_images:
            comparison = self._compare_images(
                registered_user_image, attendee_image)

            if comparison.success:
                self._delete_image(attendee_image)
                return Result(True, comparison.payload)

        self._delete_image(attendee_image)
        return Result(False, None)

    def _compare_images(self, registered_user_image: ImageMetadata, attendee_image: ImageMetadata) -> Result:
        result = DeepFace.verify(img1_path=registered_user_image.path,
                                 img2_path=attendee_image.path,
                                 detector_backend="ssd")

        if result['distance'] < COMPARISON_THRESHOLD:
            return Result(True, registered_user_image.id)
        return Result(False, None)

    def load_images(self) -> list[ImageMetadata]:
        directory_content = os.listdir(IMAGES_DIRECTORY)
        return map(lambda filename: ImageMetadata.from_filename(filename), directory_content)

    def save_image(self, image: ImageMetadata) -> None:
        cv2.imwrite(image.path, image.content)

    def _delete_image(self, image: ImageMetadata) -> None:
        if os.path.exists(image.path):
            os.remove(image.path)


class JsonPersister:

    def save_user(self, user: User) -> None:
        users_list = self._read_file(USERS_STORAGE)
        users_list.append(user.to_json())
        self._write_file(USERS_STORAGE, users_list)

    def load_user(self, id: str) -> User:
        users_list = self._read_file(USERS_STORAGE)
        json_user = (next(filter(lambda user: user["id"] == id, users_list)))
        return User.from_json(json_user)

    def save_attendance(self, user: User) -> None:
        attendance = Attendance(user)
        attendance_list = self._read_file(ATTENDANCE_STORAGE)
        attendance_list.append(attendance.to_json())
        self._write_file(ATTENDANCE_STORAGE, attendance_list)

    def _read_file(self, path) -> any:
        with open(path, 'r') as file:
            data = json.load(file)
            return data

    def _write_file(self, path, data) -> None:
        with open(path, 'w') as file:
            uniq_data = self._ensure_no_duplications(data, path)
            json.dump(uniq_data, file, indent=2)

    def _ensure_no_duplications(self, data, path):
        if path == USERS_STORAGE:
            users_list = list(map(lambda user: User.from_json(user), data))
            users_set = set(users_list)
            return list(map(lambda user: user.to_json(), users_set))

        if path == ATTENDANCE_STORAGE:
            attendance_list = list(
                map(lambda attendance: Attendance.from_json(attendance), data))
            attendance_set = set(attendance_list)
            return list(map(lambda attendance: attendance.to_json(), attendance_set))
