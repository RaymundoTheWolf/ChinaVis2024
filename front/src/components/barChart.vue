<template>  
    <div id = "bar-chart" ref="chartContainer"></div>  
</template>  
  
<script>  
import * as echarts from 'echarts';  
import axios from 'axios'; 
import { EventBus } from './eventBus.js';
  
export default {  
    name: 'barChartComponent',   
    data() {    
        return {    
            cityData: null, // 改为存储从API获取的全部数据    
            lastClickedCity: '',
            currentCityName: '', // 新增的属性用于显示当前城市名
        };    
    },    
    methods: {    
        getData() {    
            axios.get('http://127.0.0.1:5000/region_map_data')  
                .then(response => {  
                    this.cityData = response.data;  
                    this.updateChart(this.lastClickedCity); // 尝试更新当前选择城市的数据   
                })  
                .catch(error => {  
                    console.error('Error fetching field map data:', error);  
                });  
        },  
        updateChart(city) {    
            if (!this.cityData) return; // 如果数据还未加载，则直接返回  
  
            const { city_avg_salary_dict, city_count_dict } = this.cityData;  
            let citiesMatchingLetter = [];
            let countLetter = [];
            let salaryLetter = [];
  
            if (city.length === 1) { // 如果输入的是单个字母  
                // 筛选出所有以该字母开头的城市名称，薪资，职位数量
                for (let cityName in city_avg_salary_dict) {  
                    if (cityName.startsWith(city)) {  
                        citiesMatchingLetter.push(cityName);  
                        salaryLetter.push(city_avg_salary_dict[cityName]);
                        countLetter.push(city_count_dict[cityName]);
                    }  
                } 
            } else if (city.length > 1) { // 如果输入的是具体城市名
                citiesMatchingLetter = Object.keys(city_avg_salary_dict).filter(cityName => cityName.startsWith(city));
                citiesMatchingLetter.forEach(cityName => {
                    salaryLetter.push(city_avg_salary_dict[cityName]);
                    countLetter.push(city_count_dict[cityName]);
                });
            }
  
            // 基于准备好的数据设置ECharts图表的配置项和数据  
            let option = {  
                xAxis: {  
                    type: 'category',  
                    data: citiesMatchingLetter,
                    axisLabel: {
                        rotate: 45, // 标签旋转45度 
                        interval: 0, // 显示所有标签
                    }
                },  
                yAxis: [  
                    {  
                        type: 'value',  
                        name: '职业数量'  
                    },  
                    {  
                        type: 'value',  
                        name: '平均薪资',  
                        axisLabel: {  
                            formatter: '{value} 元'  
                        }  
                    }  
                ],  
                series: [  
                {    
        name: '职业数量',    
        type: 'bar',    
        yAxisIndex: 0,    
        data: countLetter,  
        itemStyle: {  
            color: (params) => {  
                // 如果匹配到的城市只有一个，并且是当前选中的城市，则高亮显示  
                return (citiesMatchingLetter.length === 1 && citiesMatchingLetter[0] === params.name) ? 'yellow' : 'blue';  
            }  
        }   
    },
                    {  
                        name: '平均薪资',  
                        type: 'line',  
                        yAxisIndex: 1,  
                        data: salaryLetter
                    }  
                ]  
            };
            // 初始化 ECharts 实例并使用配置项和数据显示图表  
            if (!this.myChart) {
                this.myChart = echarts.init(this.$refs.chartContainer);
            }
        
            // 使用配置项和数据显示图表  
            this.myChart.setOption(option);
        }  
    },  
    mounted() {  
        // 获取数据  
        EventBus.$on('value-fresh', (newValue) => {  
            this.lastClickedCity = newValue;
            this.updateChart(newValue); // 更新选定城市的数据  
        });  
        this.getData();  
    }  
};  
</script>
<style>



</style>
