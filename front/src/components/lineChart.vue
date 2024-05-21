<template>
    <div id="line-chart">
        <div ref="chart" class="lineChart"></div>
    </div>
</template>
  
  <script>
  import * as echarts from 'echarts';
  import axios from 'axios';
  import { EventBus } from './eventBus';
  
  export default {
    name: 'BumpChart',
    data() {
      return {
        myChart: null,
        job1_line: [0, 1, 2, 1, 2],
        job2_line: [2, 0, 2, 2, 0],
        job3_line: [0, 2, 0, 1, 0]
      };
    },
    mounted() {
      this.myChart = echarts.init(this.$refs.chart);
      this.initChart();
      EventBus.$on('line-job', (data) => {
        this.sendDataToBackend(data),
        this.initChart()
      });
    },
    methods: {
      sendDataToBackend(data) {
        axios.post('http://127.0.0.1:5000/job_line', {
            job1: data[0],
            job2: data[1],
            job3: data[2]
        })
          .then(response => {
            this.job1_line = response.data.job1_pre.flat(),
            this.job2_line = response.data.job2_pre.flat(),
            this.job3_line = response.data.job3_pre.flat(),
            this.initChart()
          })
          .catch(error => {
            console.error('Error sending data to backend:', error);
          });
      },
      initChart() {
        const option = {
          tooltip: {
            trigger: 'item'
          },
          grid: {
            left: 30,
            right: 110,
            bottom: 30,
            containLabel: true
          },
          xAxis: {
            type: 'category',
            splitLine: {
              show: true
            },
            axisLabel: {
              margin: 30,
              fontSize: 16
            },
            boundaryGap: false,
            data: ['0', '0.2', '0.4', '0.6', '0.8']
          },
          yAxis: {
            type: 'value',
            axisLabel: {
              margin: 30,
              fontSize: 16,
            },
            inverse: false,
            interval: 1,
            min: 0,
            max: 3
          },
          series: [
            {
              name: 'postion1',
              symbolSize: 20,
              type: 'line',
              smooth: true,
              emphasis: {
                focus: 'series'
              },
              endLabel: {
                show: true,
                formatter: '{a}',
                distance: 20
              },
              lineStyle: {
                width: 4
              },
              data: this.job1_line
            },
            {
              name: 'postion2',
              symbolSize: 20,
              type: 'line',
              smooth: true,
              emphasis: {
                focus: 'series'
              },
              endLabel: {
                show: true,
                formatter: '{a}',
                distance: 20
              },
              lineStyle: {
                width: 4
              },
              data: this.job2_line
            },
            {
              name: 'postion3',
              symbolSize: 20,
              type: 'line',
              smooth: true,
              emphasis: {
                focus: 'series'
              },
              endLabel: {
                show: true,
                formatter: '{a}',
                distance: 20
              },
              lineStyle: {
                width: 4
              },
              data: this.job3_line
            },
          ]
        };
        this.myChart.setOption(option);
      }
    }
  };
  </script>
  
  <style>

  #line-chart{
      width: 100%;
      height: 100%;
  }
    
    
  #line-chart .lineChart {
      width: 100%;
      height: 100%;
  }
  
  </style>
  