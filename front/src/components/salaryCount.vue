<template>  
    <div ref="chartContainer" style="width: 1000px; height: 1000px;"></div>  
  </template>  
    
  <script>  
  import * as echarts from 'echarts';  
  import axios from 'axios'; 
  import { EventBus } from './eventBus.js';
    
  export default {  
    name: 'salaryCountComponent',  
    data() {  
      return {  
        fieldData: null, // 用于存储从API获取的数据
        lastFieldName: ''
      };  
    },  
    methods: {  
      getData() {  
        axios.get('http://127.0.0.1:5000/field_map_data')  
          .then(response => {  
            this.fieldData = response.data;  
            this.updateChart(); // 数据获取后更新图表  
          })  
          .catch(error => {  
            console.error('Error fetching field map data:', error);  
          });  
      },  
      updateChart() {  
        if (!this.fieldData) return;    
        // 准备数据点  
        const dataPoints = [];  
        for (let field in this.fieldData.field_avg_salary_dict) {  
          if (this.fieldData.field_count_dict[field]) {  
            dataPoints.push({  
              name: field, // 行业名称  
              value: [  
                this.fieldData.field_avg_salary_dict[field] - 10000, // 薪资减去9000作为X轴数据  
                this.fieldData.field_count_dict[field] - 10000 // 岗位数量减去1000作为Y轴数据  
              ]  
            });  
          }  
        }  
    
        // 定义图表配置  
        const option = {   
          xAxis: {  
            name: '岗位数量',  
            type: 'value',
            min: -10000, // 设置X轴最小值  
            max: 10000,
            axisTick:{
                show: false,
            },
            splitLine: { show: false }
          },  
          yAxis: {  
            name: '薪资水平',  
            type: 'value',
            axisTick:{
                show: false,
            },
            min: -10000, // 设置Y轴最小值  
            max: 13000,
            splitLine: { show: false }
          },
          // 添加名称显示到tooltip中  
          tooltip: { 
                trigger: 'item',
                formatter: function (params) {  
                  return `行业名称: ${params.name}<br/>实际岗位数量: ${params.value[1] + 10000}<br/>实际薪资水平: ${params.value[0] + 10000}`;  
                }  
              },
          series: [  
            {  
              type: 'scatter',  
              symbolSize: 10,  
              data: dataPoints, // 使用准备好的数据点
              itemStyle: {  
            color: function(params) {  
                // 如果数据点的名称与lastFieldName相匹配，则颜色为黄色  
                if (params.name === this.lastFieldName) {  
                return 'yellow';  
                }  
                // 否则，返回初始颜色（例如：蓝色）  
                return 'blue';  
                }.bind(this) // 绑定当前Vue实例的this上下文  
            },    
            },  
          ],  
        };  
    
        // 设置图表配置  
        this.myChart.setOption(option);  
      },  
    },  
    mounted() {  
        // 获取图表容器DOM元素  
        const chartDom = this.$refs.chartContainer;  
            // 初始化ECharts实例  
        this.myChart = echarts.init(chartDom);  
        // 获取数据 
        EventBus.$on('value-updated', (newValue) => {
            this.lastFieldName = newValue,
            this.updateChart()
        });
        this.getData();  
        },  
    };  
  </script>