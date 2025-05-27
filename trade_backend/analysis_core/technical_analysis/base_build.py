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
                "UP" if (lastKline["high"] > lastSecondKline["high"]) else "DOWN"
            )
            if smallDirection == "UP":
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


def fenxingBuild(klines):
    """分型构建"""
    fenxingList = []
    for i in range(1, len(klines) - 1):
        if isTopFenxing(klines[i - 1], klines[i], klines[i + 1]):
            fenxingList.append(
                {
                    "id": klines[i]["id"],
                    "time": klines[i]["time"],
                    "type": "top",
                }
            )
        elif isBottomFenxing(klines[i - 1], klines[i], klines[i + 1]):
            fenxingList.append(
                {
                    "id": klines[i]["id"],
                    "time": klines[i]["time"],
                    "type": "bottom",
                }
            )
    return fenxingList
