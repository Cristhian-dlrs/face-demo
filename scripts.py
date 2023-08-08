import os
def on_init() -> None:
    if not os.path.exists("images"):
        os.makedirs("images")
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
