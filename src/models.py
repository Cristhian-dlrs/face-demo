from datetime import date
import platform
import os
from config import *
from uuid import uuid4


class User():
    def __init__(self, first_name: str, last_name: str, email: str, id=None):
        if id is None:
            self._id = hash((first_name, last_name, email))
        else:
            self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.first_name == other.first_name\
            and self.last_name == other.last_name\
            and self.email == other.email

    def __hash__(self) -> int:
        return hash((self.first_name, self.last_name, self.email))

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
        return User(json_data["first_name"],
                    json_data["last_name"],
                    json_data["email"],
                    json_data["id"])

    def to_json(self) -> str:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }


class Attendance():
    def __init__(self, user, date=date.today().strftime("%Y-%m-%d")):
        self._user = user
        self._date = date

    def __hash__(self) -> int:
        return hash((self._date, self.user.first_name, self.user.last_name, self.user.email))

    def __eq__(self, other):
        if not isinstance(other, Attendance):
            return False
        return self.date == other.date and self.user == other.user

    @property
    def date(self) -> str:
        return self._date

    @property
    def user(self) -> str:
        return self._user

    @staticmethod
    def from_json(json_data: dict) -> 'Attendance':
        return Attendance(User.from_json(json_data['user']),
                          json_data['date'])

    def to_json(self) -> str:
        return {
            "date": self._date,
            "user": self._user.to_json(),
        }


class ImageMetadata:
    def __init__(self, path: str, content: any):
        self._path = path
        self._content = content

    @property
    def content(self) -> any:
        return self._content

    @property
    def path(self) -> str:
        return self._path

    @property
    def id(self) -> str:
        os_name = platform.system()
        if os_name == 'Windows':
            return self._path.split('\\')[-1].replace(IMAGE_FILE_EXTENSION, '')

        elif os_name in ['Darwin', 'Linux']:
            return self._path.split('/')[-1].replace(IMAGE_FILE_EXTENSION, '')

    @staticmethod
    def from_filename(filename: str) -> 'ImageMetadata':
        path = os.path.join(IMAGES_DIRECTORY, filename)
        return ImageMetadata(path, None)

    @staticmethod
    def from_user(user: User, content: any) -> 'ImageMetadata':
        path = os.path.join(IMAGES_DIRECTORY, user.id + IMAGE_FILE_EXTENSION)
        return ImageMetadata(path, content)

    @staticmethod
    def from_tmp_image(content: any) -> 'ImageMetadata':
        temp_path = os.path.join(TEMP_DIRECTORY,
                                 str(uuid4())+IMAGE_FILE_EXTENSION)
        return ImageMetadata(temp_path, content)


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
