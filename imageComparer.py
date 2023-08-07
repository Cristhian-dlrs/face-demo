from tkinter import *
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN as FaceDetector
import json
from datetime import date

# --------------------------------- CONFIG ------------------------------- #
CAMERA_INDEX = 1  # change depending on the machine
CLOSE_CAM_KEY_ORD = 13  # key ord for close the camera (default is "enter")
ACCURACY_THRESHOLD = 70  # change depending on the desired accuracy
COMPARISON_RESULT_THRESHOLD = .85
DATA_STORE = "attendance.json"


def register_user(username):
    img = capture_image()
    save_image(img, username)


def check_user_assistance(username) -> bool:
    login_user_img = capture_image()
    login_user_face = crop_face_from_image(login_user_img)
    actual_user_face = cv2.imread(f"faces/{username}.jpg")
    comparison_result = compare_images(
        actual_user_face, login_user_face) > COMPARISON_RESULT_THRESHOLD

    if comparison_result:
        save_attendance(username)
        return True
    else:
        return False


def save_attendance(username):
    today = date.today().strftime("%Y-%m-%d")
    with open(DATA_STORE, 'r') as file:
        data = json.load(file)

    data.append({
        "name": username,
        "date": today
    })

    with open(DATA_STORE, 'w') as file:
        json.dump(data, file, indent=4)


def capture_image():
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


def save_image(img, username):
    cropped_face = crop_face_from_image(img)
    cv2.imwrite(f"faces/{username}.jpg", cropped_face)


def crop_face_from_image(img):
    face = FaceDetector().detect_faces(img)[0]
    x1, y1, width, heigh = face['box']
    x2, y2 = x1 + width, y1 + heigh
    cropped_face = img[y1:y2, x1:x2]
    return cv2.resize(cropped_face, (300, 400),
                      interpolation=cv2.INTER_CUBIC)  # during comparison, images must have the same size


def compare_images(faceA, faceB) -> bool:
    imageDescriptor = cv2.ORB_create()
    _, descr_a = imageDescriptor.detectAndCompute(faceA, None)
    _, descr_b = imageDescriptor.detectAndCompute(faceB, None)

    imageComparer = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = imageComparer.match(descr_a, descr_b)
    if len(matches) == 0:
        return 0

    similar_regions = [i for i in matches if i.distance < ACCURACY_THRESHOLD]
    similarity_ratio = len(similar_regions)/len(matches)

    return similarity_ratio


# --------------------------------- TEST ------------------------------- #
# if __name__ == '__main__':
#     register_user("Christian")
#     time.sleep(1)
#     result = check_user_assistance("Christian")
#     print(result)
