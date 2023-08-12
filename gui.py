import pathlib
from tkinter import *
from controller import *
import cv2


# -----------------------------------------------------------------------------
# Main Window
# -----------------------------------------------------------------------------
# def root_window(controller: GuiController):
cascade_path = pathlib.Path(cv2.__file__).parent.absolute(
) / "data/haarcascade_frontalface_default.xml"

clf = cv2.CascadeClassifier(str(cascade_path))


def root_window():
    root = Tk()
    config = Configuration(str(cascade_path))
    root.minsize = (650, 550)
    root.maxsize = (650, 550)

    root.title("Assistance Tracker")

    panel = None

    # return root
    # -------------------Demo Cam----------------------
    f1 = LabelFrame(root, bg="red")
    f1.pack()
    l1 = Label(f1, bg="red", width=650, height=500)
    l1.pack(side="left", padx=10, pady=10)

    Button(root, text="Register User").pack(
        side="bottom", fill="both", expand="yes", padx=10, pady=10)

    detected = 0
    videoCapture = cv2.VideoCapture(config.camera_index)
    while (detected != 200):
        detected += 1
        print(detected)
        frame = videoCapture.read()[1]
        reflected_frame = cv2.flip(frame, 1)
        faces = clf.detectMultiScale(
            reflected_frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(faces) > 1:
            detected = True

        for (x, y, width, height) in faces:
            if detected:
                cv2.rectangle(reflected_frame, (x, y), (x+width, y+height),
                              (0, 255, 0), 2)

                cv2.putText(reflected_frame, 'Christian', (x, y-20), 2,
                            0.8, (0, 255, 0), 1, cv2.LINE_AA)

            if not detected:
                cv2.rectangle(reflected_frame, (x, y), (x+width, y+height),
                              (255, 255, 0), 2)

                cv2.putText(reflected_frame, 'Registering...', (x, y-20), 2,
                            0.8, (255, 255, 0), 1, cv2.LINE_AA)

        colorized_frame = cv2.cvtColor(reflected_frame, cv2.COLOR_BGR2RGB)
        image_display = ImageTk.PhotoImage(Image.fromarray(colorized_frame))
        l1['image'] = image_display
        root.update()


# -----------------------------------------------------------------------------
# Components
# -----------------------------------------------------------------------------

# def alert(root, msg, fg="green"):
#     window = Toplevel(root)
#     window.geometry("300x250")
#     window.title("Alert")
#     Label(window, text=msg, fg=fg).pack()
if __name__ == "__main__":
    root_window()
