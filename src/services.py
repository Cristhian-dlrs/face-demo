import json
import os
import cv2
from deepface import DeepFace
from datetime import date
from models import *


class ImagePersister:

    def __init__(self, image_storage, tmp_storage):
        self.image_storage = image_storage
        self.tmp_storage = tmp_storage

    def capture_image(self, options: CameraOptions) -> Image:
        videoCapture = cv2.VideoCapture(options.camera_index)
        while (True):
            ret, frame = videoCapture.read()
            if ret is False:
                return Image(id=options.default_capture_id,
                             path=os.path.join(
                                 self.tmp_storage, options.default_capture_id),
                             data=None)

            cv2.imshow(options.window_title, frame)
            if cv2.waitKey(1) == options.close_key:
                videoCapture.release()
                cv2.destroyAllWindows()

                return Image(id=options.default_capture_id,
                             path=os.path.join(
                                 self.tmp_storage, options.default_capture_id),
                             data=frame)

    def compare_images(self, user_image: Image, capture: Image) -> [bool, str]:
        result = DeepFace.verify(
            img1_path=user_image.path,
            img2_path=capture.path,
            detector_backend="ssd")

        if result['distance'] < .2:
            return [True, user_image.id]
        return [False, ""]

    def load_image(self, id: str) -> Image:
        filenames = os.listdir(self.image_storage)
        image_path = next(
            filter(lambda filename: id in filename, filenames))
        return Image(id=id, path=image_path, data=cv2.imread(image_path))

    def load_images(self) -> list[Image]:
        directory_content = os.listdir(self.image_storage)
        return map(
            lambda filename: Image(id=filename.split('.')[0],
                                   path=os.path.join(
                                       self.image_storage, filename),
                                   data=cv2.imread(os.path.join(self.image_storage, filename))),
            directory_content)

    def save_image(self, image: Image) -> None:
        cv2.imwrite(image.path, image.data)

    def delete_image(self, image: Image) -> None:
        if os.path.exists(image.path):
            os.remove(image.path)


class JsonPersister:

    def __init__(self, user_storage_path, attendance_storage_path):
        self.user_storage_path = user_storage_path
        self.attendance_storage_path = attendance_storage_path

    def save(self, user: User) -> None:
        with open(self.user_storage_path, 'r') as file:
            data = json.load(file)

        data.append(user.to_json())
        with open(self.user_storage_path, 'w') as file:
            json.dump(data, file, indent=4)

    def load_user(self, id: str) -> User:
        with open(self.user_storage_path, 'r') as file:
            users = json.load(file)

        user_json = next(filter(lambda user: user["id"] == id, users))
        user = User(user_json["id"], user_json["first_name"], user_json["last_name"],
                    user_json["email"])
        return user

    def save_attendance(self, user: User) -> None:
        today = date.today().strftime("%Y-%m-%d")
        with open(self.attendance_storage_path, 'r') as file:
            data = json.load(file)

        data.append({
            f"{today}": user.to_json(),
        })

        with open(self.attendance_storage_path, 'w') as file:
            json.dump(data, file, indent=4)


if __name__ == "__main__":
    pass
