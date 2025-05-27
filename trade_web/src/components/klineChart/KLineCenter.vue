<script setup lang="ts">
import { type PropType, ref } from "vue";
import { commonChartOptions } from "./config";
import KLineChart from "./KLineChart.vue";
import type { IChartApi, ISeriesApi } from "lightweight-charts";
import { type IKLineData } from "./interface";

const props = defineProps({
  data: {
    type: Object as PropType<IKLineData>,
    required: true,
  },
  autosize: {
    default: true,
    type: Boolean,
  },
});
const kLineChartRef = ref<{
  getChart: () => IChartApi;
  getKSeries: () => ISeriesApi<"Candlestick">;
} | null>(null);
</script>

<template>
  <div class="klineCentre">
    <KLineChart
      ref="kLineChartRef"
      :data="props.data"
      autosize
      :common-chart-options="commonChartOptions"
    />
  </div>
</template>

<style lang="less" scoped>
.klineCentre {
  height: 100%;
}
</style>
