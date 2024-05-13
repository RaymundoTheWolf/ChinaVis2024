<template>  
  <div>  
    <!-- 创建一个容器来放置图表 -->  
    <div ref="chart" style="width: 100%; height: 600px;"></div>  
    <!-- 添加一个按钮 -->  
    <button @click="backToPreviousMap">返回上一级</button>  
  </div>  
</template>  
  
<script>  
import axios from 'axios';  
import * as echarts from 'echarts';  
  
export default {  
  data() {  
    return {  
      mapData: null,  
      chartOptionsStack: [], // 用于存储主地图的配置项  
      subChartOptionsStack: [], // 用于存储用户交互产生的子图配置项  
      currentChart: null // 当前图表的实例  
    };  
  },  
  mounted() {  
    this.getData();  
    this.initChart();  
  },   
  methods: {
    initChart() {  
      const chartDom = this.$refs.chart;  
      this.currentChart = echarts.init(chartDom);  
      this.currentChart.on('click', params => {  
        // 获取点击的区域名字  
        const clickedCityName = params.name;  
        // 过滤出以该区域名字首字母开头的城市的平均工作数量和平均薪资数据  
        const filteredData = {};  
        for (const city in this.mapData.city_count_dict) {  
          if (city.startsWith(clickedCityName)) {  
            filteredData[city] = {  
              count: this.mapData.city_count_dict[city],  
              avgSalary: this.mapData.city_avg_salary_dict[city]  
            };  
          }  
        }  
        // 绘制新的网格图  
        this.drawSubMap(filteredData, true);  
      });  
    }, 
    backToPreviousMap() {  
      // 如果子地图配置堆栈中有元素，则弹出并渲染  
      if (this.subChartOptionsStack.length > 0) {  
        const prevOption = this.subChartOptionsStack.pop();  
        this.currentChart.setOption(prevOption);  
      } else if (this.mainChartOptions) {  
        // 如果没有子地图配置，但主地图配置存在，则返回主地图  
        this.currentChart.setOption(this.mainChartOptions);  
      }  
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
  
      // 创建 ECharts 实例（只在首次调用时）  
      if (!this.currentChart) {  
        const chartDom = this.$refs.chart;  
        this.currentChart = echarts.init(chartDom);  
      }

      // 配置项
      const option = {
        series: [
          {
            type: 'treemap',
            breadcrumb: { show: false},
            roam: false, //是否开启拖拽漫游（移动和缩放）
            nodeClick: false, //点击节点后的行为,false无反应
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

      // 保存主地图的配置项  
      this.mainChartOptions = option;  
  
      // 初始化或更新图表  
      if (!this.currentChart) {  
        const chartDom = this.$refs.chart;  
        this.currentChart = echarts.init(chartDom);  
      }  
      this.currentChart.setOption(option);  
    },  
    drawSubMap(data, isUserInteraction = false) {  
      // 配置项  
      const option = {  
        series: [
          {
            type: 'treemap',
            breadcrumb: { show: false},
            roamController: {
                zoomOnMouseWheel: false // 禁止鼠标滚轮缩放
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
      // 如果当前是用户交互（如点击事件），则推入堆栈  
      if (isUserInteraction) {  
        this.subChartOptionsStack.push(option);  
      }   
        
      // 使用配置项绘制图表  
      this.currentChart.setOption(option);  
    },

    isDifferentOption(option1, option2) {  
      // 这是一个简单的比较函数，用于检查两个配置项是否不同。  
      return JSON.stringify(option1) !== JSON.stringify(option2);  
    }  
  }  
};  
</script>  
  
<style>  
.button-container {  
  text-align: center;  
  margin-top: 10px;  
}  
</style>
