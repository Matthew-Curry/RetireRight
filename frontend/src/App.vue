<template>
  <div>
    <h1>RetireRight</h1>
    <h2>
      Click on a scenario to see/change it and view the resulting net asset
      growth in the chart.
    </h2>
    <user
      :username="user.username"
      :stockAllocation="user.stockAllocation"
      :retirementAge="user.retirementAge"
      :currentAge="user.currentAge"
      :principle="user.principle"

      @updated-stock-allocation="updateUserStockAllocation"
      @updated-retirement-age="updateUserRetirementAge"
      @updated-current-age="updateUserCurrentAge"
      @updated-principle="updateUserPrinciple"
    ></user>
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
    <button v-if="scenarios.length < 5" @click="addScenario">
      Add Scenario
    </button>
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
      user: {
        username: "Matt",
        stockAllocation: 0.7,
        retirementAge: 55,
        currentAge: 25,
        principle: 3000,
      },
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
          ageKids: [34, 35, 36],
          incomeInc: { 25: 120000, 30: 200000 },
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
          ageKids: [34, 35, 36],
          incomeInc: { 25: 120000, 30: 200000 },
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
          ageKids: [34, 35, 36],
          incomeInc: { 25: 120000, 30: 200000 },
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
          ageKids: [34, 35, 36],
          incomeInc: { 25: 120000, 30: 200000 },
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
          ageKids: [34, 35, 36],
          incomeInc: { 25: 120000, 30: 200000 },
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

      alert("Scenario updated!");
    },

    deleteScenario(index) {
      this.scenarios.splice(index, 1);
    },

    addScenario() {
      this.scenarios.push({
        percentSuccess: null,
        rent: null,
        food: null,
        entertainment: null,
        yearlyTravel: null,
        ageHome: null,
        homeCost: null,
        downpaymentSavings: null,
        mortgageRate: null,
        mortgageLength: null,
        ageKids: [],
        incomeInc: {},
      });

      this.selectedScenarioIndex = this.scenarios.length - 1;
    },

    updateUserStockAllocation(newVal) {
      this.user.stockAllocation = newVal;
    },

    updateUserRetirementAge(newVal) {
      this.user.retirementAge = newVal;
    },

    updateUserCurrentAge(newVal) {
      this.user.currentAge = newVal;
    },

    updateUserPrinciple(newVal) {
      this.user.principle = newVal;
    },
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

button {
  font: inherit;
  border: 1px solid #0076bb;
  background-color: #0076bb;
  color: white;
  cursor: pointer;
  padding: 0.75rem 2rem;
  border-radius: 30px;
  margin: 5px;
}
</style>
