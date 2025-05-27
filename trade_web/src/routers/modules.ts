import type { RouteRecordRaw } from "vue-router";

export const RouterModules: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/market_quotes",
  },
  {
    path: "/market_quotes",
    name: "MarketQuotes",
    component: () => import("@/pages/MarketQuotesPage.vue"),
    meta: {
      icon: "TrendCharts",
      title: "市场行情",
    },
  },
  {
    path: "/futures",
    name: "Futures",
    meta: {
      icon: "Platform",
      title: "期货",
    },
    children: [
      {
        path: "/futures/monitor",
        component: () => import("@/pages/futures/MonitorPage.vue"),
        meta: {
          icon: "",
          title: "机会监控",
        },
      },
      {
        path: "/futures/open_calc",
        component: () => import("@/pages/futures/OpenCalcPage.vue"),
        meta: {
          icon: "",
          title: "开仓计算",
        },
      },
      // 交易所保证金
    ],
  },
];
