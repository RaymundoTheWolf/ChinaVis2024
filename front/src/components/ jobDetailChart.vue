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
    <div class="content-container">
      <div class="charts-container">
        <percentageChart ref="percentageChart" style="width: 100px; height: 200px;"/>
        <div class='radar' ref="radarChart" style="width: 200px; height: 300px;"></div>
      </div>
      <div class="final-container">
        <div class="details-container">
          <div class='pie-chart' ref="pieChart" style="width: 180%; height: 100%;"></div>
          <div class='bar-chart' ref="barChart" style="width: 421%; height: 150px;"></div>
        </div>
        <div class="top-jobs-container">
          <div
            v-for="(job, index) in topJobs"
            :key="index"
            class="job-name"
            @click="selectJob(job)"
          >
            {{ job }}
          </div>
        </div>
      </div>
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
      searchedSalary: 0,
      cityName: ['J722', 'Q598', 'H610', 'K115'],
      cityTimes: [1, 1, 1, 6],
      minSalary: 1000,
      maxSalary: 10000,
      topJobs: ['75321885b3a892ec010656b498fda861kW', 'c38f53b33c8355beed8af099908fb1d7JE', 'fb6e82ef0a1eb0f9e6d8196638d40408tu'],
      topValues: [0.8, 0.6, 0.7],
      ringChart: []
    };
  },
  mounted() {
    this.typeName = 'type_MpUmNW';
    this.getCheckBoxData();
    this.radarChart = echarts.init(this.$refs.radarChart);
    this.renderRadarChart();
    this.pieChart = echarts.init(this.$refs.pieChart);
    this.renderPieChart();
    this.barChart = echarts.init(this.$refs.barChart);
    this.renderBarChart();
  },
  methods: {
    selectJob(job) {
      this.selectedJobTitle = job;
      this.search();
    },
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
          jobList: this.jobTitles.flat()
        })
        .then(response => {
          this.topJobs = []
          this.skillPreference = response.data.matrix_job.flat().slice(0, 3);
          this.avgSkillPreference = response.data.matrix_title.flat().slice(0, 3);
          this.searchedSalary = response.data.salary;
          this.cityName = response.data.city_name;
          this.cityTimes = response.data.city_times.flat()
          this.maxSalary = response.data.max_salary;
          this.minSalary = response.data.min_salary;
          this.topJobs = response.data.top_jobs.flat();
          this.renderRadarChart();
          this.renderPieChart();
          this.renderBarChart();
          console.log(this.topJobs)
        })
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
    },
    renderPieChart() {
      this.pieChart.clear();
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            padAngle: 5,
            itemStyle: {
              borderRadius: 10
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 40,
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: this.cityName.map((name, index) => ({
              value: this.cityTimes[index],
              name: name
            }))
          }
        ]
      };
      this.pieChart.setOption(option);
    },
    renderBarChart() {
      this.barChart.clear();
      const option = {
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.01]
        },
        yAxis: {
          type: 'category',
          data: ['Min Salary', 'Max Salary']
        },
        series: [
          {
            type: 'bar',
            data: [this.minSalary, this.maxSalary],
            itemStyle: {
              color: '#aba08c'
            },
            barWidth: '50%'
          }
        ]
      };
      this.barChart.setOption(option);
    },
  },
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
  margin-top: 20px;
  transform: translateX(-50%);
}

.select {
  width: 60%; /* 设置选择框的宽度 */
}

.search-button {
  width: 30%; /* 设置按钮的宽度 */
}

.content-container {
  display: flex;
  margin-left: 10px; /* 左边距 */
  justify-content: space-between;
}

.charts-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* 将内容从容器顶部开始排列 */
  left: 0;
  margin-left: 20px; /* 左边距 */
  margin-right: -40px; 
  margin-top: 80px;
}

.details-container {
  display: flex;
  left: 0;
  margin-top: 70px;
}



.final-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* 将内容从容器顶部开始排列 */
  margin-left: -200px
}

.job-name {
  font-size: 20px;
  font-weight: bold;
  font-family: 'cursive'; /* 设置花字字体 */
  color: #9894a7;
  margin-top: 30px;
}

.radar {
  margin-top: -100px;
}
</style>

