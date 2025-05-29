<script setup lang="ts">
import type { IKLineData } from "./interface";
import {
  createChart,
  createSeriesMarkers,
  CandlestickSeries,
  type IChartApi,
  type ISeriesApi,
  type ISeriesMarkersPluginApi,
  LineSeries,
  LineStyle,
} from "lightweight-charts";
import { onMounted, onUnmounted, ref, watch, type PropType } from "vue";
import {
  candlestickSeriesOptions,
  lineSeriesOptions,
  type ICommonChartOptions,
} from "./config";
import {
  getFenxingMarkerList,
  getSegmentsLine,
  getLastSegmentLine,
} from "./utils";

const props = defineProps({
  data: {
    type: Object as PropType<IKLineData>,
    required: true,
  },
  autosize: {
    default: true,
    type: Boolean,
  },
  commonChartOptions: {
    type: Object as PropType<ICommonChartOptions>,
    required: true,
  },
});

const chartContainer = ref();
let chart: IChartApi | null = null;
let kSeries: ISeriesApi<"Candlestick"> | null = null;
let lineSerise: ISeriesApi<"Line"> | null = null;
let lastLineSerise: ISeriesApi<"Line"> | null = null;
let seriesMarkers: ISeriesMarkersPluginApi<any> | null = null;
onMounted(() => {
  chart = createChart(chartContainer.value, {
    ...props.commonChartOptions,
  });
  // 隐藏K线图的时间刻度
  // chart.applyOptions({
  //   timeScale: {
  //     visible: false,
  //   },
  // });
  kSeries = chart.addSeries(CandlestickSeries, candlestickSeriesOptions.value);
  kSeries.setData([]);
  lineSerise = chart.addSeries(LineSeries, lineSeriesOptions.value);
  lineSerise.setData([]);
  lastLineSerise = chart.addSeries(LineSeries, {
    ...lineSeriesOptions.value,
    lineStyle: LineStyle.Dashed,
  });
  lastLineSerise.setData([]);

  seriesMarkers = createSeriesMarkers(kSeries, []);

  chart.timeScale().fitContent();
  chart.subscribeCrosshairMove((param) => {
    const series = param.seriesData.get(kSeries);
    if (!series) return;
    console.table(series);
  });
  if (props.autosize) {
    window.addEventListener("resize", resizeHandler);
  }
});
onUnmounted(() => {
  if (chart) {
    chart.remove();
    chart = null;
  }
  if (kSeries) {
    kSeries = null;
  }
  if (lineSerise) {
    lineSerise = null;
  }
  window.removeEventListener("resize", resizeHandler);
});
const resizeHandler = () => {
  if (!chart || !chartContainer.value) return;
  const dimensions = chartContainer.value.getBoundingClientRect();
  chart.resize(dimensions.width, dimensions.height);
};

watch(
  () => props.data,
  (newData: any) => {
    if (!kSeries || !lineSerise || !lastLineSerise) return;
    kSeries.setData(newData.klines);
    console.log(newData.segments);

    const newLineData = getSegmentsLine(newData.segments);
    lineSerise.setData(newLineData);

    const lastLineData = getLastSegmentLine(newData.segments);
    lastLineSerise.setData(lastLineData);

    // seriesMarkers?.setMarkers(getFenxingMarkerList(newData.fenxingList));
  }
);
watch(
  () => props.autosize,
  (enabled) => {
    if (!enabled) {
      window.removeEventListener("resize", resizeHandler);
      return;
    }
    window.addEventListener("resize", resizeHandler);
  }
);
watch(
  () => props.commonChartOptions,
  (newOptions) => {
    if (!chart) return;
    chart.applyOptions(newOptions);
  }
);
</script>

<template>
  <div class="lw-chart" ref="chartContainer"></div>
</template>

<style lang="less" scoped>
.lw-chart {
  height: 100%;
  position: relative;
}
</style>
