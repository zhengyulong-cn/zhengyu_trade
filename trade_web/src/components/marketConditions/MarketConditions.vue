<script setup lang="ts">
import { onMounted, ref } from "vue";
import KLineCenter from "@/components/klineChart/KLineCenter.vue";
import { getFutureDataApi } from "@/apis/modules";
import type { IKLineData } from "../klineChart/interface";
import { ElMessage } from "element-plus";

const loading = ref(false);

// 股票/期货代码选择的值
const selectedCode = ref("");
// 时间周期选择的值，默认设置为15分钟
const selectedTime = ref(15);

const codeOptions = ref([
  {
    value: "GFEX.lc2508",
    label: "碳酸锂 lc2508",
  },
  {
    value: "DCE.p2507",
    label: "棕榈油 p2507",
  },
  {
    value: "DCE.jd2507",
    label: "鸡蛋 jd2507",
  },
  {
    value: "SHFE.sp2507",
    label: "纸浆 sp2507",
  },
  {
    value: "CZCE.SH509",
    label: "烧碱 SH2509",
  },
  {
    value: "DCE.i2509",
    label: "铁矿石 i2509",
  },
  {
    value: "DCE.m2509",
    label: "豆粕 m2507",
  },
  {
    value: "CZCE.RM509",
    label: "菜粕 RM2509",
  },
]);
const timeOptions = ref([
  {
    value: 3,
    label: "3M",
  },
  {
    value: 15,
    label: "15M",
  },
  {
    value: 60,
    label: "1H",
  },
]);

const klinesData = ref<IKLineData>({
  symbol: "",
  time: 15,
  klines: [],
  segments: {
    A0: [],
    A1: [],
  },
});

const getKLineData = async (symbol: string, time: number) => {
  loading.value = true;
  getFutureDataApi({
    symbol: symbol,
    minutes: time,
  })
    .then((res) => {
      console.log(res);
      klinesData.value = res as IKLineData;
    })
    .catch((err) => {
      ElMessage.error(err);
    })
    .finally(() => {
      loading.value = false;
    });
};

const onSelectCode = (value: string) => {
  console.log("onSelectCode", value);
  getKLineData(value, selectedTime.value);
};

const onSelectTime = (value: number) => {
  console.log("onSelectTime", value);
  getKLineData(selectedCode.value, value);
};

onMounted(() => {
  getKLineData("GFEX.lc2508", 15);
});
</script>

<template>
  <div class="market-conditions-box">
    <header class="market-conditions-header">
      <el-select
        v-model="selectedCode"
        placeholder="请输入股票代码或期货代码"
        class="market-conditions-code-select"
        @change="onSelectCode"
      >
        <el-option
          v-for="item in codeOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
      <el-select
        v-model="selectedTime"
        placeholder="请选择时间周期"
        class="market-conditions-time-select"
        @change="onSelectTime"
      >
        <el-option
          v-for="item in timeOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
    </header>
    <section class="market-conditions-chart-container" v-loading="loading">
      <KLineCenter :data="klinesData" />
    </section>
  </div>
</template>

<style scoped lang="less">
.market-conditions-box {
  display: flex;
  flex-direction: column;
  background-color: white;
  height: calc(100% - 1rem);
  padding: 0.5rem;
  border-radius: 0.5rem;
  position: relative;
}
.market-conditions-header {
  display: flex;
  justify-content: flex-start;
  column-gap: 0.5rem;
  position: absolute;
  top: 0.5rem;
  left: 0.5rem;
  right: 0.5rem;
  border-radius: 0.5rem;
  opacity: 0.5;
  z-index: 999;
}
.market-conditions-code-select {
  max-width: 14rem;
}
.market-conditions-time-select {
  max-width: 10rem;
}
.market-conditions-chart-container {
  background-color: rgba(201, 12, 12, 0.2);
  height: 100%;
}
</style>
