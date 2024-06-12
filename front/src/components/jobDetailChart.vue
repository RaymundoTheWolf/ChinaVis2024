<template>
  <div id="job-detail-chart">
    <div class="container">
      <el-select v-model="selectedJobTitle" placeholder="请选择或输入职位" clearable filterable remote :remote-method="getCheckBoxData" class="select">
        <el-option
          v-for="item in jobTitles"
          :key="item"
          :label="item"
          :value="item"
        ></el-option>
      </el-select>
      <el-button class="search-button" type="primary" @click="search">
        <i class="el-icon-search"></i>
      </el-button>
    </div>
    <div class="content-container">
      <div class="charts-container">
        <div class="job-info">
          <div>{{ this.searchedSalary }}</div>
        </div>
        <percentageChart ref="percentageChart" class="percentageChart"/>
      </div>
      <div class="final-container">
        <div class="details-container">
          <div class='pie-chart' ref="pieChart"></div>
          <div class='bar-chart' ref="barChart"></div>
        </div>
        <div class="top-jobs-container">
          <radarChart ref="lineChart" class="lineChart"/>
          <ringChart ref="ringChart" class="ringChart"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';
import percentageChart from './percentageChart.vue';
import ringChart from './ringChart.vue';
import lineChart from './lineChart.vue';
import radarChart from './radar.vue'
import { EventBus } from './eventBus';

export default {
  components: {
    percentageChart,
    ringChart,
    lineChart,
    radarChart
  },
  data() {
    return {
      jobTitles: [],
      skillPreference: [0.5, 0.5, 0.5],
      avgSkillPreference: [0.3, 0.3, 0.3],
      selectedJobTitle: '',
      typeName: '',
      searchedSalary: 5000,
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
    this.pieChart = echarts.init(this.$refs.pieChart);
    this.renderPieChart();
    this.barChart = echarts.init(this.$refs.barChart);
    this.renderBarChart();
    EventBus.$on('fresh-data', (newValue)=>{
      this.typeName = newValue,
      this.getCheckBoxData()
    });

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
          this.renderPieChart();
          this.renderBarChart();
          EventBus.$emit('salary', this.searchedSalary);
          EventBus.$emit('radar-data', {
            avgSkillPreference: this.avgSkillPreference,
            skillPreference: this.skillPreference
          });
          EventBus.$emit('top-jobs', {
            score: response.data.top_scores.flat(),
            job: response.data.top_jobs.flat()
          });
          EventBus.$emit('line-job', response.data.top_jobs.flat());
        })
      sessionStorage.setItem('selectedJobTitle', this.selectedJobTitle);
      localStorage.setItem('salaryPercentage', this.searchedSalary);
      EventBus.$emit('salary', this.searchedSalary);
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
          boundaryGap: [0, 0.01],
          show:false
        },
        yAxis: {
          nameGap: 20,
          type: 'category',
          data: ['Max', 'Min'],
          axisLabel: {
            fontSize:9
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: (params) => {
            const labels = ['min salary', 'max salary'];
            return `${labels[params.dataIndex]}: ${params.value}`;
          }
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
#job-detail-chart {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

#job-detail-chart .container {
  display: flex;
  width: 100%;
  height: 15%;
  padding-left: 10%;
}

#job-detail-chart .select {
  width: 40%;
  height: 100%;
  margin-left: 20%;
}

#job-detail-chart .search-button {
  width: 10%;
  height: 100%;
  margin-left: 1%;
  flex-direction: column;
  align-items: center;
}

#job-detail-chart .content-container {
  display: flex;
  width: 95%;
  height: 100%;
  padding-left: 10%;
  padding-bottom: 2%;
}

#job-detail-chart .percentageChart {
  margin-left: 20%;
  width: 80%;
  height: 100%;
}

#job-detail-chart .job-info {
  margin-left: 20%;
  font-size: 25px;
  font-weight: bold;
  font-family: 'cursive';
  margin-top: 50%;
  text-align: center;
  color: #dcdcdc;
  width: 80%;
  height: 2%;
}

#job-detail-chart .charts-container {
  display: flex;
  flex-direction: column;
  width: 20%;
  height: 110%;
}

#job-detail-chart .pie-chart {
  width: 100%;
  height: 100%;
  margin-top: 2%;
}

#job-detail-chart .bar-chart {
  width: 200%;
  height: 140%;
  margin-top: -5%;
  left: 20%;
  overflow: visible;
}

#job-detail-chart .final-container {
  display: flex;
  flex-direction: column;
  width: 70%;
  height: 100%;
  padding-left: 5%;
  padding-bottom: 20px; 
}

#job-detail-chart .details-container {
  display: flex;
  width: 100%;
  height: 50%;
}

#job-detail-chart .top-jobs-container {
  width: 100%;
  height: calc(50%); 
  display: flex;
  border: 2px solid #dcdcdc;
  border-radius: 10px;
  padding: 5px;
}

#job-detail-chart .ringChart {
  width: 50%;
  height: 100%;
}

#job-detail-chart .lineChart {
  padding-top: 5px;
  width: 50%;
  height: 120%;
}
</style>
