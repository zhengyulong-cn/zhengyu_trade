from flask import Blueprint, request
from trade_backend.futures.fetch_data import getFutureKline

futures_bp = Blueprint("futures", __name__)


@futures_bp.route("/klines")
def getMarketQuotesApi():
    symbol = request.args.get("symbol")
    minutes = int(request.args.get("minutes"))
    futureKline = getFutureKline(symbol, minutes)
    return {
        "symbol": symbol,
        "minutes": minutes,
        "klines": futureKline,
    }
