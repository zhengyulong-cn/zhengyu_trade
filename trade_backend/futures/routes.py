from flask import Blueprint, request
from trade_backend.futures.fetch_data import getFutureKline
from trade_backend.analysis_core.technical_analysis.ma_build import buildAllSegments
from trade_backend.analysis_core.technical_analysis.opportunities_analysis import (
    analysisOpportunities,
)

futures_bp = Blueprint("futures", __name__)


@futures_bp.route("/market_conditions")
def getMarketConditionsApi():
    symbol = request.args.get("symbol")
    minutes = int(request.args.get("minutes"))
    futureKline = getFutureKline(symbol, minutes)
    serializeKline = futureKline.to_dict(orient="records")
    segmentsA0, segmentsA1 = buildAllSegments(futureKline)
    # analysisOpportunities(segmentsA0, segmentsA1)
    return {
        "symbol": symbol,
        "minutes": minutes,
        "klines": serializeKline,
        "segments": {
            "A0": segmentsA0,
            "A1": segmentsA1,
        },
    }
