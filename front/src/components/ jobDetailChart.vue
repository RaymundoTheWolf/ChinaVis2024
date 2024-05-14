<template>
  <div>
    <div class="container">
      <el-select v-model="selectedJobTitle" placeholder="请选择或输入职位" clearable filterable remote :remote-method="getCheckBoxData" class="select">
        <el-option
          v-for="item in jobTitles"
          :key="item"
          :label="item"
          :value="item"
        ></el-option>
      </el-select>
      <el-button class="search-button" type="primary" @click="search">搜索</el-button>
    </div>
    <div class="charts-container">
      <percentageChart ref="percentageChart" style="width: 30%; height: 300px;"/>
      <div ref="radarChart" style="width: 500px; height: 300px;"></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts'; 
import percentageChart from './percentageChart.vue';

export default {
  components: {
    percentageChart
  },
  data() {
    return {
      jobTitles: [],
      skillPreference: [0.5, 0.5, 0.5],
      avgSkillPreference: [0.3, 0.3, 0.3],
      selectedJobTitle: '',
      radarChart: null,
      typeName: '',
      searchedSalary: 0
    };
  },
  mounted() {
    this.typeName = 'type_MpUmNW';
    this.getCheckBoxData();
    this.radarChart = echarts.init(this.$refs.radarChart);
    this.renderRadarChart();
    window.addEventListener('storage', e => {
        if(e.key == 'selectedJobTitle'){
            console.log("new")
        }
      })
  },
  methods: {
    getCheckBoxData() {
      axios.post('http://127.0.0.1:5000/check_box', {
        typeName: this.typeName,
      })
        .then(response => {
          this.jobTitles = response.data;
        })
        .catch(error => {
          console.error('Error fetching checkbox data:', error);
        });
    },
    search() {
      if (this.selectedJobTitle === '') {
        this.selectedJobTitle = 'e0dd920456695914fed9481503e83b41xW';
      }
      axios.post('http://127.0.0.1:5000/job_title_comparison', {
          jobTitle: this.selectedJobTitle,
          typeName: this.typeName,
        })
        .then(response => {
          this.skillPreference = response.data.matrix_job.flat().slice(0, 3);
          this.avgSkillPreference = response.data.matrix_title.flat().slice(0, 3);
          this.searchedSalary = response.data.salary;
          this.renderRadarChart();
        })
        .catch(error => {
          console.error('Error sending job title comparison data:', error);
        });
      this.$refs.percentageChart.updateChartOption();
      sessionStorage.setItem('selectedJobTitle', this.selectedJobTitle);
      localStorage.setItem('salaryPercentage', this.searchedSalary);
    },
    renderRadarChart() {
      const option = {
        radar: {
          indicator: [
            { name: 'City', max: 1 },
            { name: 'Experience', max: 1 },
            { name: 'Education', max: 1 },
          ],
          center: ['50%', '50%'],
          radius: '60%'
        },
        series: [{
          type: 'radar',
          data: [
            {
              value: this.skillPreference, 
              name: 'Skill Performance'
            },
            {
              value: this.avgSkillPreference, 
              name: 'Average Skill Performance'
            }
          ]
        }]
      };
      this.radarChart.setOption(option);
    }
  }
};
</script>

<style>
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  max-width: 800px; /* 设置容器的最大宽度 */
  margin: 0 auto; /* 水平居中 */
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.select {
  width: 60%; /* 设置选择框的宽度 */
}

.search-button {
  width: 30%; /* 设置按钮的宽度 */
}

.charts-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* 将内容从容器顶部开始排列 */
  position: absolute;
  left: 0;
  margin-left: 20px; /* 左边距 */
  margin-top: 200px;
}

</style>

