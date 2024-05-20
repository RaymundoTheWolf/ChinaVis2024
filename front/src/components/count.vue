<template>  
    <div id="count-chart" class="count-chart">  
        <div ref="chartContainer" style="width: 600px; height: 600px; margin-top: 40px; margin-left: 120px;">
            <div class="click-in">当前显示地区为: {{ currentCityName }}</div>
            <div>
                <span>职业数量：{{ cityCount.toString() }}</span>
                <span>  平均薪资：{{ cityAvgSalary.toString() }}</span>
            </div>
        </div>  
    </div>  
</template>  
  
<script>  
import axios from 'axios';  
import { EventBus } from './eventBus.js';  
  
export default {  
    name: 'count-chart',    
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
.click-in {
  position: relative;
  top: -10px;
  left: 10px;
  background-color: #f0f0f0;
  padding: 5px;
  border-radius: 5px;
  z-index: 1000;
  width: 200px;
  height: 30px;
  color: black; 
  pointer-events: none; /* 可选：确保这个元素不响应鼠标事件 */
}
</style>
