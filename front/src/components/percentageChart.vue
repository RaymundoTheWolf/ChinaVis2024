<template>
  <div ref="chartRef"></div>
</template>
  
<script>
import * as echarts from 'echarts';
import { EventBus } from './eventBus';

export default {
  name: 'EChartComponent',
  data() {
    return {
      myChart: null,
      bodyMax: 150,
      bodyPercentage: 20,
      salary: 0,
      symbols: [
        'path://M1867 -4989 c-509 49 -948 401 -1112 893 -52 153 -69 280 -62 461 10 271 92 508 250 724 98 134 275 290 409 361 32 17 58 33 58 36 0 5 -693 1208 -1100 1909 -316 545 -310 534 -310 571 l0 34 2000 0 2000 0 0 -33 c0 -26 -155 -302 -701 -1248 -386 -668 -703 -1219 -706 -1226 -2 -6 22 -25 54 -42 92 -49 223 -152 308 -243 152 -161 260 -357 317 -578 40 -151 49 -361 24 -520 -64 -405 -319 -761 -680 -951 -167 -88 -313 -131 -501 -149 -121 -11 -122 -11 -248 1z'
      ],
      labelSetting: {
        show: true,
        position: 'top',
        offset: [0, -20],
        formatter: function (param) {
          const value = param.value;
          if (value === 150 * 0.2) {
            return '20%';
          } else if (value === 150 * 0.4) {
            return '40%';
          } else if (value === 150 * 0.6) {
            return '60%';
          } else if (value === 150 * 0.8) {
            return '80%';
          } else if (value === 150 * 1.0) {
            return '100%';
          } else {
            return '';
          }
        },
        fontSize: 18,
        fontFamily: 'Arial',
      },
      markLineSetting: {
        symbol: 'none',
        lineStyle: {
          opacity: 0.3
        },
      }
    };
  },

  mounted() {
    this.initChart();
  },
  created() {
    EventBus.$on('salary', (newValue) => {
      this.salary = newValue
      this.updateChartOption(newValue)
    })
  },
  beforeDestroy(){
    EventBus.$off('salary', this.salary);
  },
  methods: {
    initChart() {
      const chartDom = this.$refs.chartRef;
      this.myChart = echarts.init(chartDom);
      this.myChart.setOption(this.getOption());
    },
    // 更新图表的配置项时，可以调用这个方法来重新渲染图表
    updateChartOption(params) {
      const option = this.getOption(params);
      this.myChart.setOption(option);
    },
    getLocalStorageData(params) {
      const value = params
      if (value >= 0 && value < 5000) {
        return 0.2;
      } else if (value >= 5000 && value < 6500) {
        return 0.4;
      } else if (value >= 6500 && value < 8500) {
        return 0.6;
      } else if (value >= 8500 && value < 12500) {
        return 0.8;
      } else if (value >= 12500 && value <= 255000) {
        return 1;
      } else {
        return 0.6;
      }
    },
    getOption(params) {
      return {
        tooltip: false,
        xAxis: {
          data: ['a'],
          axisTick: { show: false },
          axisLine: { show: false },
          axisLabel: { show: false }
        },
        yAxis: {
          splitLine: { show: false },
          axisTick: { show: false },
          axisLine: { show: false },
          axisLabel: { show: false }
        },

        series: [
          {
            name: 'typeA',
            type: 'pictorialBar',
            symbolClip: true,
            symbolBoundingData: this.bodyMax,
            label: this.salary,
            data: [
              {
                value: 150 * this.getLocalStorageData(params),
                symbol: this.symbols[0]
              },
            ],
            markLine: this.markLineSetting,
            z: 10
          },
          {
            name: 'full',
            type: 'pictorialBar',
            symbolBoundingData: this.bodyMax,
            animationDuration: 0,
            itemStyle: {
              color: '#ccc'
            },
            data: [
              {
                value: 150,
                symbol: this.symbols[0]
              }
            ]
          }
        ]
      };
    },
    makeChart() {
      const chartDom = this.$refs.chartRef;
      this.myChart = echarts.init(chartDom);
    }
  },
};
</script>
