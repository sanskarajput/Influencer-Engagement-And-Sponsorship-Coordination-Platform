<template>
  <canvas ref="chartCanvas" id="myAreaChart"></canvas>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'EarningsAreaChart',
  props: {
    labels: {
      type: Array,
      default: () => ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    },
    data: {
      type: Array,
      default: () => [0, 10000, 5000, 15000, 10000, 20000, 15000, 25000, 20000, 30000, 25000, 40000]
    },
    chartTitle: {
      type: String,
      default: 'Investments',
    }
  },
  data() {
    return {
      chart: null
    }
  },
  methods: {
    number_format(number, decimals, dec_point, thousands_sep) {
      number = (number + '').replace(',', '').replace(' ', '');
      var n = !isFinite(+number) ? 0 : +number,
        prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
        sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
        dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
        s = '',
        toFixedFix = function(n, prec) {
          var k = Math.pow(10, prec);
          return '' + Math.round(n * k) / k;
        };
      
      s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
      if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
      }
      if ((s[1] || '').length < prec) {
        s[1] = s[1] || '';
        s[1] += new Array(prec - s[1].length + 1).join('0');
      }
      return s.join(dec);
    },
    createChart() {
      // Destroy existing chart if it exists
      if (this.chart) {
        this.chart.destroy();
      }

      const ctx = this.$refs.chartCanvas;
      
      // Set global defaults
      Chart.defaults.font.family = 'Nunito, -apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
      Chart.defaults.color = '#858796';

      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.labels,
          datasets: [{
            label: this.chartTitle,
            tension: 0.3,
            borderColor: "rgba(78, 115, 223, 1)",
            pointRadius: 3  ,
            pointBackgroundColor: "rgba(78, 115, 223, 1)",
            pointBorderColor: "rgba(78, 115, 223, 1)",
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "black",
            pointHoverBorderColor: "black",
            pointHitRadius: 10,
            pointBorderWidth: 2,
            data: this.data,
          }],
        },
        options: {
          maintainAspectRatio: false,
          layout: {
            padding: {
              left: 0,
              right: 2,
              top: 2,
              bottom: 0
            }
          },
          scales: {
            x: {
              grid: {
                display: false,
                drawBorder: false
              },
              ticks: {
                // maxTicksLimit: 10
              }
            },
            y: {
              beginAtZero: true,
              ticks: {
                maxTicksLimit: 15,   
                padding: 5,
                callback: function(value) {
                  return '₹ ' + this.number_format(value);
                }.bind(this)
              },
              grid: {
                color: "rgba(234, 236, 244, 0.5)",
                drawBorder: false,
              }
            }
          },
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              backgroundColor: "rgb(255,255,255)",
              bodyColor: "#00000f",
              titleColor: '#0000ff',
              titleSize: 14,
              borderColor: '#000000',
              borderWidth: 1,
              padding: {
                x: 15,
                y: 15
              },
              displayColors: false,
              mode: 'index',
              intersect: false,
              callbacks: {
                label: (context) => {
                  return `${context.dataset.label}: $${this.number_format(context.parsed.y)}`;
                }
              }
            }
          }
        }
      });
    }
  },
  mounted() {
    this.createChart();
  },
  watch: {
    // Recreate chart if props change
    labels() {
      this.createChart();
    },
    data() {
      this.createChart();
    }
  }
}
</script>

<style scoped>
canvas {
  width: 100%;
  height: 300px;
}
</style>