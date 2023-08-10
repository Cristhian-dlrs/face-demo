class User:
    __slots__ = ("id", "first_name", "last_name", "email")

    def __init__(self, id: str, first_name: str, last_name: str, email: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def to_json(self) -> str:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }


class Image:
    __slots__ = ("id", "path", "data")

    def __init__(self, id: str, path: str, data: any):
        self.id = id
        self.path = path
        self.data = data


class CameraOptions:
    __slots__ = ("default_capture_id", "camera_index",
                 "close_key", "window_title")

    def __init__(self,
                 default_capture_id="tmp.jpg",
                 camera_index=0,
                 close_key=13,
                 window_title="Facial Recognition"):
        self.default_capture_id = default_capture_id
        self.camera_index = camera_index
        self.close_key = close_key
        self.window_title = window_title
