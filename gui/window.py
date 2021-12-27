
import arcade

class Window():
    """
    Create an instance of the Window to create visuals.
    """

    def __init__(self):
        self.w = 600
        self.h = 600
        self.name = "AW Window"

    def open(self):
        arcade.open_window(self.w, self.h, self.name)
        arcade.run()
