<template>
  <div id="parallel-chart">
      <div class="input-button-container">
          <el-input v-model="inputJobTitle" placeholder="请输入职位" class="input"/>
          <el-button class="search-button" type="primary" @click="shift">筛选</el-button>
          <el-button class="search-button" type="primary" @click="clear">清空</el-button>
      </div>
      <!-- 创建一个容器来放置图表 -->
      <div ref="chart" style="width: 100%; height: 100%;"></div>
  </div>
</template>


<script>
  import axios from 'axios';  
  import * as echarts from 'echarts';
  import { Notification } from 'element-ui'; 
  
  
  export default {
    data() {
      return {
        companyType: '',
        inputJobTitle: '',
        chart: null,//绘制的图表
        option: null,//图表参数
        paralleldata: null,//返回的图表数据
        paralleldataShift: null,//筛选后的图表数据
        allJobTitle: [],//返回数据对应的职位
        shiftSwitch: false //是否处于筛选状态
      };
    },
    mounted() {
        this.getData();
    },
    methods: {
      getData() {
        console.log("开始发送");
        if(this.companyType == '') {
          this.companyType = 'type_aAuygy';
        }
        axios.post('http://127.0.0.1:5000/job_parallel_all',{
            companyType : this.companyType 
            })
            .then(response => {
                this.paralleldata = response.data.data;
                this.allJobTitle = response.data.job;
                console.log(this.paralleldata);
                console.log(this.allJobTitle);
                this.initChart();
            })
            .catch(error => {
                console.error('Error sending job title comparison data:', error);
            });
      },
      //筛选职位
      shift() {
        //更新图表中数据项的样式
        if(this.inputJobTitle != ''){
          var newindex = this.allJobTitle.indexOf(this.inputJobTitle)
          if (newindex == -1){
            Notification({  
              title: '提示',  
              message: '该行业没有所筛选的职位',  
              type: 'error'  
            });
          }
          else{
            if(this.shiftSwitch){
            this.paralleldataShift[newindex].lineStyle = {
              //color: '#ffcc00'
              width: '10',
              opacity: '1',
            }
            }
            else{
              this.paralleldataShift = this.paralleldata.map((item, index) => {
                return {
                  value: item,
                  lineStyle: {
                    //color: (index == newindex) ? '#ffcc00' : '#ccc',
                    width: (index == newindex) ? '10' : '1',
                    opacity: (index == newindex) ? '1' : '0.05'
                  }
                };
              })
              this.shiftSwitch = true
            }
            this.option.series.data = this.paralleldataShift
            this.chart.setOption(this.option)
          }
        }
      },
      //清空筛选
      clear(){
        this.paralleldataShift = this.paralleldata
        this.option.series.data = this.paralleldataShift
        this.chart.setOption(this.option)
        this.shiftSwitch = false
        this.inputJobTitle = ''
      },
      //初始化图表
      initChart() {
        this.chart = echarts.init(this.$refs.chart);
        this.option = {
            backgroundColor: '#22272e',
            parallelAxis : [
            {dim: 0, name: '地区'},
            {dim: 1, name: '工作经验'},
            {dim: 2, name: '教育经历'},
            {dim: 3, name: '公司'},
            ],
            visualMap: {
              show: false,
              min: 0,
              max: 1,
              dimension: 2,
              inRange: {
                color: ['#F38181', '#FCE38A', '#EAFFD0', '#95E1D3'].reverse(),
                //colorAlpha: [0, 1]
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
        this.chart.setOption(this.option)
      },
    }
  }
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
    height: 12%;
    width: 100%;
    margin-bottom: 20px;
}

/* 输入框样式 */
#parallel-chart .el-input {
    flex-shrink: 1; /* 输入框将占据剩余空间 */
    height: 50%;
    flex-basis: 50%;
}
/* 搜索按钮样式 */
#parallel-chart .search-button {
  flex-basis: 10%;
  margin-left: 10px; /* 按钮之间留出空间 */
}

/* 图表容器样式 */
#parallel-chart div[ref="chart"] {
  flex-shrink: 1;
  width: 100%; /* 图表容器宽度为100%，可以占据父容器的全部宽度 */
  height: auto; /* 图表容器高度，可根据需要调整 */
}
</style>
