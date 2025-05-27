<script setup lang="ts">
import type { IKLineData } from "./interface";
import {
  createChart,
  CandlestickSeries,
  type IChartApi,
  type ISeriesApi,
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
const fitContent = () => {
  if (!chart) return;
  chart.timeScale().fitContent();
};
defineExpose({
  getChart: () => chart,
  getKSeries: () => kSeries,
});
const resizeHandler = () => {
  if (!chart || !chartContainer.value) return;
  const dimensions = chartContainer.value.getBoundingClientRect();
  chart.resize(dimensions.width, dimensions.height);
};

watch(
  () => props.data,
  (newData: any) => {
    if (!kSeries) return;
    kSeries.setData(newData.klines);
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
