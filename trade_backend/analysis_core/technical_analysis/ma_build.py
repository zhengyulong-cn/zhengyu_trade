import pandas as pd
from tqsdk.ta import MA
from trade_backend.analysis_core.technical_analysis.public_type import SegmentPoint
from trade_backend.enum import Direction, FenxingType, MALevel


def getDirectionOnKline(ma1, ma2):
    if ma1 > ma2:
        return Direction.Up
    elif ma1 < ma2:
        return Direction.Down
    else:
        return None


def buildDirectionOnKlines(klines):
    ma_a0 = MA(klines, MALevel.A0.value)
    ma_a1 = MA(klines, MALevel.A1.value)
    ma_a2 = MA(klines, MALevel.A2.value)

    direction_a0 = [
        getDirectionOnKline(ma_a0.iloc[i]["ma"], ma_a1.iloc[i]["ma"])
        for i in range(len(ma_a0))
    ]
    direction_a1 = [
        getDirectionOnKline(ma_a1.iloc[i]["ma"], ma_a2.iloc[i]["ma"])
        for i in range(len(ma_a1))
    ]

    return direction_a0, direction_a1


def getPenMaxMinPrice(
    histPrice: pd.DataFrame,
    startIdx: int,
    endIdx: int,
    direct: int,
):
    if direct == Direction.Up:
        lowMinPrice = histPrice.iloc[startIdx:endIdx]["low"].min()
        lowMinPriceIdx = histPrice.iloc[startIdx:endIdx]["low"].idxmin()
        return SegmentPoint(
            id=lowMinPriceIdx,
            type=FenxingType.Bottom if direct == Direction.Up else FenxingType.Top,
            price=lowMinPrice,
            datetime=histPrice.iloc[lowMinPriceIdx]["datetime"],
        )
    elif direct == Direction.Down:
        highMaxPrice = histPrice.iloc[startIdx:endIdx]["high"].max()
        highMaxPriceIdx = histPrice.iloc[startIdx:endIdx]["high"].idxmax()
        return SegmentPoint(
            id=highMaxPriceIdx,
            type=FenxingType.Bottom if direct == Direction.Up else FenxingType.Top,
            price=highMaxPrice,
            datetime=histPrice.iloc[highMaxPriceIdx]["datetime"],
        )
    else:
        raise ValueError("direct的值不可能为0，请检查输入数据")


def buildSingleSegments(klines, klineDirections) -> list[SegmentPoint]:
    penDirect = None
    # 笔判断条件切换的点位
    switchList = []
    for i, curDirect in enumerate(klineDirections):
        if curDirect == Direction.Up and penDirect != Direction.Up:
            penDirect = Direction.Up
            switchList.append((i, penDirect))
        if curDirect == Direction.Down and penDirect != Direction.Down:
            penDirect = Direction.Down
            switchList.append((i, penDirect))
    segmentPointList: list[SegmentPoint] = []
    for i in range(len(switchList)):
        curSwitch = switchList[i]
        endIdx = curSwitch[0]
        direct = curSwitch[1]
        if i == 0:
            priceObj = getPenMaxMinPrice(klines, 0, endIdx, direct)
            segmentPointList.append(priceObj)
        else:
            lastPriceObj = segmentPointList[len(segmentPointList) - 1]
            # 开始的那天不算，避免日期重叠
            startIdx = lastPriceObj.id + 1
            priceObj = getPenMaxMinPrice(klines, startIdx, endIdx, direct)
            segmentPointList.append(priceObj)
        if i == len(switchList) - 1:
            lastPriceObj = segmentPointList[len(segmentPointList) - 1]
            # 开始的那天不算，避免日期重叠
            startIdx = lastPriceObj.id + 1
            priceObj = getPenMaxMinPrice(
                klines,
                startIdx,
                len(klines),
                Direction.Down if direct == Direction.Up else Direction.Up,
            )
            segmentPointList.append(priceObj)
    return segmentPointList


def serializeSegments(segments: list[SegmentPoint]):
    return [segmentPoint.toDict() for segmentPoint in segments]


def buildAllSegments(klines):
    klineDirectionsA0, klineDirectionsA1 = buildDirectionOnKlines(klines)
    segmentsA0 = buildSingleSegments(klines, klineDirectionsA0)
    serializedSegmentsA0 = serializeSegments(segmentsA0)
    segmentsA1 = buildSingleSegments(klines, klineDirectionsA1)
    serializedSegmentsA1 = serializeSegments(segmentsA1)
    return serializedSegmentsA0, serializedSegmentsA1
