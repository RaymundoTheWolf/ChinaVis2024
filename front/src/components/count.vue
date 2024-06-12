<template>  
    <div id="count-chart" class="count-chart">  
        <div ref="chartContainer" class="show">
            <span class="city-info">当前显示地区为: {{ currentCityName }}</span>
            <span class="city-info">职业数量：{{ cityCount.toString() }}</span>
            <span class="city-info">平均薪资：{{ Math.round(cityAvgSalary).toString() }}</span>
        </div>
        <bar-chart class="bar-chart"/>
    </div>  
</template>  

<script>  
import axios from 'axios';  
import { EventBus } from './eventBus.js';
import barChart from './barChart.vue'
  
export default {
    components: {
    barChart,
},
    name: 'count',    
    data() {    
        return {    
            cityData: null, // 改为存储从API获取的全部数据    
            lastClickedCity: '',
            currentCityName: '', // 新增的属性用于显示当前城市名
            cityCount: 1000,    
            cityAvgSalary: 1000
        };    
    },    
    methods: {    
        getData() {    
            axios.get('http://127.0.0.1:5000/region_map_data')  
                .then(response => {  
                    this.cityData = response.data;  
                    this.updateDataForCity(this.lastClickedCity); // 尝试更新当前选择城市的数据   
                })  
                .catch(error => {  
                    console.error('Error fetching field map data:', error);  
                });  
        },  
        updateDataForCity(city) {    
            if (!this.cityData) return; // 如果数据还未加载，则直接返回  
  
            const { cities, city_avg_salary_dict, city_count_dict } = this.cityData;  
            let totalSalary = 0;  
            let totalCount = 0;  
            let citiesMatchingLetter = [];  

            this.currentCityName = city; // 更新当前选择的城市名  
  
            if (city.length === 1) { // 如果输入的是单个字母  
                // 筛选出所有以该字母开头的城市，并计算平均薪资总和和职业数量总和  
                for (let cityName in city_avg_salary_dict) {  
                    if (cityName.startsWith(city)) {  
                        citiesMatchingLetter.push(cityName);  
                        totalSalary += city_avg_salary_dict[cityName];  
                        totalCount += city_count_dict[cityName];  
                    }  
                }  
                if (totalCount > 0) {  
                    this.cityAvgSalary = totalSalary / citiesMatchingLetter.length; // 平均薪资是薪资总和除以城市数量  
                    this.cityCount = totalCount; // 对于单个字母，我们认为职业数量就是所有相关城市的职业数量总和  
                } else {  
                    this.cityAvgSalary = null;  
                    this.cityCount = null;  
                }  
            } else { // 如果输入的是完整的城市名  
                this.cityAvgSalary = city_avg_salary_dict[city];  
                this.cityCount = city_count_dict[city];  
            }  
        }  
    },  
    mounted() {  
        // 获取数据  
        EventBus.$on('value-fresh', (newValue) => {  
            this.lastClickedCity = newValue;
            this.updateDataForCity(newValue); // 更新选定城市的数据  
        });  
        this.getData();  
    }  
};  
</script>

<style>
#count-chart{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding-left: 2%;
    padding-right: 2%;
}

#count-chart .show{
    width: 100%;
    height: 20%;
    margin-left: 5%;
    display: flex;
    flex-direction: column;
    font-family: 'Arial', sans-serif;
    color: #daf0dd;
    align-items: center;
}

#count-chart .city-info {
    font-size: 1.5em;
    margin-bottom: 5px;
    font-weight: bold;
    text-shadow: 1px 1px 2px #888888;
}

#count-chart .bar-chart {
    width: 100%;
    height: 80%;
    display: flex;
}
</style>
