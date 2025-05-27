import axios from "@/apis/axios";

export const getFutureDataApi = (params: {
  symbol: string;
  minutes: number;
}) => {
  return axios.get("/api/futures/market_conditions", params);
};
