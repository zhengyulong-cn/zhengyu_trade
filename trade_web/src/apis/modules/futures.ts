import axios from "@/apis/axios";
import type { IKLineData } from "@/components/klineChart/interface";

const transDatetime2Time = (datetime: number) => {
  return datetime / 1000000000;
};

export const getFutureDataApi = async (params: {
  symbol: string;
  minutes: number;
}): Promise<IKLineData> => {
  const res = await axios.get("/api/futures/market_conditions", params);
  const data = res.data as any;
  const success = res.success;
  if (success) {
    return {
      ...data,
      klines: data.klines.map((kline: any) => ({
        ...kline,
        time: transDatetime2Time(kline.datetime),
      })),
      segments: {
        A0: data.segments.A0.map((segmentPoint: any) => ({
          ...segmentPoint,
          time: transDatetime2Time(segmentPoint.datetime),
        })),
        A1: data.segments.A1.map((segmentPoint: any) => ({
          ...segmentPoint,
          time: transDatetime2Time(segmentPoint.datetime),
        })),
      },
    };
  }
  throw new Error("获取数据失败");
};
