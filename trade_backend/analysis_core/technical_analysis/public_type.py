from trade_backend.enum import Direction, FenxingType


class Fenxing:
    def __init__(self, id: int, time: int, type: str, price: float):
        self.id = id
        self.time = time
        self.type = type
        # 顶分型时候为最高价，底分型时候为最低价
        self.price = price

    def __eq__(self, other: object) -> bool:
        return self.id == other.id

    def toDict(self):
        return self.__dict__


class Segment:
    def __init__(
        self,
        startFenxing: Fenxing,
        endFenxing: Fenxing,
        direction: Direction,
        building: bool,
    ):
        self.startFenxing = startFenxing
        self.endFenxing = endFenxing
        self.direction = direction
        self.building = building

    def toDict(self):
        return {
            "startFenxing": self.startFenxing,
            "endFenxing": self.endFenxing,
            "direction": self.direction.value,
            "building": self.building,
        }


class SegmentPoint:
    def __init__(
        self,
        id: int,
        type: FenxingType,
        price: float,
        datetime: int,
    ):
        self.id = id
        self.type = type
        self.price = price
        self.datetime = datetime

    def toDict(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "price": self.price,
            "datetime": self.datetime,
        }


class SequenceProperty:
    def __init__(
        self,
        startSegmentPoint: SegmentPoint,
        endSegmentPoint: SegmentPoint,
        direction: Direction,
    ):
        self.startSegmentPoint = startSegmentPoint
        self.endSegmentPoint = endSegmentPoint
        self.direction = direction
