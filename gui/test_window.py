
import window

def setup_parser(parser):
    """
    Arguments for the window test command go here
    """
    pass

def test_window(args):
    """
    The test function for the GUI module
    """

    myWindow = window.Window()
    myWindow.open()

if __name__ == "__main__":
    test_window(None)
