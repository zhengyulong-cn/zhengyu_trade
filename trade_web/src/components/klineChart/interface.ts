export interface IKLineItem {
  /** K线id */
  id: number;
  /** 股票或期货代码 */
  symbol: string;
  /** 时间戳 */
  time: number;
  /** 时间周期，秒 */
  duration: number;
  /** 收盘价 */
  close: number;
  /** 最高价 */
  high: number;
  /** 最低价 */
  low: number;
  /** 开盘价 */
  open: number;
  /** 成交量 */
  volume: number;
  /** 开盘持仓量 */
  openOi: number;
  /** 收盘持仓量 */
  closeOi: number;
}

export interface IKLineData {
  symbol: string;
  time: number;
  klines: IKLineItem[];
}
