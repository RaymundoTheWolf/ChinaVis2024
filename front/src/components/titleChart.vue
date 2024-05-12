<template>
    <div ref="map" class="map_chart"></div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  data() {
    return {
      mapData: null
    }
  },
  mounted() {
    this.getData()
  },
  methods: {
    getData() {
      axios.get('http://127.0.0.1:5000/field_map_data')
        .then(response => {
          this.mapData = response.data
          this.renderMap()
        })
        .catch(error => {
          console.error('Error fetching field map data:', error)
        })
    },
    renderMap() {
      const { field_type, field_avg_salary_dict, field_count_dict } = this.mapData;

      // 将城市按照平均工资排序
      const sortedCities = field_type.sort((a, b) => field_avg_salary_dict[b] - field_avg_salary_dict[a]);

      // 定义圆的半径和每个圆上的城市数量
      const radius = [600, 500, 400, 300, 200]; // 六个圆的半径从大到小
      const fieldCounts = []; // 每个圆上的城市数量
      const totalCount = field_type.length; // 总城市数量
      let sum = 0;

      // 计算每个圆上的城市数量
      for (let i = 0; i < radius.length; i++) {
        fieldCounts.push(Math.floor(totalCount * radius[i] / 2000));
        sum += Math.floor(totalCount * radius[i] / 2000);
        if (i === radius.length - 1){
          fieldCounts.push(totalCount - sum)
        }
      }

      const data = [];
      let fieldIndex = 0;

      // 遍历每个圆
      for (let i = 0; i < radius.length; i++) {

        // 放置每个圆上的城市
        for (let j = 0; j < fieldCounts[i]; j++) {
          const field = sortedCities[fieldIndex];
          let count = field_count_dict[field] || 0; // 获取城市数量，若无数据则默认为0
          if (count > 10000) {
            count /= 25;
          }

          // 计算当前城市的坐标
          const x = radius[i] * Math.cos((j / fieldCounts[i]) * Math.PI * 2);
          const y = radius[i] * Math.sin((j / fieldCounts[i]) * Math.PI * 2);

          data.push({
            name: field,
            value: [x, y],
            symbolSize: Math.sqrt(count) * 1.2, // 根据城市数量设置点的大小
            itemStyle: {
              color: echarts.color.modifyHSL('#5A94DF', Math.round(field_count_dict[field]) * 100)
            }
          });

          fieldIndex++;
        }
      }

      const option = {
        tooltip: {
          formatter: function(params) {
            const field = params.data.name;
            const avgSalary = field_avg_salary_dict[field];
            const count = field_count_dict[field] || 0;
            return `${field}<br/>平均薪资: ${avgSalary}<br/>出现次数: ${count}`;
          }
        },
        xAxis: {
          type: 'value'
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          type: 'scatter',
          coordinateSystem: 'cartesian2d',
          data: data
        }]
      };

      const chart = echarts.init(this.$refs.map);
      chart.setOption(option);

      // 点击事件
      chart.on('click', function(params) {
        if (params.data && params.data.name) {
          const fieldName = params.data.name;
          axios.post('http://127.0.0.1:5000/field_click', { field: fieldName })
            .then(response => {
              console.log('Field clicked:', fieldName);
              console.log('Response data:', response.data)
            })
            .catch(error => {
              console.error('Error sending city click data:', error);
            });
        }
      });
    }
  }
}
</script>
