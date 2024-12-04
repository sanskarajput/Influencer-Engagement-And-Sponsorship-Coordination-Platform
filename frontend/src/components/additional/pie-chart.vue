<template>
    <div>
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import Chart from 'chart.js/auto'
  
  export default {
    name: 'PieChart',
    props: {
      // Existing props
      labels: {
        type: Array,
        default: () => ['Private', 'Public']
      },
      data: {
        type: Array,
        default: () => [50, 100]
      },
      backgroundColor: {
        type: Array,
        default: () => [
          'rgb(255, 99, 132)', 
          'rgb(54, 162, 235)', 
        ]
      },
      chartTitle: {
        type: String,
        default: 'Campaign\'s Visibility'
      },
      
      // New configuration props
      titleConfig: {
        type: Object,
        default: () => ({
          display: false,
          text: 'Pie Chart',
          padding: 5,
          font: {
            size: 16,
            weight: 'bold'
          }
        })
      },
      legendConfig: {
        type: Object,
        default: () => ({
          display: false,
          position: 'bottom',
          labels: {
            padding: 10,
            boxWidth: 20,
            boxHeight:5,
            boxRadius:10,
            font: {
              size: 10,
              weight: 'normal'
            }
          }
        })
      },
      layoutConfig: {
        type: Object,
        default: () => ({
          padding: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
          }
        })
      },
      responsiveConfig: {
        type: Object,
        default: () => ({
          maintainAspectRatio: false,
          responsive: true
        })
      }
    },
    data() {
      return {
        chartInstance: null
      }
    },
    mounted() {
      this.createChart()
    },
    methods: {
      createChart() {
        // Destroy existing chart if it exists
        if (this.chartInstance) {
          this.chartInstance.destroy()
        }
  
        // Create new chart with extended configuration
        this.chartInstance = new Chart(this.$refs.chartCanvas, {
          type: 'pie',
          data: {
            labels: this.labels,
            datasets: [{
              label: this.chartTitle,
              data: this.data,
              backgroundColor: this.backgroundColor,
              hoverOffset: 4
            }]
          },
          options: {
            // Spread configuration props
            plugins: {
              title: this.titleConfig,
              legend: this.legendConfig
            },
            layout: this.layoutConfig,
            ...this.responsiveConfig
          }
        })
      }
    },
    watch: {
      labels: 'createChart',
      data: 'createChart',
      backgroundColor: 'createChart',
      titleConfig: 'createChart',
      legendConfig: 'createChart',
      layoutConfig: 'createChart',
      responsiveConfig: 'createChart'
    },
    beforeUnmount() {
      // Ensure chart is destroyed when component is removed
      if (this.chartInstance) {
        this.chartInstance.destroy()
      }
    }
  }
  </script>
  
  <style scoped>
  canvas {
    max-width: 100%;
    height: 17.5rem;
  }
  </style>