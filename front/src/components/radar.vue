<template>
    <div id="radar-chart">
        <div ref="radarChart" class="radarChart"></div>
    </div>
</template>
  
  <script>
  import * as echarts from 'echarts'; 
  import { EventBus } from './eventBus';
  
  export default {
    data() {
      return {
        jobTitles: [],
        skillPreference: [0.5, 0.5, 0.5],
        avgSkillPreference: [0.3, 0.3, 0.3],
      };
    },
    mounted() {
      this.radarChart = echarts.init(this.$refs.radarChart);
      this.renderRadarChart();
      EventBus.$on('radar-data', (data) => {
            this.avgSkillPreference = data.avgSkillPreference;
            this.skillPreference = data.skillPreference;
            this.renderRadarChart()
        });
    },
    methods: {
      renderRadarChart() {
        const option = {
          radar: {
            indicator: [
              { name: 'City', max: 1 },
              { name: 'Exp', max: 1 },
              { name: 'Edu', max: 1 },
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
    }
}
  </script>
  
<style>

#radar-chart{
    width: 100%;
    height: 100%;
}
  
  
#radar-chart .radarChart {
    width: 100%;
    height: 100%;
}

</style>
  
  