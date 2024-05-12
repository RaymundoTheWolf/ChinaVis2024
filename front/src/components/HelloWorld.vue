<template>
  <dv-full-screen-container>
    <top-header />
    <div class="chart-container">
      <mapChart class="map_chart"/> 
      <titleChart class="title-chart"/>
    </div>
  </dv-full-screen-container>
  
</template>

<script>
import mapChart from './mapChart.vue'; 
import titleChart from './titleChart.vue'
import topHeader from './topHeader.vue'

export default {
  components: {
    mapChart,
    titleChart,
    topHeader
  },
}
</script>

<style scoped>
.chart-container {
  display: flex;
  align-items: center;
}

.map_chart {
  width: 50%; 
  height: 1000px;
  margin-left: -100px;
}

.title-chart {
  width: 50%;
  height: 800px;
}
</style>
