from tqsdk import TqApi, TqAuth
import pandas as pd
from typing import List


def getTqApi():
    return TqApi(auth=TqAuth("Zhengyu", "lzy523024"))


def getFutureKline(symbol: str, durationMinutes: int):
    api = getTqApi()
    sourceKline: pd.DataFrame = api.get_kline_serial(
        symbol=symbol, data_length=500, duration_seconds=durationMinutes * 60
    )
    return sourceKline
