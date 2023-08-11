from datetime import date
from uuid import UUID, uuid4
import platform
import os


class User:
    def __init__(self, id: UUID, first_name: str, last_name: str, email: str):
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email

    @property
    def id(self) -> str:
        return str(self._id)

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def email(self) -> str:
        return self._email

    @staticmethod
    def from_json(json_data: dict) -> 'User':
        return User(json_data["id"],
                    json_data["first_name"],
                    json_data["last_name"],
                    json_data["email"])

    def to_json(self) -> str:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }


class Attendance:
    def __init__(self, user):
        self._user = user
        self._date = date.today().strftime("%Y-%m-%d")

    @property
    def date(self) -> str:
        return self._date

    def to_json(self) -> str:
        return {
            "date": self._date,
            "user": self._user.to_json(),
        }


class Image:
    def __init__(self, path: str, data: any):
        self._path = path
        self._data = data

    @property
    def path(self):
        return self._path

    @property
    def data(self):
        return self._data

    @property
    def id(self):
        os_name = platform.system()
        if os_name == 'Windows':
            return self._path.split('\\')[-1].replace('.jpg', '')

        elif os_name in ['Darwin', 'Linux']:
            return self._path.split('/')[-1].replace('.jpg', '')

    @staticmethod
    def from_filename(filename: str, data: any) -> 'Image':
        path = os.path.join("images", filename)
        return Image(path, data)

    @staticmethod
    def from_tmp_data(data: any) -> 'Image':
        temp_path = os.path.join("tmp", str(uuid4())+".jpg")
        return Image(temp_path, data)

    @staticmethod
    def from_user_id(user_id: str, data: any) -> 'Image':
        path = os.path.join("images", user_id+".jpg")
        return Image(path, data)


class Result:

    def __init__(self, success: bool, payload: any):
        self._success = success
        self._payload = payload

    @property
    def success(self) -> bool:
        return self._success

    @property
    def payload(self) -> any:
        return self._payload


class ImageManagerConfig:

    def __init__(self,
                 comparison_threshold=.2,
                 camera_index=0,
                 close_key=13,
                 window_title="Facial Recognition",
                 tmp_storage="tmp",
                 image_storage="images"):
        self._comparison_threshold = comparison_threshold
        self._camera_index = camera_index
        self._close_key = close_key
        self._window_title = window_title
        self._tmp_storage = tmp_storage
        self._image_storage = image_storage

    @property
    def comparison_threshold(self) -> float:
        return self._comparison_threshold

    @property
    def camera_index(self) -> int:
        return self._camera_index

    @property
    def window_title(self) -> str:
        return self._window_title

    @property
    def close_key(self) -> int:
        return self._close_key

    @property
    def tmp_storage(self) -> str:
        return self._tmp_storage

    @property
    def image_storage(self) -> str:
        return self._image_storage
