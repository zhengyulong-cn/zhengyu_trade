<script setup lang="ts">
import type { IKLineData } from "./interface";
import {
  createChart,
  createSeriesMarkers,
  CandlestickSeries,
  type SeriesMarker,
  type IChartApi,
  type ISeriesApi,
  type ISeriesMarkersPluginApi,
} from "lightweight-charts";
import { onMounted, onUnmounted, ref, watch, type PropType } from "vue";
import { candlestickSeriesOptions, type ICommonChartOptions } from "./config";

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
  // // 时间刻度自适应
  kSeries = chart.addSeries(CandlestickSeries, candlestickSeriesOptions.value);
  kSeries.setData([]);
  seriesMarkers = createSeriesMarkers(kSeries, []);

  chart.timeScale().fitContent();
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
  window.removeEventListener("resize", resizeHandler);
});
const resizeHandler = () => {
  if (!chart || !chartContainer.value) return;
  const dimensions = chartContainer.value.getBoundingClientRect();
  chart.resize(dimensions.width, dimensions.height);
};

const getFenxingMarkerList = (fenxingList: any[]) => {
  const markers: SeriesMarker<any>[] = [];
  for (const item of fenxingList) {
    console.log(item);
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

watch(
  () => props.data,
  (newData: any) => {
    if (!kSeries) return;
    kSeries.setData(newData.klines);

    seriesMarkers?.setMarkers(getFenxingMarkerList(newData.fenxingList));
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
