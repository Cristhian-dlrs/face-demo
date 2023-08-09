import os
import cv2


class User:
    __slots__ = ("id", "first_name", "last_name", "email")

    def __init__(self, id: str, first_name: str, last_name: str, email: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


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
                 default_capture_id="tmp",
                 camera_index=1,
                 close_key=13,
                 window_title="Facial Recognition"):
        self.default_capture_id = default_capture_id
        self.camera_index = camera_index
        self.close_key = close_key
        self.window_title = window_title


class ImagePersister:

    def capture_image(directory_name: str, options: CameraOptions) -> Image:
        videoCapture = cv2.VideoCapture(options.camera_index)
        while (True):
            ret, frame = videoCapture.read()
            if ret is False:
                return Image(identifier=options.default_capture_id,
                             path=os.path.join(
                                 directory_name, options.default_capture_id),
                             data=None)

            cv2.imshow(options.window_title, frame)
            if cv2.waitKey(1) == options.close_key:
                videoCapture.release()
                cv2.destroyAllWindows()

                return Image(identifier=options.default_capture_id,
                             path=os.path.join(
                                 directory_name, options.default_capture_id),
                             data=frame)

    def load_image(self, id: str, directory_name: str) -> Image:
        filenames = os.listdir(directory_name)
        image_path = next(
            filter(lambda filename: id in filename, filenames))
        return Image(id=id, path=image_path, data=cv2.imread(image_path))

    def load_images(self, directory_name: str) -> list[Image]:
        directory_content = os.listdir(directory_name)
        return map(
            lambda filename: Image(id=filename.split('.')[0],
                                   path=os.path.join(
                                       directory_name, filename),
                                   data=cv2.imread(os.path.join(directory_name, filename))),
            directory_content)

    def save_image(self, image: Image) -> None:
        cv2.imwrite(image.path, image.data)

    def delete_image(self, image: Image) -> None:
        if os.path.exists(image.path):
            os.remove(image.path)


if __name__ == "__main__":

    print("")
