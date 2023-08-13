import pathlib
import cv2

# Settings
JSON_IDENT = 2
DEEPFACE_DETECTOR_BACKEND = "ssd"
IMAGE_FILE_EXTENSION = '.jpg'
ROOT_GEOMETRY = "700x600"
FORM_GEOMETRY = "300x250"
COMPARISON_THRESHOLD = 0.2
CAMERA_INDEX = 0
SCREEN_WARMUP_TIME = 1
USERS_STORAGE = "storage_users.json"
ATTENDANCE_STORAGE = "storage_attendance.json"
IMAGES_DIRECTORY = "images"
TEMP_DIRECTORY = "tmp"
CASCADE_PATH = str(pathlib.Path(cv2.__file__).parent.absolute(
) / "data/haarcascade_frontalface_default.xml")

# Messages
USER_REGISTRATION_SUCCESS_MESSAGE = "User successfully registered, welcome"
USER_REGISTRATION_ERROR_MESSAGE = "An error has occurred, please try again"
ATTENDANCE_CONFIRMED_SUCCESS_MESSAGE = "Attendance confirmed for"
ATTENDANCE_CONFIRMATION_FAILED_MESSAGE = "User not recognized, please try again"
ATTENDANCE_CONFIRMATION_ERROR_MESSAGE = "An error has occurred, please try again"


# Labels
FORM_WINDOW_TITLE = "User Registration Form"
MAIN_WINDOW_TITLE = "Assistance Tracker"
ATTENDANCE_BTN_LABEL = "Register Attendance"
REGISTER_USER_BTN_LABEL = "Register User"
