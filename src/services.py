import json
import os
import cv2
from deepface import DeepFace
from datetime import date
from models import *


class ImageManager:

    def __init__(self, config: ImageManagerConfig):
        self._config = config

    def register_image(self, user_id) -> None:
        image = Image.from_user_id(user_id, self._get_camera_frame())
        self.save_image(image)

    def capture_attendee_image(self) -> Image:
        image = Image.from_tmp_data(self._get_camera_frame())
        self.save_image(image)
        return image

    def _get_camera_frame(self) -> any:
        videoCapture = cv2.VideoCapture(self._config.camera_index)
        while (True):
            ret, frame = videoCapture.read()
            if ret is False:
                videoCapture.release()
                cv2.destroyAllWindows()
                return frame

            cv2.imshow(self._config.window_title, frame)
            if cv2.waitKey(1) == self._config.close_key:
                videoCapture.release()
                cv2.destroyAllWindows()
                return frame

    def compare_images(self, registered_user_image: Image, attendee_image: Image) -> Result:
        result = DeepFace.verify(img1_path=registered_user_image.path,
                                 img2_path=attendee_image.path,
                                 detector_backend="ssd")

        if result['distance'] < self._config.comparison_threshold:
            return Result(True, registered_user_image.id)
        return Result(False, "")

    def load_image(self, id: str) -> Image:
        filenames = os.listdir(self._config.image_storage)
        def by_id_in_filename(filename): return id in filename
        filename = next(filter(by_id_in_filename, filenames))
        return Image.from_filename(filename, cv2.imread(filename))

    def load_images(self) -> list[Image]:
        directory_content = os.listdir(self._config.image_storage)
        return map(lambda filename: Image.from_filename(filename, cv2.imread(
            os.path.join(self._config.image_storage, filename))), directory_content)

    def save_image(self, image: Image) -> None:
        cv2.imwrite(image.path, image.data)

    def delete_image(self, image: Image) -> None:
        if os.path.exists(image.path):
            os.remove(image.path)


class JsonPersister:

    def __init__(self, user_storage_path, attendance_storage_path):
        self._user_storage_path = user_storage_path
        self._attendance_storage_path = attendance_storage_path

    def save_user(self, user: User) -> None:
        users_list = self._read_file(self._user_storage_path)
        users_list.append(user.to_json())
        self._write_file(self._user_storage_path, users_list)

    def load_user(self, id: str) -> User:
        users_list = self._read_file(self._user_storage_path)
        json_user = (next(filter(lambda user: user["id"] == id, users_list)))
        return User.from_json(json_user)

    def save_attendance(self, user: User) -> None:
        attendance = Attendance(user)
        attendance_list = self._read_file(self._attendance_storage_path)
        attendance_list.append(attendance.to_json())
        self._write_file(self._attendance_storage_path, attendance_list)

    def _read_file(self, path) -> any:
        with open(path, 'r') as file:
            data = json.load(file)
        return data

    def _write_file(self, path, data) -> None:
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
