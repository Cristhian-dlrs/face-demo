import cv2
from deepface import DeepFace
import json
from datetime import date
import os

# --------------------------------- CONFIG ------------------------------- #
CAMERA_INDEX = 0  # change depending on the machine
CLOSE_CAM_KEY_ORD = 13  # key ord for close the camera (default is "enter")
DATA_STORE = "attendance.json"
IMAGES_DIRECTORY = os.path.join(os.getcwd(), "images")
TMP_DIRECTORY = os.path.join(os.getcwd(), "tmp")
ACCURACY_THRESHOLD = .2


def register_user(username) -> None:
    user_img = capture_image()
    img_path = os.path.join(IMAGES_DIRECTORY, f"{username}.jpg")
    cv2.imwrite(img_path, user_img)


def confirm_user_assistance() -> [bool, str]:
    attendee_image = capture_image()
    attendee_image_path = os.path.join(TMP_DIRECTORY, "tmp_image.jpg")
    cv2.imwrite(attendee_image_path, attendee_image)
    registered_user_image_path = load_registered_user_image_paths()

    for image_path in registered_user_image_path:
        is_same_person = compare_images(image_path, attendee_image_path)

        if is_same_person:
            raw_image_path = r""+image_path
            username = raw_image_path.split("\\")[-1].replace(".jpg", "")
            save_attendance(username)
            os.remove(attendee_image_path)
            return [True, username]
    return [False, ""]


def capture_image() -> any:
    videoCapture = cv2.VideoCapture(CAMERA_INDEX)
    while (True):
        ret, frame = videoCapture.read()
        if ret is False:
            break

        cv2.imshow('Facial Registration', frame)
        if cv2.waitKey(1) == CLOSE_CAM_KEY_ORD:
            videoCapture.release()
            cv2.destroyAllWindows()
            return frame


def compare_images(image_path_a, image_path_b) -> dict[str, any]:
    result = DeepFace.verify(
        img1_path=image_path_a,
        img2_path=image_path_b, detector_backend="ssd")

    print(result)
    if result['distance'] < ACCURACY_THRESHOLD:
        return True
    return False


def load_registered_user_image_paths() -> list[str]:
    images_path = os.listdir(IMAGES_DIRECTORY)
    images_full_path = map(lambda x: os.path.join(
        IMAGES_DIRECTORY, x), images_path)

    return images_full_path


def save_attendance(username) -> None:
    today = date.today().strftime("%Y-%m-%d")
    with open(DATA_STORE, 'r') as file:
        data = json.load(file)

    data.append({
        "name": username,
        "date": today
    })

    with open(DATA_STORE, 'w') as file:
        json.dump(data, file, indent=4)


# --------------------------------- TEST ------------------------------- #
if __name__ == '__main__':
    # register_user("Christian")
    # result = check_user_assistance()
    # print(result)
    path = r"C:\Users\cdelarosa\Desktop\face-demo\images\Chris.jpg"

    raw_path = r"" + f"{path}"
    name = raw_path.split("\\")[-1].replace(".jpg", "")
    print(name)