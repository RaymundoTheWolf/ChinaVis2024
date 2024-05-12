<template>
  <div class="chart-container">
    <MapChart class="map_chart"/> 
    <titleChart class="title-chart"/>
  </div>
</template>

<script>
import MapChart from './MapChart.vue'; 
import titleChart from './titleChart.vue'

export default {
  components: {
    MapChart,
    titleChart 
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
}

.title-chart {
  width: 50%;
  height: 800px;
}
</style>
