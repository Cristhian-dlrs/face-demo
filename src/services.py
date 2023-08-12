import json
import os
from tkinter import PhotoImage
import cv2
from deepface import DeepFace
from PIL import Image, ImageTk
from models import *


class ImageManager():

    def __init__(self, config: Configuration):
        self._config = config
        self._classifier = cv2.CascadeClassifier(
            config.cascade_classifier_model_path)

    def compare_images(self, registered_user_image: ImageMetadata, attendee_image: ImageMetadata) -> Result:
        result = DeepFace.verify(img1_path=registered_user_image.path,
                                 img2_path=attendee_image.path,
                                 detector_backend="ssd")

        if result['distance'] < self._config.comparison_threshold:
            return Result(True, registered_user_image.id)
        return Result(False, None)

    def capture_image(self) -> PhotoImage:
        detected = False
        count = 0
        videoCapture = cv2.VideoCapture(self._config.camera_index)
        while (True):
            count += 1
            frame = videoCapture.read()[self._config.camera_index]
            reflected_frame = cv2.flip(frame, 1)
            faces = self._detect_faces(reflected_frame)

            if len(faces):
                detected = True

                self._tag_faces(reflected_frame, faces[0])

            colorized_frame = cv2.cvtColor(reflected_frame, cv2.COLOR_BGR2RGB)
            display_frame = ImageTk.PhotoImage(
                Image.fromarray(colorized_frame))
            return display_frame

    def _detect_faces(self, frame) -> any:
        return self._classifier.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

    def _tag_face(self, image, face, tag=None) -> None:
        (x, y, width, height) = face
        color = None

        if len(tag):
            color = (0, 255, 0)
            tag = self._config.default_tag
        else:
            color = (255, 255, 0)

        cv2.rectangle(image, (x, y), (x+width, y+height), color, 2)
        cv2.putText(image, tag, (x, y-20), 2, 0.8, color, 1, cv2.LINE_AA)


class ImagePersister:

    def __init__(self, config: Configuration):
        self._config = config

    def register_image(self, user_id) -> None:
        image = self._get_camera_frame()
        imageMetadata = ImageMetadata.from_user_id(user_id)
        self._save_image(imageMetadata, image)

    def capture_attendee_image(self) -> ImageMetadata:
        image = self._get_camera_frame()
        imageMetadata = ImageMetadata.from_tmp_data()
        self._save_image(imageMetadata, image)
        return imageMetadata

    def load_image(self, id: str) -> ImageMetadata:
        filenames = os.listdir(self._config.image_storage)
        def by_id_in_filename(filename): return id in filename
        filename = next(filter(by_id_in_filename, filenames))
        return ImageMetadata.from_filename(filename)

    def load_images(self) -> list[ImageMetadata]:
        directory_content = os.listdir(self._config.image_storage)
        return map(lambda filename: ImageMetadata.from_filename(filename), directory_content)

    def _save_image(self, imageMetadata: ImageMetadata, image: any) -> None:
        cv2.imwrite(imageMetadata.path, image)

    def delete_image(self, imageMetadata: ImageMetadata) -> None:
        if os.path.exists(imageMetadata.path):
            os.remove(imageMetadata.path)


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

    def _read_file(self, path) -> Result:
        with open(path, 'r') as file:
            data = json.load(file)
            return data

    def _write_file(self, path, data) -> None:
        with open(path, 'w') as file:
            json.dump(data, file, indent=2)
