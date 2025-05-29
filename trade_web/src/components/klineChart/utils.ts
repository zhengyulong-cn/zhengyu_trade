import type { SeriesMarker, Time } from "lightweight-charts";
import type { ISegment } from "./interface";

export const getSegmentsLine = (
  segments: ISegment[]
): Array<{ time: Time; value: number }> => {
  return segments.map((segment) => {
    return {
      time: segment.startFenxing.time as Time,
      value: segment.startFenxing.price,
    };
  });
};

export const getLastSegmentLine = (segments: ISegment[]) => {
  const lastSegment = segments[segments.length - 1];
  return [
    {
      time: lastSegment.startFenxing.time as Time,
      value: lastSegment.startFenxing.price,
    },
    {
      time: lastSegment.endFenxing.time as Time,
      value: lastSegment.endFenxing.price,
    },
  ];
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
