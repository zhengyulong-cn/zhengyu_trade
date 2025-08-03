import pandas as pd
from tqsdk.ta import MA
from trade_backend.analysis_core.technical_analysis.public_type import SegmentPoint
from trade_backend.enum import Direction, FenxingType, MALevel

PRICE_AMPLITUDE_CONSTANT = 0.035


def getDirectionOnKline(ma1, ma2):
    if ma1 > ma2:
        return Direction.Up
    elif ma1 < ma2:
        return Direction.Down
    else:
        return None


def buildBaseDirectionOnKlines(klines):
    ma_a0 = MA(klines, MALevel.A0.value)
    ma_a1 = MA(klines, MALevel.A1.value)
    baseKlineDirections = [
        getDirectionOnKline(ma_a0.iloc[i]["ma"], ma_a1.iloc[i]["ma"])
        for i in range(len(ma_a0))
    ]
    return baseKlineDirections


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


def judgeIsLess4Kline(lastPriceObj: SegmentPoint, curPriceObj: SegmentPoint) -> bool:
    startIdx = lastPriceObj.id
    endIdx = curPriceObj.id
    # 对于大幅度暴涨暴跌特殊处理
    priceAmplitude = abs((curPriceObj.price - lastPriceObj.price) / lastPriceObj.price)
    return endIdx - startIdx < 4 and priceAmplitude < PRICE_AMPLITUDE_CONSTANT


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
            # 对相邻线段，如果小于4根K线，则删除
            isLess4Kline = judgeIsLess4Kline(lastPriceObj, priceObj)
            if isLess4Kline:
                segmentPointList.pop()
                continue
            # 添加新的线段
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


def buildRecursionSegments(baseSegments: list[SegmentPoint]) -> list[SegmentPoint]:
    """
    通过基础线段，递归构建高一级别线段
    """
    return []


def serializeSegments(segments: list[SegmentPoint]):
    return [segmentPoint.toDict() for segmentPoint in segments]


def buildAllSegments(klines):
    baseKlineDirections = buildBaseDirectionOnKlines(klines)
    baseSegments = buildSingleSegments(klines, baseKlineDirections)
    serializedSegmentsA0 = serializeSegments(baseSegments)
    return serializedSegmentsA0
