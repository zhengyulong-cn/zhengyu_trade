from trade_backend.enum import Direction


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


def removeInclude(klines):
    """删除包含关系"""
    removedIncludeKlines = []
    for i in range(0, len(klines)):
        currentKline = klines[i]
        if i < 2:
            removedIncludeKlines.append(currentKline)
            continue

        lastKline = removedIncludeKlines[-1]
        lastSecondKline = removedIncludeKlines[-2]
        if (
            lastKline["high"] >= currentKline["high"]
            and lastKline["low"] <= currentKline["low"]
        ) or (
            lastKline["high"] <= currentKline["high"]
            and lastKline["low"] >= currentKline["low"]
        ):
            smallDirection = (
                Direction.Up
                if (lastKline["high"] > lastSecondKline["high"])
                else Direction.Down
            )
            if smallDirection == Direction.Up:
                maxHigh = max(lastKline["high"], currentKline["high"])
                maxLow = max(lastKline["low"], currentKline["low"])
                mergedKline = {
                    "id": currentKline["id"],
                    "time": currentKline["time"],
                    "symbol": currentKline["symbol"],
                    "high": maxHigh,
                    "low": maxLow,
                    "open": maxLow,
                    "close": maxHigh,
                }
                removedIncludeKlines.pop()
                removedIncludeKlines.append(mergedKline)
            else:
                minHigh = min(lastKline["high"], currentKline["high"])
                minLow = min(lastKline["low"], currentKline["low"])
                mergedKline = {
                    "id": currentKline["id"],
                    "time": currentKline["time"],
                    "symbol": currentKline["symbol"],
                    "high": minHigh,
                    "low": minLow,
                    "open": minHigh,
                    "close": minLow,
                }
                removedIncludeKlines.pop()
                removedIncludeKlines.append(mergedKline)
        else:
            removedIncludeKlines.append(currentKline)
    return removedIncludeKlines


def isTopFenxing(k1, k2, k3):
    """判断顶分型（中间K线最高价最高且最低价最高）"""
    return (
        k2["high"] > k1["high"]
        and k2["high"] > k3["high"]
        and k2["low"] > k1["low"]
        and k2["low"] > k3["low"]
    )


def isBottomFenxing(k1, k2, k3):
    """判断底分型（中间K线最低价最低且最高价最低）"""
    return (
        k2["low"] < k1["low"]
        and k2["low"] < k3["low"]
        and k2["high"] < k1["high"]
        and k2["high"] < k3["high"]
    )


def fenxingBuild(klines) -> list[Fenxing]:
    """分型构建"""
    fenxingList = []
    for i in range(1, len(klines) - 1):
        if isTopFenxing(klines[i - 1], klines[i], klines[i + 1]):
            fenxingList.append(
                Fenxing(
                    klines[i]["id"], klines[i]["time"], "top", klines[i]["high"]
                ).toDict()
            )
        elif isBottomFenxing(klines[i - 1], klines[i], klines[i + 1]):
            fenxingList.append(
                Fenxing(
                    klines[i]["id"], klines[i]["time"], "bottom", klines[i]["low"]
                ).toDict()
            )
    return fenxingList


def checkSegmentFenxingLenIsOk(
    currentFenxing: Fenxing, comparedFenxing: Fenxing, klines: list[dict]
) -> bool:
    """检查线段分型长度是否符合要求"""
    currentFenxingIndex = next(
        (i for i, kline in enumerate(klines) if kline["id"] == currentFenxing["id"]),
        None,
    )
    comparedFenxingIndex = next(
        (i for i, kline in enumerate(klines) if kline["id"] == comparedFenxing["id"]),
        None,
    )
    return comparedFenxingIndex - currentFenxingIndex >= 4


def checkSegmentIncludeIsOk(
    startFenxing: Fenxing, endFenxing: Fenxing, includesFenxingList: list[Fenxing]
) -> bool:
    """检查线段是否成立"""
    if startFenxing["type"] == endFenxing["type"]:
        return False
    if startFenxing["type"] == "top":
        return all(
            item["price"] <= startFenxing["price"] for item in includesFenxingList
        ) and all(item["price"] >= endFenxing["price"] for item in includesFenxingList)
    if startFenxing["type"] == "bottom":
        return all(
            item["price"] >= startFenxing["price"] for item in includesFenxingList
        ) and all(item["price"] <= endFenxing["price"] for item in includesFenxingList)


def checkSegmentBackTracker(
    comparedFenxing: Fenxing, backTracker: list[Fenxing]
) -> bool:
    return any(item["id"] == comparedFenxing["id"] for item in backTracker)


