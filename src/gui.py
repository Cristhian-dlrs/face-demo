from tkinter import *
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from config import *
from controller import *
import time


class GUI:

    def __init__(self, controller: GuiController):
        self._controller = controller
        self._root = Tk()
        self._current_image = None
        self._panel = None

    def handle_register_attendance(self):
        result = self._controller.confirm_attendance(self._current_image)
        if result.success:
            messagebox.showinfo(message=result.payload)
        else:
            messagebox.showerror(message=result.payload)

    def handle_register_user(self):
        register_form(self._root, self._current_image,
                      self._controller.register_user)

    def run(self):
        self._configure_root()
        time.sleep(SCREEN_WARMUP_TIME)
        self._start_recording()

    def _configure_root(self):
        self._root.geometry(ROOT_GEOMETRY)
        self._root.title(MAIN_WINDOW_TITLE)

        label_frame = LabelFrame(self._root, bg="blue")
        label_frame.pack()

        self._panel = Label(label_frame, bg="blue", width=650, height=500)
        self._panel.pack(side="top", padx=2, pady=2)

        attendance_btn = Button(self._root,
                                text=ATTENDANCE_BTN_LABEL,
                                height="2",
                                width="30",
                                command=lambda: self.handle_register_attendance())
        attendance_btn.pack(side="left")

        attendance_btn = Button(self._root,
                                text=REGISTER_USER_BTN_LABEL,
                                height="2",
                                width="30",
                                command=lambda: self.handle_register_user())
        attendance_btn.pack(side="right")

    def _start_recording(self):
        videoCapture = cv2.VideoCapture(CAMERA_INDEX)
        while (True):
            frame = videoCapture.read()[1]
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = self._get_faces(frame)
            frame = self._frame_faces(faces, frame)
            self._current_image = frame
            frame = ImageTk.PhotoImage(Image.fromarray(frame))
            self._panel['image'] = frame
            self._root.update()

    def _get_faces(self, frame) -> any:
        return cv2.CascadeClassifier(CASCADE_PATH).detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

    def _frame_faces(self, faces, frame) -> any:
        for (x, y, width, height) in faces:
            cv2.rectangle(frame,
                          (x, y),
                          (x+width, y+height),
                          (0, 255, 0), 2)
        return frame


# -----------------------------------------------------------------------------
# Components
# -----------------------------------------------------------------------------

def register_form(root, image, callback):
    window = Toplevel(root)
    window.geometry(FORM_GEOMETRY)
    window.title(FORM_WINDOW_TITLE)

    def on_register_user():
        result = callback(first_name_entry.get(),
                          last_name_entry.get(),
                          email_entry.get(),
                          image)

        if result.success:
            messagebox.showinfo(message=result.payload)
        else:
            messagebox.showerror(message=result.payload)
        window.destroy()

    Label(window, text="First Name * ").pack()
    first_name = StringVar()
    first_name_entry = Entry(window, textvariable=first_name)
    first_name_entry.pack()

    Label(window, text="Last Name * ").pack()
    last_name = StringVar()
    last_name_entry = Entry(window, textvariable=last_name)
    last_name_entry.pack()

    Label(window, text="Email * ").pack()
    email = StringVar()
    email_entry = Entry(window, textvariable=email)
    email_entry.pack()

    Label(window, text="").pack()
    Button(window, text=REGISTER_USER_BTN_LABEL, height="2", width="30",
           command=lambda: on_register_user()).pack()
