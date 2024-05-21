<template>
    <div ref="chart"></div>
  </template>
  
  <script>
  import * as echarts from 'echarts';
  import { EventBus } from './eventBus.js';
  
  export default {
    name: 'GaugeChart',
    data() {
      return {
        chart: null,
        gaugeData: [
          {
            value: 40,
            name: '',
            title: {
              offsetCenter: ['0%', '-30%']
            },
            detail: {
              valueAnimation: false,
              offsetCenter: ['0%', '-20%']
            }
          },
          {
            value: 50,
            name: '',
            title: {
              offsetCenter: ['0%', '0%']
            },
            detail: {
              valueAnimation: false,
              offsetCenter: ['0%', '10%']
            }
          },
          {
            value: 60,
            name: '',
            title: {
              offsetCenter: ['0%', '30%']
            },
            detail: {
              valueAnimation: false,
              offsetCenter: ['0%', '40%']
            }
          }
        ]
      };
    },
    mounted() {
      this.initChart();
      EventBus.$on('top-jobs', (data) => {
        this.updateGaugeData(data.score, data.job);
      });
    },
    methods: {
      initChart() {
        this.chart = echarts.init(this.$refs.chart);
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: (params) => {
              const dataIndex = params.dataIndex;
              return `${this.gaugeData[dataIndex].name}: ${params.value}%`;
            }
          },
          series: [
            {
              type: 'gauge',
              startAngle: 90,
              endAngle: -270,
              pointer: {
                show: false
              },
              progress: {
                show: true,
                overlap: false,
                roundCap: true,
                clip: false,
                itemStyle: {
                  borderWidth: 1,
                  borderColor: '#464646'
                }
              },
              axisLine: {
                lineStyle: {
                  width: 40
                }
              },
              splitLine: {
                show: false,
                distance: 0,
                length: 10
              },
              axisTick: {
                show: false
              },
              axisLabel: {
                show: false,
                distance: 50
              },
              data: this.gaugeData,
              title: {
                show: false
              },
              detail: {
                show: false
              }
            }
          ]
        };
        this.chart.setOption(option);
      },
      updateGaugeData(scores, jobs) {
        this.gaugeData.forEach((item, index) => {
          item.value = (scores[index] * 100).toFixed(2); // 将值转化为百分比形式
          item.name = jobs[index]; // 更新职位名称
        });
        this.chart.setOption({
          series: [
            {
              data: this.gaugeData
            }
          ]
        });
      }
    }
  };
  </script>
  
  