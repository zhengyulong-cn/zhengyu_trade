from enum import Enum


class MALevel(Enum):
    A0 = 5
    A1 = 20
    A2 = 80


class Direction(Enum):
    Up = "Up"
    Down = "Down"

    def __str__(self):
        return self.value


class FenxingType(Enum):
    Top = "Top"
    Bottom = "Bottom"

    def __str__(self):
        return self.value
