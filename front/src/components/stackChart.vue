<template>
  <div id="stack-chart">
    <div id="stackmain" style="width: 100%; height: 100%;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
import { EventBus } from './eventBus';

export default {
  created() {
    EventBus.$on('fresh-data', this.freshData);
  },
  data() {
    return {
      stackData: null,
      processedData: null,
      categories: [], // 行业类别
      legendData: [], // 图例数据
      seriesData: [], // 系列数据
      chartWidth: '100%' // 图表宽度
    };
  },
  mounted() {
    this.getData();
    this.handleResize();
    window.addEventListener('resize', this.handleResize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
    EventBus.$off('fresh-data', this.freshData);
  },
  methods: {
    handleResize() {
      // 当窗口大小改变时重新渲染图表
      this.renderStackChart();
    },
    getData() {
      axios.get('http://127.0.0.1:5000/stack_data')
        .then(response => {
          this.stackData = response.data.stack_dict; // 注意这里的 key
          this.processData();
        })
        .catch(error => {
          console.error('Error fetching stack data', error);
        });
    },
    processData() {
      this.processedData = Object.keys(this.stackData).map(companyType => [
        companyType,
        this.stackData[companyType][1], // 工资
        this.stackData[companyType][0]  // 公司名
      ]);

      // 提取所有行业类别
      this.categories = [...new Set(this.processedData.map(item => item[0]))];

      const legendData = [];
      const seriesData = [];
      const colors = [
        ['rgb(128, 255, 165)', 'rgb(1, 191, 236)'],
        ['rgb(0, 221, 255)', 'rgb(77, 119, 255)'],
        ['rgb(55, 162, 255)', 'rgb(116, 21, 219)'],
        ['rgb(255, 0, 135)', 'rgb(135, 0, 157)'],
        ['rgb(255, 191, 0)', 'rgb(224, 62, 76)']
      ];

      let colorIndex = 0;
      for (const [companyType, salary, companyName] of this.processedData) {
        legendData.push(companyName); // 将公司名作为图例
        const data = this.categories.map(category => (category === companyType ? salary : 0)); // 根据行业类别分配工资数据
        seriesData.push({
          name: companyName, // 将公司名作为系列名称
          type: 'line',
          stack: '总量',
          smooth: true,
          lineStyle: {
            width: 0
          },
          showSymbol: false,
          areaStyle: {
            opacity: 0.8,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: colors[colorIndex][0]
              },
              {
                offset: 1,
                color: colors[colorIndex][1]
              }
            ])
          },
          emphasis: {
            focus: 'series'
          },
          data: data // 按行业类别分配数据
        });
        colorIndex = (colorIndex + 1) % colors.length;
      }

      this.legendData = legendData;
      this.seriesData = seriesData;
      this.renderStackChart();
    },
    renderStackChart() {
      const chartDom = document.getElementById('stackmain');
      const myChart = echarts.init(chartDom);

      let option = {
        color: ['#80FFA5', '#00DDFF', '#37A2FF', '#FF0087', '#FFBF00'],
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          },
          formatter: function (params) {
            let content = '';
            params.forEach(function (item) {
              if (item.value !== 0) {
                content += item.seriesName + ': ' + item.value + '<br/>';
              }
            });
            return content;
          }
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '10%', // 调整grid的bottom以给dataZoom留出空间
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            data: this.categories, // 使用所有行业类别作为x轴数据
            axisLabel: {
              rotate: 45, // 旋转角度
              margin: 20 // 调整x轴标签的高度
            }
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: this.seriesData,
        dataZoom: [ // 添加拖动条，调整位置
          {
            type: 'slider',
            show: true,
            xAxisIndex: [0],
            start: 0,
            end: 100,
            bottom: '5%' // 调整拖动条位置
          }
        ]
      };

      myChart.setOption(option);
    },
    freshData(newCity) {
      axios.post('http://127.0.0.1:5000/stack_data', { city: newCity })
        .then(response => {
          this.stackData = response.data.stack_dict; // 注意这里的 key
          this.processData();
        })
        .catch(error => {
          console.error('Error sending stack data:', error);
        });
    }
  }
};
</script>

<style scoped>
#stack-chart {
  width: 100%;
  height: 100%;
}
</style>
