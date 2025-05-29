from flask import Blueprint, request
from trade_backend.futures.fetch_data import getFutureKline
from trade_backend.analysis_core.technical_analysis.base_build import (
    removeInclude,
    fenxingBuild,
    baseSegmentBuild,
)

futures_bp = Blueprint("futures", __name__)


@futures_bp.route("/market_conditions")
def getMarketConditionsApi():
    symbol = request.args.get("symbol")
    minutes = int(request.args.get("minutes"))
    futureKline = getFutureKline(symbol, minutes)
    futureKline = removeInclude(futureKline)
    fenxingList = fenxingBuild(futureKline)
    segments = baseSegmentBuild(futureKline, fenxingList)
    return {
        "symbol": symbol,
        "minutes": minutes,
        "klines": futureKline,
        "fenxingList": fenxingList,
        "segments": segments,
    }
