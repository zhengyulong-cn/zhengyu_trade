from enum import Enum


class Direction(Enum):
    Up = "Up"
    Down = "Down"

    def __str__(self):
        return self.value
