import json
import os
from enum import Enum

class Config_Enum(Enum):
    RES_X = 1920
    RES_Y = 1080
    FPS = 30
    TAB = True
    TAB_LENGTH = 4
    FONT_NAME = ""
    FONT_PATH = "FSEX302.ttf"
    FONT_SIZE = 30
    FONT_COLOR = (0,255,0,)
    DURATION_TEXT = 2
    DURATION_CURSOR = 2
    EFFECT_WARP_INTENSITY = 0.15
    EFFECT_SCANLINE_INTENSITY = 0.3
    EFFECT_NOISE_INTENSITY = 0.03
    EFFECT_GLOW_INTENSITY = 3
    OVERRIDE_LINUX = ""
    OVERRIDE_KERNEL = ""
    OVERRIDE_DE = ""
    OVERRIDE_BASH = ""
    OVERRIDE_PHYS_MEM = ""

class Config():
    def __init__(self):
        self.config_dict = {enum.name: enum.value for enum in Config_Enum}

    def to_json(self, filename):
        # Convert config_dict to a serializable format (convert Enum members to their names)
        serializable_dict = {
            key: self.serialize_value(value) for key, value in self.config_dict.items()
        }

        with open(filename, 'w') as json_file:
            json.dump(serializable_dict, json_file, indent=4)

    def serialize_value(self, value):
        # Check if it's a tuple or other non-primitive types and handle accordingly
        if isinstance(value, tuple):
            return list(value)  # Convert tuple to list for JSON serialization
        return value  # For other types, return the value as is

    @classmethod
    def from_json(cls, filename):
        if not os.path.exists(filename):  # Check if the file exists
            config_instance = cls()  # Create an instance with default values
            config_instance.to_json(filename)  # Save default values to the file
            return config_instance  # Return the new instance with default values
        
        with open(filename, 'r') as json_file:
            data = json.load(json_file)

        # Convert values back to Enum members and handle non-primitive types
        config_instance = cls()
        config_instance.config_dict = {
            key: cls.deserialize_value(val) for key, val in data.items()
        }
        return config_instance

    @staticmethod
    def deserialize_value(value):
        # If the value is a list, convert it back to a tuple (e.g., FONT_COLOR)
        if isinstance(value, list):
            return tuple(value)  # Convert list back to tuple
        # If it's a known Enum value, convert it back to the Enum member
        elif isinstance(value, str):
            try:
                return Config_Enum[value]  # This assumes the value is the Enum member name
            except KeyError:
                return value  # Return as is if it's not a valid Enum member name
        return value

