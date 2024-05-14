<template>  
    <div>
        <el-input v-model="inputJobTitle" placeholder="请输入职位"  class="input"/>
        <el-button class="search-button" type="primary" @click="shift">筛选</el-button>
        <el-button class="search-button" type="primary" @click="clear">清空</el-button>
        
        <!-- 创建一个容器来放置图表 -->  
        <div ref="chart" style="width: 100%; height: 1000px;"></div>
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
              show: true,
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
              right: '18%',
              bottom: 100,
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
  .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 800px; /* 设置容器的最大宽度 */
    margin: 0 auto; /* 水平居中 */
  }
  
  .input {
    width: 31%; /* 设置输入框的宽度 */
  }
  
  .search-button {
    width: 15%; /* 设置按钮的宽度 */
  }
  </style>
