<template>  
    <div id="bar-chart" ref="chartContainer"></div>  
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
            defaultCities: ['City1', 'City2', 'City3', 'City4', 'City5', 'City6'], // 默认城市数据
            defaultCounts: [100, 200, 150, 120, 300, 50], // 默认职业数量数据
            defaultSalaries: [5000, 6000, 5500, 6500, 10000, 5000] // 默认平均薪资数据
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
            const { city_avg_salary_dict, city_count_dict } = this.cityData || {};  
            let citiesMatchingLetter = [];
            let countLetter = [];
            let salaryLetter = [];
  
            if (city && city.length === 1) { // 如果输入的是单个字母  
                // 筛选出所有以该字母开头的城市名称，薪资，职位数量
                for (let cityName in city_avg_salary_dict) {  
                    if (cityName.startsWith(city)) {  
                        citiesMatchingLetter.push(cityName);  
                        salaryLetter.push(city_avg_salary_dict[cityName]);
                        countLetter.push(city_count_dict[cityName]);
                    }  
                } 
            } else if (city && city.length > 1) { // 如果输入的是具体城市名
                citiesMatchingLetter = Object.keys(city_avg_salary_dict).filter(cityName => cityName.startsWith(city));
                citiesMatchingLetter.forEach(cityName => {
                    salaryLetter.push(city_avg_salary_dict[cityName]);
                    countLetter.push(city_count_dict[cityName]);
                });
            }
  
            // 如果没有匹配到任何城市，则使用默认值
            if (citiesMatchingLetter.length === 0) {
                citiesMatchingLetter = this.defaultCities;
                countLetter = this.defaultCounts;
                salaryLetter = this.defaultSalaries;
            }
  
            // 基于准备好的数据设置ECharts图表的配置项和数据  
            let option = {  
                xAxis: {  
                    type: 'category',  
                    data: citiesMatchingLetter,
                    axisLabel: {
                        rotate: 45, // 标签旋转45度 
                        interval: 0, // 显示所有标签
                        fontSize: 7
                    }
                },  
                yAxis: [  
                    {  
                        type: 'value',  
                        name: '职业数量',
                        axisLabel: {  
                            fontSize: 6.5
                        }
                    },  
                    {  
                        type: 'value',  
                        name: '平均薪资',  
                        axisLabel: {  
                            formatter: '{value} ',
                            fontSize: 6.5
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
                            color: '#d9b1b7'  
                        },     
                    },
                    {  
                        name: '平均薪资',  
                        type: 'line',  
                        yAxisIndex: 1,  
                        data: salaryLetter,
                        itemStyle: {  
                            color: '#fff8d5'  
                        }  
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
#bar-chart {
    width: 100%;
    height: 400px;
}
</style>
