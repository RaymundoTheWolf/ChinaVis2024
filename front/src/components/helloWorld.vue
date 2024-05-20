
<template>
  <div id="index" ref="appRef">
    <dv-full-screen-container class="bg">
      <!-- 顶部title部分 -->
      <top-header />
      <div class="fir">
        <!-- 第一行 -->
            <!-- 发展动态 -->
            <div class="fir_box1">
              <dv-border-box-12 style="padding-top: 10px">
                <h1>发展动态</h1>
              </dv-border-box-12>
            </div>
            <!-- 地区画像 -->
            <div class="fir_box2">
              <dv-border-box-12>
                <h1>地区画像</h1>
              </dv-border-box-12>
            </div>
            <!-- 学历3D图 -->
          <div class="fir_box3">
            <dv-border-box-12 style="padding-top: 10px">
                <scatterChart/>
            </dv-border-box-12>
          </div>
      </div>
      <div class="sec">
        <!-- 第二行 -->
            <!-- 地区大图 -->
            <div class="sec_box1">
              <dv-border-box-12>
                <map-chart/>
              </dv-border-box-12>
            </div>
            <!-- 行业大图 -->
            <div class="sec_box2">
              <dv-border-box-12 style="padding-top: 10px">
                <title-chart/>
              </dv-border-box-12>
            </div>
      </div>
      <div class="thr">
        <!-- 第三行 -->
            <!-- 未知图 -->
            <div class="thr_box1">
              <dv-border-box-12>
                <radar-chart/>
              </dv-border-box-12>
            </div>
            <!-- 职位分析图 -->
            <div class="thr_box2">
              <dv-border-box-12 style="padding-top: 10px">
                <job-detail-chart/>
              </dv-border-box-12>
            </div>
            <!-- 平行坐标图 -->
            <div class="thr_box3">
              <dv-border-box-12 style="padding-top: 10px">
                <parallel-chart/>
              </dv-border-box-12>
            </div>
      </div>
    </dv-full-screen-container>
  </div>
</template>


<script>
import topHeader from "./topHeader.vue";
import parallelChart from "./parallelChart.vue";
import scatterChart from "./scatterChart.vue";
import mapChart from "./mapChart.vue";
import titleChart from "./titleChart.vue";
import jobDetailChart from "./ jobDetailChart.vue";
import radarChart from "./radar.vue"
export default {
  components: {
    topHeader,
    parallelChart,
    scatterChart,
    mapChart,
    titleChart,
    jobDetailChart,
    radarChart
},
  data () {
    return {}
  },
  methods: {}
}

</script>


<style>

* {
  margin: 0;
  padding: 0;
  list-style-type: none;
  outline: none;
  box-sizing: border-box;
}
html {
  margin: 0;
  padding: 0;
}
body {
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.2em;
  background-color: #f1f1f1;
  margin: 0;
  padding: 0;
}
a {
  color: #343440;
  text-decoration: none;
}
#index {
  color: #d3d6dd;
  width: 1920px;
  height: 1080px;
  position: absolute;
  background-color: #030409;
  color: #fff;
}

#index .bg {
  /* 整体页面背景 */
  background-image: url('../assets/img/bg.png');
  background-size: 100% 100%;
  box-shadow: 0 0 3px blue;
  display: flex;
  flex-direction: column;
}


#index .fir {
  height: 30%;
  width: 100%;
  display: flex;
  flex-direction: row;
}

#index .sec {
  height: 40%;
  width: 100%;
  display: flex;
  flex-direction: row;
}

#index .thr {
  height: 30%;
  width: 100%;
  display: flex;
  flex-direction: row;
}
#index .fir_box1 {
  height: 100%;
  width: 20%;
}
#index .fir_box2 {
  height: 100%;
  width: 60%;
}
#index .fir_box3 {
  height: 100%;
  width: 20%;
}
#index .sec_box1 {
  height: 100%;
  width: 50%;
}
#index .sec_box2 {
  height: 100%;
  width: 50%;
}
#index .thr_box1 {
  height: 100%;
  width: 20%;
}
#index .thr_box2 {
  height: 100%;
  width: 50%;
}
#index .thr_box3 {
  height: 100%;
  width: 30%;
}

</style>