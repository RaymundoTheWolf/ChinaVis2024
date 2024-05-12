<template>
  <div ref="title" class="title-chart"></div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  data() {
    return {
      sunburstData: null
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
      
      // Filter to only top 50 fields
      const topFields = sortedCounts.slice(0, 30);

      // Calculate salary quantiles
      const quantiles = [
        field_avg_salary_dict[sortedFields[Math.floor(sortedFields.length * 0.2)]],
        field_avg_salary_dict[sortedFields[Math.floor(sortedFields.length * 0.4)]],
        field_avg_salary_dict[sortedFields[Math.floor(sortedFields.length * 0.6)]],
        field_avg_salary_dict[sortedFields[Math.floor(sortedFields.length * 0.8)]]
      ];

      // Define salary ranges
      const salaryRanges = [
        { name: 'Low Salary', min: 0, max: quantiles[0] },
        { name: 'Moderate Salary', min: quantiles[0], max: quantiles[1] },
        { name: 'Average Salary', min: quantiles[1], max: quantiles[2] },
        { name: 'High Salary', min: quantiles[2], max: quantiles[3] },
        { name: 'Very High Salary', min: quantiles[3], max: Infinity }
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

      const colorBar = ['#B08D61', '#A4917D', '#8F7D5F', '#C4A985', '#725F4D']


      // Build sunburst data
      const data = salaryRanges.map((range, i) => ({
        name: range.name,
        color:colorBar[i],
        children: salaryGroups[i].map(field => ({
          real_name: field,
          name: topFields.includes(field) ? field : null, // Only show names for top 50 values
          value: field_count_dict[field] || 0,
          itemStyle: {
            color: echarts.color.modifyHSL(colorBar[i], Math.round(field_avg_salary_dict[field]) * 100)
          }
        }))
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
              return 'Field Type: ' + params.data.real_name;
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
          const fieldName = params.data.real_name;
          axios.post('http://127.0.0.1:5000/field_click', { field: fieldName })
            .then(response => {
              console.log('Field clicked:', fieldName);
              console.log('Response data:', response.data)
            })
            .catch(error => {
              console.error('Error sending field click data:', error);
            });
        }
      });
    }
  }
}
</script>

