<template>
    <div>
      <!-- 创建一个容器来放置图表 -->
      <div ref="chart" style="width: 100%; height: 600px;"></div>
      <!-- 添加一个按钮 -->
      <button @click="backToMainMap">返回主图</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import * as echarts from 'echarts';
  
  export default {
    data() {
      return {
        mapData: null
      };
    },
    created() {
      this.getData();
    },
    methods: {
      backToMainMap() {
          // 重新渲染初始地图
          this.renderMap();
      },
      getData() {
        axios.get('http://127.0.0.1:5000/region_map_data')
          .then(response => {
            this.mapData = response.data;
            this.renderMap();
          })
          .catch(error => {
            console.error('Error fetching map data:', error);
          });
      },
      renderMap() {
        const { city_count_dict, city_avg_salary_dict } = this.mapData;
        
        // 合并城市工作数量
        const mergedCityCount = {};
        for (const city in city_count_dict) {
          const firstLetter = city[0];
          if (!mergedCityCount[firstLetter]) {
            mergedCityCount[firstLetter] = city_count_dict[city];
          } else {
            mergedCityCount[firstLetter] += city_count_dict[city];
          }
        }
  
        // 合并平均薪资
        const mergedAvgSalary = {};
        for (const city in city_avg_salary_dict) {
          const firstLetter = city[0];
          if (!mergedAvgSalary[firstLetter]) {
            mergedAvgSalary[firstLetter] = city_avg_salary_dict[city];
          } else {
            mergedAvgSalary[firstLetter] += city_avg_salary_dict[city];
          }
        }
        
        // 计算网格的总面积
        const totalArea = Object.values(mergedCityCount).reduce((acc, cur) => acc + cur, 0);
  
        // 计算每个城市的面积占比
        const areaRatios = {};
        for (const city in mergedCityCount) {
          areaRatios[city] = mergedCityCount[city] / totalArea;
        }
  
        // 找出合并平均薪资的最大值和最小值
        const maxAvgSalary = Math.max(...Object.values(mergedAvgSalary));
        const minAvgSalary = Math.min(...Object.values(mergedAvgSalary));
        
        // 创建 ECharts 实例
        const chartDom = this.$refs.chart;
        const myChart = echarts.init(chartDom);
        
        // 配置项
        const option = {
          series: [
            {
              type: 'treemap',
              data: Object.keys(mergedCityCount).map(city => ({
                name: city,
                value: areaRatios[city],
                // 设置区域颜色深浅
                color: (() => {
                  // 计算颜色深浅程度
                  const colorRatio = (mergedAvgSalary[city[0]] - minAvgSalary) / (maxAvgSalary - minAvgSalary);
                  // 根据颜色深浅程度返回颜色
                  return echarts.color.modifyHSL('#4682B4', colorRatio * 100, 0);
                })()
              }))
            }
          ]
        };
        
        // 使用配置项绘制图表
        myChart.setOption(option);
  
        // 监听点击事件
        myChart.on('click', params => {
          // 获取点击的区域名字
          const clickedCityName = params.name;
          // 过滤出以该区域名字首字母开头的城市的平均工作数量和平均薪资数据
          const filteredData = {};
          for (const city in city_count_dict) {
            if (city.startsWith(clickedCityName)) {
              filteredData[city] = {
                count: city_count_dict[city],
                avgSalary: city_avg_salary_dict[city]
              };
            }
          }
          // 绘制新的网格图
          this.drawSubMap(filteredData);
        });
      },
  
      // 绘制新的网格图
      drawSubMap(data) {
        // 创建 ECharts 实例
        const chartDom = this.$refs.chart;
        const myChart = echarts.init(chartDom);
        
        // 配置项
        const option = {
          series: [
            {
              type: 'treemap',
              roamController: {
                  zoomOnMouseWheel: false // -> 禁止鼠标滚轮缩放 目前无效 需要修改 <-
              },
              data: Object.keys(data).map(city => ({
                name: city,
                value: data[city].count > 10000 ? data[city].count / 15 : data[city].count,
                // 设置区域颜色深浅
                color: echarts.color.modifyHSL('#4682B4', 0, 50 - (data[city].avgSalary - Math.min(...Object.values(data)))/(Math.max(...Object.values(data))-Math.min(...Object.values(data)))*50)
              }))
            }
          ]
        };
        
        // 使用配置项绘制图表
        myChart.setOption(option);
      }
    }
  };
  </script>
  
  <style>
  .button-container {
    text-align: center; /* 居中按钮 */
    margin-top: 10px; /* 控制按钮与图表之间的间距 */
  }
  </style>