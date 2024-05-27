<template>
	<div id="scatter-chart">
	  <div id="scattermain" style="width: 100%; height: 100%;"></div>
	</div>
  </template>
  
  <script>
  import * as echarts from 'echarts';
  import axios from 'axios';
  import { EventBus } from './eventBus';
  
  export default {
	created(){
		EventBus.$on('fresh-data', (newValue) => {
        this.freshData(newValue)
      });
	},
	data() {
	  return {
		scatterData: null,
		processed_data: null
	  };
	},
	mounted() {
	  this.getData();
	},
	methods: {
	  getData() {
		axios.get('http://127.0.0.1:5000/3d_scatter_data')
		  .then(response => {
			this.scatterData = response.data.job_dict;
			this.renderScatterChart();
		  })
		  .catch(error => {
			console.error('获取散点图数据时出错:', error);
		  });
	  },
	  renderScatterChart() {
		if (this.scatterData) {
		  this.processed_data = Object.entries(this.scatterData).map(([jobTitle, item]) => ({
			jobTitle,
			salary: item[0],
			company: item[1],
			region: item[2][0],
			experience: item[2][1],
			education: item[2][2]
		  }));
		  this.setOption();
		}
	  },
	  freshData(new_type){
		axios.post('http://127.0.0.1:5000/3d_scatter_data',{
				field : new_type
                })
                .then(response => {
					this.scatterData = response.data.job_dict;
					this.renderScatterChart();
                })
                .catch(error => {
                    console.error('Error sending scatter data:', error);
                });
	  },
	  setOption() {
		const chartDom = document.getElementById('scattermain');
		const myChart = echarts.init(chartDom);
  
		// 计算工资的最小值和最大值
		const salaries = this.processed_data.map(item => item.salary);
		const minSalary = Math.min(...salaries);
		const maxSalary = Math.max(...salaries);
  
		// 设置点大小的最小值和最大值
		const minSymbolSize = 10;
		const maxSymbolSize = 40;
  
		const option = {
		  tooltip: {
			formatter: (params) => {
			  const { data } = params;
			  const formatNumber = (num) => Number(num).toFixed(3);
			  return `职业: ${data[4]}<br>公司: ${data[5]}<br>工资: ${formatNumber(data[3])}<br>地区评分: ${formatNumber(data[0])}<br>经验评分: ${formatNumber(data[1])}<br>学历评分: ${formatNumber(data[2])}`;
			}
		  },
		  visualMap: {
			calculable: true,
			dimension: 3,
			max: maxSalary,
			inRange: {
			  symbolSize: [minSymbolSize, maxSymbolSize],
			  color:['#ff5c41', '#44ff40', '#00a6ff']
			},
			textStyle: {
			  color: '#fff'
			}
		  },
		  xAxis3D: {
			name: '地区评分',
			type: 'value',
			min: 0,
			max: 0.6,
			interval: 0.1 // 调整间隔，使得点更分散
		  },
		  yAxis3D: {
			name: '经验评分',
			type: 'value',
			min: 0,
			max: 0.6,
			interval: 0.1 // 调整间隔，使得点更分散
		  },
		  zAxis3D: {
			name: '学历评分',
			type: 'value',
			min: 0,
			max: 0.6,
			interval: 0.1 // 调整间隔，使得点更分散
		  },
		  grid3D: {
			axisLine: {
			  lineStyle: {
				color: '#fff'
			  }
			},
			axisPointer: {
			  lineStyle: {
				color: '#ffbd67'
			  }
			},
			viewControl: {
			  // autoRotate: true
			  // projection: 'orthographic'
			}
		  },
		  series: [
			{
			  type: 'scatter3D',
			  data: this.processed_data.map(item => [
				item.region,
				item.experience,
				item.education,
				item.salary,
				item.jobTitle,
				item.company
			  ]),
			  symbolSize: (value) => {
				// 归一化工资值，并映射到点大小范围
				const normalizedSalary = (value[3] - minSalary) / (maxSalary - minSalary);
				return minSymbolSize + normalizedSalary * (maxSymbolSize - minSymbolSize);
			  },
			  itemStyle: {
				borderWidth: 1,
				borderColor: 'rgba(255,255,255,0.8)'
			  },
			  emphasis: {
				itemStyle: {
				  color: '#fff'
				}
			  }
			}
		  ]
		};
  
		myChart.setOption(option);
	  },
	  beforeDestroy(){
      	EventBus.$off('fresh-data', this.freshData);
    }
	}
  };
  </script>
  
  <style scoped>
  #scatter-chart {
	width: 100%;
	height: 100%;
  }
  </style>
  