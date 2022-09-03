<template>
  <div>
    <h1>RetireRight</h1>
    <h2>
      Click on a scenario to see/change it and view the resulting net asset
      growth in the chart.
    </h2>
    <user></user>
    <ul>
      <app-scenario
        v-for="(sourceData, index) in scenarios"
        @selected="updateSelectedScenario"
        @form-submitted="patchScenario"
        @deleted="deleteScenario"
        :key="index"
        :scenarioIndex="index"
        :isSelected="index === selectedScenarioIndex"
        :sourceData="sourceData"
      >
      </app-scenario>
    </ul>
    <chart></chart>
  </div>
</template>

<script>
import AppScenario from "./components/AppScenario.vue";
import AppUser from "./components/AppUser.vue";
import TheChart from "./components/TheChart.vue";

export default {
  name: "App",

  components: {
    "app-scenario": AppScenario,
    user: AppUser,
    chart: TheChart,
  },

  data() {
    return {
      selectedScenarioIndex: 0,
      scenarios: [
        {
          percentSuccess: 0.7,
          rent: 500,
          food: 200,
          entertainment: 200,
          yearlyTravel: 3000,
          ageHome: 34,
          homeCost: 200000,
          downpaymentSavings: 0,
          mortgageRate: 0.06,
          mortgageLength: 15,
          ageKids: [34, 35, 36]
        },
        {
          percentSuccess: 0.8,
          rent: 500,
          food: 200,
          entertainment: 200,
          yearlyTravel: 3000,
          ageHome: 34,
          homeCost: 200000,
          downpaymentSavings: 0,
          mortgageRate: 0.06,
          mortgageLength: 15,
          ageKids: [34, 35, 36]
        },
        {
          percentSuccess: 0.9,
          rent: 500,
          food: 200,
          entertainment: 200,
          yearlyTravel: 3000,
          ageHome: 34,
          homeCost: 200000,
          downpaymentSavings: 0,
          mortgageRate: 0.06,
          mortgageLength: 15,
          ageKids: [34, 35, 36]
        },
        {
          percentSuccess: 0.95,
          rent: 500,
          food: 200,
          entertainment: 200,
          yearlyTravel: 3000,
          ageHome: 34,
          homeCost: 200000,
          downpaymentSavings: 0,
          mortgageRate: 0.06,
          mortgageLength: 15,
          ageKids: [34, 35, 36]
        },
        {
          percentSuccess: 0.4,
          rent: 500,
          food: 200,
          entertainment: 200,
          yearlyTravel: 3000,
          ageHome: 34,
          homeCost: 200000,
          downpaymentSavings: 0,
          mortgageRate: 0.06,
          mortgageLength: 15,
          ageKids: [34, 35, 36]
        },
      ],
    };
  },

  methods: {
    updateSelectedScenario(newIndex) {
      this.selectedScenarioIndex = newIndex;
    },

    patchScenario(index, patchValues) {
      for (let field in patchValues) {
        this.scenarios[index][field] = patchValues[field];
      }

      alert("Scenario updated!")
    },

    deleteScenario(index) {
      this.scenarios.splice(index,1);
    }
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
