"""
Basic unit tests for the awbw module on select sample replays.

To run:
python -m unittest -v
"""

import unittest

from .game import DefaultDict

# pylint: disable=no-self-use

class TestDefaultDict(unittest.TestCase):
    """Tests for the DefaultDict class"""

    class ColorDict(DefaultDict):
        """Example DefaultDict"""

        ALLOWED_DATA = {
            "r": 0,
            "g": 0,
            "b": 0,
        }

    def test_color_dict(self):
        """Test that we can create and use ColorDict as a dict"""
        test_dict = TestDefaultDict.ColorDict(r=100)
        assert test_dict["r"] == 100
        assert test_dict["b"] == 0
        assert test_dict["g"] == 0

        test_dict = test_dict | { "r": 255, "b": 255 }
        assert test_dict["r"] == 255
        assert test_dict["b"] == 255
        assert test_dict["g"] == 0

        test_dict = TestDefaultDict.ColorDict(r=123, b=45, g=67)
        assert test_dict["r"] == 123
        assert test_dict["b"] == 45
        assert test_dict["g"] == 67

        test_dict = TestDefaultDict.ColorDict({"r": 15, "b": 22, "g": 81})
        assert test_dict["r"] == 15
        assert test_dict["b"] == 22
        assert test_dict["g"] == 81

        zero_dict = TestDefaultDict.ColorDict()
        assert zero_dict["r"] == 0
        assert zero_dict["b"] == 0
        assert zero_dict["g"] == 0

    def test_bad_keys(self):
        """Test that an exception is raised when an invalid key is used"""
        with self.assertRaises(KeyError):
            DefaultDict(r=100)
        with self.assertRaises(KeyError):
            DefaultDict({"r":100})
        with self.assertRaises(KeyError):
            TestDefaultDict.ColorDict(pi=3.1415)
        with self.assertRaises(KeyError):
            TestDefaultDict.ColorDict({"pi":3.1415})
