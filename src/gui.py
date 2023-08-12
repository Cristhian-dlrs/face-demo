from tkinter import *
from controller import *


# -----------------------------------------------------------------------------
# Main Window
# -----------------------------------------------------------------------------

def root_window(controller: GuiController):
    root = Tk()
    root.geometry("400x350")
    root.title("Assistance Tracker")

    Label(text="First Name * ").pack()
    first_name = StringVar()
    first_name_entry = Entry(textvariable=first_name)
    first_name_entry.pack()

    Label(text="Last Name * ").pack()
    last_name = StringVar()
    last_name_entry = Entry(textvariable=last_name)
    last_name_entry.pack()

    Label(text="Email * ").pack()
    email = StringVar()
    email_entry = Entry(textvariable=email)
    email_entry.pack()

    Label(text="").pack()
    Button(text="Register User", height="2", width="30",
           command=lambda: on_register()).pack()

    Label(text="").pack()
    Button(text="Confirm Assistance", height="2",
           width="30", command=lambda: on_assist()).pack()

    def on_register():
        controller.register_user(first_name_entry.get(),
                                 last_name_entry.get(),
                                 email_entry.get())
        alert(root, "User Registered")

    def on_assist():

        result = controller.confirm_attendance()
        if result.success:
            alert(
                root, f"Assistance confirmed for {result.payload.first_name} {result.payload.last_name}")
        else:
            alert(root, "Image comparison failed", "red")

    return root


# -----------------------------------------------------------------------------
# Components
# -----------------------------------------------------------------------------

def alert(root, msg, fg="green"):
    window = Toplevel(root)
    window.geometry("300x250")
    window.title("Alert")
    Label(window, text=msg, fg=fg).pack()
