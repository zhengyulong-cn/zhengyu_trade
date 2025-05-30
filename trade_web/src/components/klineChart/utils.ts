import type { SeriesMarker, Time } from "lightweight-charts";
import type { ISegmentPoint } from "./interface";

export const getSegmentsLine = (
  segments: ISegmentPoint[]
): Array<{ time: Time; value: number }> => {
  return segments.map((segmentPoint) => {
    return {
      value: segmentPoint.price,
      time: segmentPoint.time,
    };
  });
};

export const getFenxingMarkerList = (fenxingList: any[]) => {
  const markers: SeriesMarker<any>[] = [];
  for (const item of fenxingList) {
    if (item.type === "top") {
      markers.push({
        time: item.time,
        price: item.close,
        position: "aboveBar",
        color: "#f68410",
        shape: "circle",
        text: "顶",
      });
    } else if (item.type === "bottom") {
      markers.push({
        time: item.time,
        price: item.close,
        position: "belowBar",
        color: "#f68410",
        shape: "circle",
        text: "底",
      });
    }
  }
  return markers;
};
