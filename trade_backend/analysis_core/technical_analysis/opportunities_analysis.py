"""
该文件主要分析最近时间的情况及给出开仓平仓信号
"""

from trade_backend.analysis_core.technical_analysis.public_type import (
    SegmentPoint,
    SequenceProperty,
)
from trade_backend.enum import FenxingType, Direction


def getSegmentDirection(startSegmentPoint: SegmentPoint, endSegmentPoint: SegmentPoint):
    if (
        startSegmentPoint["type"] == FenxingType.Top.value
        and endSegmentPoint["type"] == FenxingType.Bottom.value
    ):
        return Direction.Down
    elif (
        startSegmentPoint["type"] == FenxingType.Bottom.value
        and endSegmentPoint["type"] == FenxingType.Top.value
    ):
        return Direction.Up
    return None


def getCurrencyLastMarkedSequenceProperty(
    a0Segments: list[SegmentPoint], a1Segments: list[SegmentPoint]
) -> SequenceProperty:
    """
    获取当前趋势最近被识别的特征序列
    """
    startA1SegmentPoint = a1Segments[-2]
    endA1SegmentPoint = a1Segments[-1]
    startA1SegmentPointId = startA1SegmentPoint["id"]
    endA1SegmentPointId = endA1SegmentPoint["id"]
    a1LastDirection = getSegmentDirection(startA1SegmentPoint, endA1SegmentPoint)
    sequencePropertyList = []
    for i in range(len(a0Segments)):
        if (
            a0Segments[i]["id"] < startA1SegmentPointId
            or a0Segments[i]["id"] > endA1SegmentPointId
        ):
            continue
        startA0SegmentPoint = a0Segments[i]
        endA0SegmentPoint = a0Segments[i + 1]
        a0SegmentDirection = getSegmentDirection(startA0SegmentPoint, endA0SegmentPoint)
        if a0SegmentDirection != a1LastDirection:
            sequencePropertyList.append(
                SequenceProperty(
                    startA0SegmentPoint, endA0SegmentPoint, a0SegmentDirection
                )
            )
    print(sequencePropertyList)
    return []


def analysisOpportunities(
    a0Segments: list[SegmentPoint], a1Segments: list[SegmentPoint]
):
    """
    分析最近特征序列
    """
    sequenceProperties = getCurrencyLastMarkedSequenceProperty(a0Segments, a1Segments)
    return []
