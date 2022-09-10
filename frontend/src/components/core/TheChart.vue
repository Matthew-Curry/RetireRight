<template>
  <div>
    <canvas id="the-chart"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js";

export default {
  props: {
    bestData: {
      type: Array,
      required: true,
    },

    worstData: {
      type: Array,
      required: true,
    },

    averageData: {
      type: Array,
      required: true,
    },

    targetValue: {
      type: Number,
      required: true,
    },
  },

  data() {
    return {
      chartData: {
        type: "scatter",
        data: {
          datasets: [
            {
              label: "Best",
              data: null,
              borderColor: "rgba(71, 183,132,.5)",
              borderWidth: 3,
              showLine: true,
              fill: false,
            },
            {
              label: "Worst",
              data: null,
              borderColor: "rgba(255, 76, 48, 1)",
              borderWidth: 3,
              showLine: true,
              fill: false,
            },
            {
              label: "Average",
              data: null,
              borderColor: "rgba(243, 225, 107)",
              borderWidth: 3,
              maxHeight: 40,
              showLine: true,
              fill: false,
            },
          ],
        },
        options: {
          scales: {
            yAxes: [
              {
                scaleLabel: {
                  display: true,
                  labelString: "Net Worth",
                  fontSize: 40,
                },
              },
            ],
            xAxes: [
              {
                scaleLabel: {
                  display: true,
                  labelString: "Years Until Retirement",
                  fontSize: 40,
                },
              },
            ],
          },
          legend: {
            display: true,
            position: "top",
            labels: {
              fontFamily: "Comic Sans MS",
              fontSize: 25,
            },
          },
        },
      },
    };
  },

  beforeMount() {
    this.chartData.data.datasets[0].data = this.bestData;
    this.chartData.data.datasets[1].data = this.worstData;
    this.chartData.data.datasets[2].data = this.averageData;
  },

  watch: {
    bestData() {
      this.chartData.data.datasets[0].data = this.bestData;
      this.createChart();
    },

    worstData() {
      this.chartData.data.datasets[1].data = this.worstData;
      this.createChart();
    },

    averageData() {
      this.chartData.data.datasets[2].data = this.averageData;
      this.createChart();
    },
  },

  mounted() {
    this.createChart();
  },

  methods: {
    createChart() {
      const ctx = document.getElementById("the-chart");
      new Chart(ctx, this.chartData);
    },

    buildTargetLine() {

    }
  }
};
</script>

<style>
canvas {
  width: 75% !important;
  height: 600px !important;
}
</style>
