<template>  
    <!-- 创建一个容器来放置图表和按钮 -->    
    <div id="map-chart">  
      <!-- 地图容器 -->  
      <div class="map">  
        <div ref="chart" class="chart-map"></div>  
        <!-- 添加一个按钮，位于地图正下方 -->  
        <el-button class="renderbutton" type="primary" @click="backToPreviousMap">返回</el-button>  
      </div>  
      <!-- 折线图容器，位于地图右侧 -->  
      <div ref="lineChart" class="chart-line"></div>  
    </div>
</template>    
  
<script>  
import axios from 'axios';  
import * as echarts from 'echarts';  
import { EventBus } from './eventBus.js';
  
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
      this.currentChart = echarts.init(chartDom, 'dark');  
      this.currentChart.on('click', params => {  
        // 获取点击的区域名字  
        const clickedCityName = params.name;
        sessionStorage.setItem('lastClickedCity', clickedCityName);
        EventBus.$emit('value-fresh', clickedCityName); 
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
      //如果需要，可以清除localStorage中的lastClickedCity  
      localStorage.removeItem('lastClickedCity'); 
      this.subChartOptionsStack.pop();
      if (this.subChartOptionsStack.length > 0) {

        const prevOption = this.subChartOptionsStack.pop(); // 直接弹出顶部配置项  
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
          this.initLineChart(); // 初始化折线图
        })  
        .catch(error => {  
          console.error('Error fetching map data:', error);  
        });  
    },

    //条形图绘制代码
    initLineChart() {  
      const lineChartDom = this.$refs.lineChart;  
      const lineChartInstance = echarts.init(lineChartDom);  
        
      // 使用mapData中的city_avg_salary_dict来配置折线图  
      const option = {
        tooltip: {
          trigger: 'axis',
          position: function (pt) {
            return [pt[0], '10%'];
          }
        },
        xAxis: {
          name: 'city',
          type: 'category',
          boundaryGap: false,
          data: Object.keys(this.mapData.city_avg_salary_dict) // 城市代号作为横坐标
        },
        yAxis: {
          name: 'salary',
          type: 'value',
          boundaryGap: [0, '100%']
        },
        dataZoom: [
          {
            type: 'inside',
            start: 0,
            end: 10
          },
          {
            start: 0,
            end: 10
          }
        ],
        series: [
          {
            name: 'Average Salary',
            type: 'line',
            symbol: 'none',
            sampling: 'lttb',
            itemStyle: {
              color: 'rgb(255, 70, 131)'
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgb(255, 158, 68)'
                },
                {
                  offset: 1,
                  color: 'rgb(255, 70, 131)'
                }
              ])
            },
            data: Object.values(this.mapData.city_avg_salary_dict), // 薪水作为纵坐标
          }
        ]
      }; 
      lineChartInstance.setOption(option);  
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
        this.currentChart = echarts.init(chartDom, 'dark');  
      }
      // 配置项
      const option = {
        backgroundColor: 'transparent', // 设置背景颜色为透明
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
              })(),
              emphasis: {  
              // 当鼠标悬停时，可以改变颜色、边框等视觉效果  
              itemStyle: {  
                // 例如，改变边框宽度或颜色  
                borderWidth: 2, // 可以根据需要调整  
                borderColor: 'rgba(0,0,0,0.5)', // 可以设置更明显的颜色  
                // 如果需要模拟放大效果，可以尝试改变阴影  
                shadowBlur: 10, // 阴影大小  
                shadowColor: 'rgba(0, 0, 0, 0.5)' // 阴影颜色  
               }  
             }
            }))
          }
        ]
      };

      // 保存主地图的配置项  
      this.mainChartOptions = option;  
  
      // 初始化或更新图表  
      if (!this.currentChart) {  
        const chartDom = this.$refs.chart;  
        this.currentChart = echarts.init(chartDom, 'dark');  
      }  
      this.currentChart.setOption(option);  
    },  
    drawSubMap(data, isUserInteraction = false) {  
      // 设置动画持续时间和其他动画参数  
      const animationOpts = {  
        animationDuration: 1000, // 设置动画持续时间为1000毫秒  
        animationEasing: 'quarticInOut' // 设置缓动函数  
      };  
      // 配置项  
      const option = {
        backgroundColor: (0,0,0,0), // 设置背景颜色为透明
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
              color: echarts.color.modifyHSL('#4682B4', 0, 50 - (data[city].avgSalary - Math.min(...Object.values(data)))
              /(Math.max(...Object.values(data))-Math.min(...Object.values(data)))*50),
              emphasis: {  
                // 当鼠标悬停时，可以改变颜色、边框等视觉效果  
                itemStyle: {  
                  // 例如，改变边框宽度或颜色  
                  borderWidth: 2, // 可以根据需要调整  
                  borderColor: 'rgba(0,0,0,0.5)', // 可以设置更明显的颜色  
                  // 如果需要模拟放大效果，可以尝试改变阴影  
                  shadowBlur: 10, // 阴影大小  
                  shadowColor: 'rgba(0, 0, 0, 0.5)' // 阴影颜色  
                }  
              }
            }))
          }
        ]  
      };  
      // 如果当前是用户交互（如点击事件），则推入堆栈  
      if (isUserInteraction) {  
        this.subChartOptionsStack.push(option); 
      }   
        
      // 使用配置项绘制图表  
      this.currentChart.setOption(option,animationOpts);  
    },

    isDifferentOption(option1, option2) {  
      // 这是一个简单的比较函数，用于检查两个配置项是否不同。  
      return JSON.stringify(option1) !== JSON.stringify(option2);  
    }  
  }  
};  
</script>

<style>
#map-chart {
  display: flex;
    width: 100%;
    height: 100%;
    padding: 20px; /* 内边距，可根据需要调整 */
    box-sizing: border-box; /* 使得padding不会影响整体尺寸 */
    flex-direction: row;
}

#map-chart .map {
    display: flex;
    width: 50%;
    height: 100%;
    flex-direction: column;
    margin-right: 10px;
    align-items: center;
}

#map-chart .chart-map {
    display: flex;
    width: 100%;
    height: 100%;

}
#map-chart .renderbutton {
  display: flex;
  width: 17%;
  height: 12%;
}

#map-chart .chart-line {
  display: flex;
  width: 50%;
  height: 100%;
}

</style>
