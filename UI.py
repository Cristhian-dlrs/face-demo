from tkinter import *
from imageComparer import *


def root_window():
    root = Tk()
    root.geometry("300x250")
    root.title("Assistance Tracker")

    Label(text="Name * ").pack()
    name = StringVar()
    name_entry = Entry(textvariable=name)
    name_entry.pack()

    Label(text="").pack()
    Button(text="Register User", height="2", width="30",
           command=lambda: on_register()).pack()

    Label(text="").pack()
    Button(text="Confirm Assistance", height="2",
           width="30", command=lambda: on_assist()).pack()

    def on_register():
        username = name.get()
        register_user(username)
        alert(root, "User Registered")

    def on_assist():

        result = confirm_user_assistance()
        if result[0] is True:
            alert(root, f"Assistance confirmed for {result[1]}")
        else:
            alert(root, "Image comparison failed", "red")

    root.mainloop()


def alert(root, msg, fg="green"):
    window = Toplevel(root)
    window.geometry("300x250")
    window.title("Alert")
    Label(window, text=msg, fg=fg).pack()


root_window()
