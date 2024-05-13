<template>
    <div class="container">
      <el-select v-model="selectedJobTitle1" placeholder="请选择或输入职位" clearable filterable remote :remote-method="getCheckBoxData" class="select1">
        <el-option
          v-for="item in jobTitles"
          :key="item"
          :label="item"
          :value="item"
        ></el-option>
      </el-select>
      <el-select v-model="selectedJobTitle2" placeholder="请选择或输入职位" clearable filterable remote :remote-method="getCheckBoxData" class="select2">
        <el-option
          v-for="item in jobTitles"
          :key="item"
          :label="item"
          :value="item"
        ></el-option>
      </el-select>
      <el-button class="search-button" type="primary" @click="search">搜索</el-button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        jobTitles: [],
        selectedJobTitle1: '',
        selectedJobTitle2: ''
      };
    },
    mounted() {
      this.getCheckBoxData();
      this.restoreFromLocalStorage();
    },
    methods: {
      getCheckBoxData() {
        axios.get('http://127.0.0.1:5000/check_box')
          .then(response => {
            this.jobTitles = response.data.job_titles;
          })
          .catch(error => {
            console.error('Error fetching checkbox data:', error);
          });
      },
      search() {
        if (this.selectedJobTitle1 === '') {
          this.selectedJobTitle1 = 'e0dd920456695914fed9481503e83b41xW';
        }
        if (this.selectedJobTitle2 === '') {
          this.selectedJobTitle2 = '9f17193f3306b63788eac8e6a4b70f88oL';
        }
        axios.post('http://127.0.0.1:5000/job_title_comparison', {
            jobTitle1: this.selectedJobTitle1,
            jobTitle2: this.selectedJobTitle2
          })
          .then(response => {
            console.log(response);
          })
          .catch(error => {
            console.error('Error sending job title comparison data:', error);
          });
        localStorage.setItem('selectedJobTitle1', this.selectedJobTitle1);
        localStorage.setItem('selectedJobTitle2', this.selectedJobTitle2);
      },
      restoreFromLocalStorage() {
        const jobTitle1 = localStorage.getItem('selectedJobTitle1');
        const jobTitle2 = localStorage.getItem('selectedJobTitle2');
        if (jobTitle1) {
          this.selectedJobTitle1 = jobTitle1;
        }
        if (jobTitle2) {
          this.selectedJobTitle2 = jobTitle2;
        }
      }
    }
  };
  </script>
  
  <style>
  .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 800px; /* 设置容器的最大宽度 */
    margin: 0 auto; /* 水平居中 */
  }
  
  .select1,
  .select2 {
    width: 31%; /* 设置选择框的宽度 */
  }
  
  .search-button {
    width: 15%; /* 设置按钮的宽度 */
  }
  </style>
  