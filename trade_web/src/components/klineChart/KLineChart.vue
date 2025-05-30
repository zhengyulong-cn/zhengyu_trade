<script setup lang="ts">
import type { IKLineData } from "./interface";
import {
  createChart,
  CandlestickSeries,
  type IChartApi,
  type ISeriesApi,
  LineSeries,
  LineStyle,
} from "lightweight-charts";
import { onMounted, onUnmounted, ref, watch, type PropType } from "vue";
import {
  candlestickSeriesOptions,
  lineSeriesOptions,
  type ICommonChartOptions,
} from "./config";
import { getSegmentsLine } from "./utils";

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
let a0lineSerise: ISeriesApi<"Line"> | null = null;
let lastA0LineSerise: ISeriesApi<"Line"> | null = null;
let a1lineSerise: ISeriesApi<"Line"> | null = null;
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
  a0lineSerise = chart.addSeries(LineSeries, lineSeriesOptions.value);
  a0lineSerise.setData([]);
  lastA0LineSerise = chart.addSeries(LineSeries, {
    ...lineSeriesOptions.value,
    lineStyle: LineStyle.Dashed,
  });
  lastA0LineSerise.setData([]);
  a1lineSerise = chart.addSeries(LineSeries, {
    ...lineSeriesOptions.value,
    color: "orange",
  });
  a1lineSerise.setData([]);

  chart.timeScale().fitContent();
  // chart.subscribeCrosshairMove((param) => {
  //   const series = param.seriesData.get(kSeries);
  //   if (!series) return;
  // });
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
  if (a0lineSerise) {
    a0lineSerise = null;
  }
  if (lastA0LineSerise) {
    a0lineSerise = null;
  }
  if (a1lineSerise) {
    a1lineSerise = null;
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
  (newData: IKLineData) => {
    if (!kSeries || !a0lineSerise || !lastA0LineSerise || !a1lineSerise) return;
    kSeries.setData(newData.klines);

    const a0LineData = getSegmentsLine(newData.segments.A0).slice(
      0,
      newData.segments.A0.length - 1
    );
    a0lineSerise.setData(a0LineData);

    const lastLineData = getSegmentsLine(newData.segments.A0).slice(
      newData.segments.A0.length - 2
    );
    lastA0LineSerise.setData(lastLineData);

    const a1LineData = getSegmentsLine(newData.segments.A1);
    a1lineSerise.setData(a1LineData);
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
