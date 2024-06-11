<template>
  <div id="title-chart">
    <salary-count/>
    <div class="display-chart">
      <div class="click-info">{{ clickedFieldName }}</div>
      <div ref="title" class="chart"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
import { EventBus } from './eventBus.js';
import { freshData } from './parallelChart.vue';
import salaryCount from './salaryCount.vue';
export default {
  components: {
    salaryCount
  },
  data() {
    return {
      sunburstData: null,
      clickedFieldName: ''
    }
  },
  mounted() {
    this.getData()
  },
  methods: {
    getData() {
      axios.get('http://127.0.0.1:5000/field_map_data')
        .then(response => {
          this.sunburstData = response.data
          this.renderSunburstChart()
        })
        .catch(error => {
          console.error('Error fetching field map data:', error)
        })
    },
    renderSunburstChart() {
      const { field_type, field_avg_salary_dict, field_count_dict } = this.sunburstData;

      const field_type_copy = field_type.slice();
      // Sort fields by average salary
      const sortedFields = field_type.sort((a, b) => field_avg_salary_dict[a] - field_avg_salary_dict[b]);

      const sortedCounts = field_type_copy.sort((a, b) => field_count_dict[b] - field_count_dict[a]);
      
      // Filter to only top 30 fields
      const topFields = sortedCounts.slice(0, 50);

      // Calculate salary quantiles
      const quantiles = [
        field_avg_salary_dict[sortedFields[Math.floor(sortedFields.length * 0.2)]],
        field_avg_salary_dict[sortedFields[Math.floor(sortedFields.length * 0.4)]],
        field_avg_salary_dict[sortedFields[Math.floor(sortedFields.length * 0.6)]],
        field_avg_salary_dict[sortedFields[Math.floor(sortedFields.length * 0.8)]]
      ];

      // Define salary ranges
      const salaryRanges = [
        { name: '低收入', min: 0, max: quantiles[0] },
        { name: '较低收入', min: quantiles[0], max: quantiles[1] },
        { name: '中等收入', min: quantiles[1], max: quantiles[2] },
        { name: '较高收入', min: quantiles[2], max: quantiles[3] },
        { name: '高收入', min: quantiles[3], max: Infinity }
      ];

      // Store fields in corresponding salary ranges
      const salaryGroups = salaryRanges.map(() => []);

      // Put fields into corresponding salary range
      sortedFields.forEach(field => {
        const salary = field_avg_salary_dict[field];
        for (let i = 0; i < salaryRanges.length; i++) {
          if (salary >= salaryRanges[i].min && salary < salaryRanges[i].max) {
            salaryGroups[i].push(field);
            break;
          }
        }
      });

      const baseColors = ['#4CAF50', '#FFEB3B', '#007BFF', '#006400', '#FF0000'];
      
      const topFields1 = topFields.map(field => field.replace(/^type_/, ''));  

      // Build sunburst data
      const data = salaryRanges.map((range, i) => ({  
          name: range.name,  
          color: baseColors[i], // Set the base color for the current range  
          children: salaryGroups[i].map(field => {  
            // Remove 'type_' prefix from the field name  
            const fieldNameWithoutPrefix = field.replace(/^type_/, '');  
              
            // Adjust the brightness based on salary, but scale it down to avoid extreme values  
            const brightnessAdjustment = 0.5 * (2 * (field_avg_salary_dict[field] - 5179.2963) / (19766.667 - 5179.2963)) - 0.5; // Your brightness adjustment logic  
            const adjustedBrightness = Math.max(0, Math.min(1, 0.5 + brightnessAdjustment)); // Your adjusted brightness calculation  
          
            return {  
              real_name: field, // Keep the original field name for other purposes  
              name: topFields1.includes(fieldNameWithoutPrefix) ? fieldNameWithoutPrefix : null, // Use the field name without prefix for display  
              value: field_count_dict[field] || 0,  
              itemStyle: {  
                color: echarts.color.modifyHSL(baseColors[i], null, adjustedBrightness)  
              }  
            };  
          })  
        })); 



      // Build series data
      const seriesData = [{
        name: 'fieldType',
        type: 'sunburst',
        data: data,
        radius: ['10%', '90%'],
        label: {
          rotate: 'radial',
          color: 'white' // Set label color to white
        },
      }];

      // ECharts options
      const option = {
        series: seriesData,
        tooltip: {
          formatter: function (params) {
            if (params.data && params.data.real_name) {
              let name = params.data.real_name.replace(/^type_/, '');
              return name;
            }
          },
          trigger: 'item' // 触发类型设置为'item'，使得可以在鼠标悬停时触发
        }
      };

      // Initialize ECharts instance and set options
      const chart = echarts.init(this.$refs.title);
      chart.setOption(option);

      chart.on('click', params => {
        if (params.data && params.data.real_name) {
          this.clickedFieldName = "当前显示行业："+params.data.real_name.replace(/^type_/, ''); // 更新显示框内容
          const fieldName = params.data.real_name;
          sessionStorage.setItem('lastFieldName', fieldName);
          EventBus.$emit('fresh-data', fieldName);
          axios.post('http://127.0.0.1:5000/field_click', { field: fieldName })
            .then(response => {
              console.log('Field clicked:', fieldName);
              console.log('Response data:', response.data)
            })
            .catch(error => {
              console.error('Error sending field click data:', error);
            });
        }
        EventBus.$emit('value-updated', params.data.real_name);
      });
    }
  }
}
</script>

<style>
#title-chart {
  display: flex;
  width: 100%;
  height: 100%;
}
#title-chart .display-chart {
  display: flex;
  width: 50%;
  height: 100%;
  flex-direction: column;
}
#title-chart .chart {
  width: 100%;
  height: 100%;
}
#title-chart .click-info {
  margin-top: 10px;
  margin-left: 30%;
  padding: 5px;
  border-radius: 5px;
  width: 80%;
  height: 10%;
  pointer-events: none; /* 可选：确保这个元素不响应鼠标事件 */
}
</style>

