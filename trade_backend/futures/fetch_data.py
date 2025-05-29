from tqsdk import TqApi, TqAuth
import pandas as pd
from typing import List


def getTqApi():
    return TqApi(auth=TqAuth("Zhengyu", "lzy523024"))


def transKline2Standard(sourceKline: pd.DataFrame, durationMinutes: int) -> List:
    # 将纳秒级时间戳转换为秒级，添加15分钟的偏移，然后转回时间戳
    sourceKline["datetime"] = (
        pd.to_datetime(sourceKline["datetime"].astype(float) / 1e9, unit="s")
        + pd.Timedelta(minutes=durationMinutes)
    ).astype(int) // 1000000000
    sourceKline["time"] = sourceKline["datetime"]
    return sourceKline.to_dict(orient="records")


def getFutureKline(symbol: str, durationMinutes: int):
    api = getTqApi()
    sourceKline: pd.DataFrame = api.get_kline_serial(
        symbol=symbol, data_length=260, duration_seconds=durationMinutes * 60
    )
    return transKline2Standard(sourceKline, durationMinutes)