def findNextFenxing(
    currentFenxing: Fenxing | None,
    klines: list[dict],
    fenxingList: list[Fenxing],
    backTracker: list[Fenxing],
) -> Fenxing:
    """找下一根符合笔构建的最近的分型。当前为顶分型，下一个一定是底分型；当前是底分型，下一个一定是顶分型"""
    if currentFenxing is None:
        return None
    currentFenxingType = currentFenxing["type"]
    currentFenxingIndex = fenxingList.index(currentFenxing)
    nextFenxing = None
    walkedFenxingList = []
    for i in range(currentFenxingIndex + 1, len(fenxingList)):
        comparedFenxing = fenxingList[i]
        comparedFenxingType = comparedFenxing["type"]

        if (currentFenxingType == "top" and comparedFenxingType == "bottom") or (
            currentFenxingType == "bottom" and comparedFenxingType == "top"
        ):
            segmentFenxingLenIsOk = checkSegmentFenxingLenIsOk(
                currentFenxing, comparedFenxing, klines
            )
            segmentIncludeIsOk = checkSegmentIncludeIsOk(
                currentFenxing, comparedFenxing, walkedFenxingList
            )
            segmentBackTracker = checkSegmentBackTracker(comparedFenxing, backTracker)
            # 让一些次低点也能符合要求
            # if (
            #     len(backTracker) > 1
            #     and segmentFenxingLenIsOk
            #     and not segmentIncludeIsOk
            # ):
            #     segmentIncludeIsOk = True
            if segmentFenxingLenIsOk and segmentIncludeIsOk and not segmentBackTracker:
                nextFenxing = comparedFenxing
                break
        walkedFenxingList.append(comparedFenxing)

    return nextFenxing


def safeSegmentsHandle(segments: list[Segment]) -> list[Segment]:
    """
    segments列表的元素的direction必须交替，如果出现连续的相同direction则合并
    """
    safeSegments = []
    i = 0
    while i < len(segments):
        if i < len(segments) - 1 and segments[i].direction == segments[i + 1].direction:
            safeSegments.append(
                Segment(
                    segments[i].startFenxing,
                    segments[i + 1].endFenxing,
                    segments[i].direction,
                    False,
                )
            )
            i = i + 2
            continue
        safeSegments.append(segments[i])
        i = i + 1
    return safeSegments


def baseSegmentBuild(klines, fenxingList: list[Fenxing]) -> list[Segment]:
    """笔构建
    笔的规则：
    1. 笔的起点和终点都是分型
    2. 上涨笔和下跌笔不断循环，不可能连续两个上涨笔或下跌笔
    3. 无论上涨笔还是下跌笔，笔的起点和终点是该笔的最高最低点
    4. 响铃顶底分型之间至少间隔1根K线或者说顶底之间至少5根K线
    """
    segments: list[Segment] = []
    backTracker = []
    p = fenxingList[0]
    pIndex = fenxingList.index(p)
    # 循环构建历史笔
    while pIndex < len(fenxingList) - 1:
        pNext = findNextFenxing(p, klines, fenxingList, backTracker)
        # pNext指向分型列表最后一个时候结束程序
        if not pNext == None and pNext["id"] == fenxingList[-1]["id"]:
            break
        if pNext == None:
            pIndex = pIndex + 1
            p = fenxingList[pIndex]
            continue
        pNextNext = findNextFenxing(pNext, klines, fenxingList, [])
        if pNextNext == None:
            backTracker.append(pNext)
            continue
        backTracker = []
        if p["type"] == "top":
            segments.append(Segment(p, pNext, Direction.Down, False))
        else:
            segments.append(Segment(p, pNext, Direction.Up, False))
        p = pNext
        pIndex = fenxingList.index(p)
    # 对可能有重复方向的笔进行安全处理
    segments = safeSegmentsHandle(segments)
    # 处理最后正在构建的笔
    lastSegmentDirection = segments[-1].direction
    lastSegmentStartFenxing = segments[-1].endFenxing
    lastMatchFenxing = next(
        (
            item
            for item in reversed(fenxingList)
            if (
                (item["type"] == "top" and lastSegmentDirection == Direction.Down)
                or (item["type"] == "bottom" and lastSegmentDirection == Direction.Up)
            )
        ),
        None,
    )
    if not lastMatchFenxing == None:
        segments.append(
            Segment(
                lastSegmentStartFenxing,
                lastMatchFenxing,
                (
                    Direction.Up
                    if lastSegmentDirection == Direction.Down
                    else Direction.Down
                ),
                True,
            )
        )
    return [item.toDict() for item in segments]
