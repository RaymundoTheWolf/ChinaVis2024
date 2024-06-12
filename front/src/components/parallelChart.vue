<template>
  <div id="parallel-chart">
    <div class="input-button-container">
      <el-select 
        v-model="inputJobTitle" 
        placeholder="请选择或输入职位" 
        clearable 
        filterable 
        remote 
        allow-create
        multiple 
        :remote-method="getCheckBoxData" 
        class="input" 
        collapse-tags
        @change="handleSelectChange"
      >
        <el-option
          v-for="item in jobTitles"
          :key="item"
          :label="item"
          :value="item"
        ></el-option>
      </el-select>
      <el-button class="search-button" type="primary" @click="shift">
        <i class="el-icon-search"></i>
      </el-button>
    </div>
    <!-- 创建一个容器来放置图表 -->
    <div ref="chart" class="chart" style="width: 100%; height: 100%;"></div>
  </div>
</template>

<script>
import axios from 'axios';  
import * as echarts from 'echarts';
import { Notification } from 'element-ui'; 
import { EventBus } from './eventBus';

export default {
  created() {
    EventBus.$on('fresh-data', (newValue) => {
      this.freshData(newValue);
    });
  },
  data() {
    return {
      typeName: '',
      jobTitles: [],
      companyType: "",
      inputJobTitle: [],
      selectedJobTitle: '',
      chart: null, // 绘制的图表
      option: null, // 图表参数
      paralleldata: null, // 返回的图表数据
      paralleldataShift: null, // 筛选后的图表数据
      allJobTitle: null, // 返回数据对应的职位
      shiftSwitch: false // 是否处于筛选状态
    };
  },
  mounted() {
    this.getData();
    this.typeName = 'type_MpUmNW';
    this.getCheckBoxData();
    EventBus.$on('fresh-data', (newValue) => {
      this.typeName = newValue;
      this.getCheckBoxData();
    });
  },
  methods: {
    getCheckBoxData(query) {
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
    getData() {
      if (this.companyType === '') {
        this.companyType = 'type_aAuygy';
      }

      axios.post('http://127.0.0.1:5000/job_parallel_all', {
        companyType: this.companyType
      })
        .then(response => {
          this.paralleldata = response.data.data;
          this.allJobTitle = response.data.job;
          this.initChart();
        })
        .catch(error => {
          console.error('Error sending job parallel data:', error);
        });
    },
    // 筛选职位
    shift() {
      const selectedJobTitles = this.inputJobTitle.join(', ');
      console.log(selectedJobTitles);

      if (selectedJobTitles === '') {
        this.clear();
        return;
      }

      for (const jobTitle of this.inputJobTitle) {
        const jobTitleStr = jobTitle.toString();
        const newIndices = this.inputJobTitle.map(title => this.allJobTitle.indexOf(title));
        if (newIndices.some(index => index === -1)) {
          Notification({
            title: '提示',
            message: '该行业没有所筛选的职位',
            type: 'error'
          });
          return;
        } else {
          if (this.shiftSwitch) {
            newIndices.forEach(newIndex => {
              this.paralleldataShift[newIndex].lineStyle = {
                width: '2',
                opacity: '0.4',
              };
            });
          } else {
            this.paralleldataShift = this.paralleldata.map((item, index) => {
              const isSelected = newIndices.includes(index);
              return {
                value: item,
                lineStyle: {
                  width: isSelected ? '2' : '1',
                  opacity: isSelected ? '0.4' : '0.008'
                }
              };
            });
            this.shiftSwitch = true;
          }
          this.option.series.data = this.paralleldataShift;
          this.chart.setOption(this.option);
        }
      }
    },
    // 清空筛选
    clear() {
      this.paralleldataShift = this.paralleldata;
      this.option.series.data = this.paralleldataShift;
      this.chart.setOption(this.option);
      this.shiftSwitch = false;
      this.inputJobTitle = [];
    },
    // 初始化图表
    initChart() {
      this.chart = echarts.init(this.$refs.chart);
      this.option = {
        backgroundColor: 'transparent',
        parallelAxis: [
          { dim: 0, name: '地区' },
          { dim: 1, name: '工作经验' },
          { dim: 2, name: '教育经历' },
          { dim: 3, name: '公司' },
        ],
        visualMap: {
          show: false,
          min: 0,
          max: 1,
          dimension: 2,
          inRange: {
            color: ['#EA907A', '#2E72AF', '#98ff93', '#ffcb60'].reverse(),
          }
        },
        parallel: {
          left: '5%',
          right: '5%',
          bottom: '6%',
          parallelAxisDefault: {
            type: 'value',
            nameTextStyle: {
              color: '#fff',
              fontSize: 12
            },
            axisLine: {
              lineStyle: {
                color: '#aaa'
              }
            },
            axisTick: {
              lineStyle: {
                color: '#777'
              }
            },
            splitLine: {
              show: false
            },
            axisLabel: {
              color: '#fff'
            }
          }
        },
        series: {
          type: 'parallel',
          data: this.paralleldata,
        }
      };
      this.chart.setOption(this.option);
    },
    // 根据行业刷新图
    freshData(new_type) {
      console.log("已获取行业");
      axios.post('http://127.0.0.1:5000/job_parallel_all', {
        companyType: new_type
      })
        .then(response => {
          this.paralleldata = response.data.data;
          this.allJobTitle = response.data.job;
          console.log(this.paralleldata);
          console.log(this.allJobTitle);
        })
        .catch(error => {
          console.error('Error sending job parallel data:', error);
        });
      this.paralleldataShift = this.paralleldata;
      this.option.series.data = this.paralleldataShift;
      this.chart.setOption(this.option);
      this.shiftSwitch = false;
    },
    // 处理用户输入或选择的变化
    handleSelectChange(value) {
      value.forEach(item => {
        if (!this.jobTitles.includes(item)) {
          this.jobTitles.push(item);
        }
      });
    }
  },
  beforeDestroy() {
    EventBus.$off('fresh-data', this.freshData);
  }
};
</script>

<style>
/* 基础样式 */
#parallel-chart {
  display: flex;
  width: 100%;
  height: 100%;
  padding: 20px; /* 内边距，可根据需要调整 */
  box-sizing: border-box; /* 使得padding不会影响整体尺寸 */
  flex-direction: column;
}

/* 输入框和按钮的容器样式 */
#parallel-chart .input-button-container {
  display: flex;
  flex-direction: row;
  height: 5%;
  width: 100%;
  margin-bottom: 20px;
}

/* 输入框样式 */
#parallel-chart .input {
  flex-shrink: 1; /* 输入框将占据剩余空间 */
  height: 10%;
  flex-basis: 50%;
}

#parallel-chart .search-button {
  width: 10%;
  height: 100%;
  padding: 10px;
  margin-left: 1%;
  align-items: center;
  display: flex;
  justify-content: center;
  background-color: #b7b2d0;
}
</style>
