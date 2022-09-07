<template>
  <main >
    <nav>
      <ul>
        <li>
          <router-link to="/">Main</router-link>
        </li>
        <li>
          <router-link to="/scenarios">Scenarios</router-link>
        </li>
        <li>
          <router-link to="/about">About</router-link>
        </li>
        <li>
          <router-link to="/logout">Logout</router-link>
        </li>
      </ul>
    </nav>
    <router-view></router-view>
    <h1>{{ error }}</h1>
  </main>
</template>

<script>
import { computed } from "vue";
import apiCon from "./api/apiService";
import auth from "./cognito/auth";

export default {
  name: "App",

  data() {
    return {
      user: null,
      error: "",
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
          average: [
            { x: 0, y: 95558.81 },
            { x: 1, y: 142808.22 },
            { x: 2, y: 182994.41 },
            { x: 3, y: 280696.84 },
            { x: 4, y: 464808.2 },
            { x: 5, y: 849719.23 },
            { x: 6, y: 668144.78 },
            { x: 7, y: 983963.42 },
            { x: 8, y: 1640682.19 },
            { x: 9, y: 1598690.03 },
            { x: 10, y: 1987343.26 },
            { x: 11, y: 2334310.32 },
            { x: 12, y: 2760821.89 },
            { x: 13, y: 3578056.79 },
            { x: 14, y: 4108642.83 },
            { x: 15, y: 5099668.57 },
            { x: 16, y: 6872762.97 },
            { x: 17, y: 8297149.74 },
            { x: 18, y: 8925869.87 },
            { x: 20, y: 10619120.47 },
            { x: 21, y: 11098883.61 },
            { x: 22, y: 13184032.8 },
            { x: 23, y: 17283873.78 },
            { x: 24, y: 17320069.38 },
            { x: 25, y: 18673013.19 },
            { x: 26, y: 19587814.84 },
            { x: 27, y: 24441086.45 },
            { x: 28, y: 28090644.22 },
            { x: 29, y: 35096166.79 },
            { x: 30, y: 36318168.67 },
            { x: 31, y: 38407833.86 },
            { x: 32, y: 39595102.68 },
            { x: 33, y: 55075926.13 },
            { x: 34, y: 49433165 },
            { x: 35, y: 49436973.77 },
            { x: 36, y: 51297232.02 },
            { x: 37, y: 43805045.94 },
            { x: 38, y: 49987896.01 },
            { x: 39, y: 47204667.83 },
            { x: 40, y: 47935419.03 },
          ],
          worst: [
            { x: 0, y: 91574.45 },
            { x: 1, y: 146491.82 },
            { x: 2, y: 204761.33 },
            { x: 3, y: 363471.51 },
            { x: 4, y: 564231.79 },
            { x: 5, y: 675002.55 },
            { x: 6, y: 914190.07 },
            { x: 7, y: 980809.1 },
            { x: 8, y: 980472.87 },
            { x: 9, y: 1064245.41 },
            { x: 10, y: 1342159.24 },
            { x: 11, y: 1505328.26 },
            { x: 12, y: 1965708.56 },
            { x: 13, y: 1892654.99 },
            { x: 14, y: 1936377.89 },
            { x: 15, y: 2335647.53 },
            { x: 16, y: 3537755.18 },
            { x: 17, y: 4058018.17 },
            { x: 18, y: 5531765.7 },
            { x: 19, y: 4926788.42 },
            { x: 20, y: 6248786.06 },
            { x: 21, y: 6473348.33 },
            { x: 22, y: 6450315.36 },
            { x: 23, y: 6258937.42 },
            { x: 24, y: 5594972.87 },
            { x: 25, y: 5266799.28 },
            { x: 26, y: 4062404.09 },
            { x: 26, y: 2879154.72 },
            { x: 27, y: 3843414.24 },
            { x: 28, y: 4766361.16 },
            { x: 29, y: 4093693.22 },
            { x: 30, y: 2999849.85 },
            { x: 31, y: 3930240.23 },
            { x: 32, y: 4332802.05 },
            { x: 33, y: 3725599.57 },
            { x: 34, y: 4054316.18 },
            { x: 35, y: 4273985.4 },
            { x: 36, y: 4754729.54 },
            { x: 37, y: 5073648.74 },
            { x: 38, y: 4402534.04 },
          ],
          best: [
            { x: 0, y: 105716.57 },
            { x: 1, y: 187700.07 },
            { x: 2, y: 317680.02 },
            { x: 3, y: 358021.67 },
            { x: 4, y: 513203.1 },
            { x: 5, y: 734559.39 },
            { x: 6, y: 1090019.8 },
            { x: 7, y: 1386521.46 },
            { x: 8, y: 1955419.52 },
            { x: 9, y: 2284976.31 },
            { x: 10, y: 2511832.98 },
            { x: 11, y: 2283719.53 },
            { x: 12, y: 2078168.75 },
            { x: 13, y: 2750748.08 },
            { x: 14, y: 3589289.01 },
            { x: 15, y: 4722436.44 },
            { x: 16, y: 4886611.73 },
            { x: 17, y: 6051172.74 },
            { x: 18, y: 8008126.02 },
            { x: 19, y: 8907404.43 },
            { x: 20, y: 10471846.51 },
            { x: 21, y: 13379783.62 },
            { x: 22, y: 19023405.36 },
            { x: 23, y: 22674820.05 },
            { x: 24, y: 22641138.97 },
            { x: 25, y: 29328702.56 },
            { x: 26, y: 39120431.57 },
            { x: 27, y: 46182530.74 },
            { x: 28, y: 52833900.58 },
            { x: 29, y: 80470096.89 },
            { x: 30, y: 96034523.12 },
            { x: 31, y: 132532815.51 },
            { x: 32, y: 198159734.33 },
            { x: 33, y: 231351252.81 },
            { x: 34, y: 246098719.38 },
            { x: 35, y: 246325847.69 },
            { x: 36, y: 334851017.77 },
            { x: 37, y: 351410432.35 },
            { x: 38, y: 378755349.58 },
            { x: 39, y: 453894292.9 },
          ],
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
          average: [
            { x: 37, y: 351410432.35 },
            { x: 38, y: 378755349.58 },
            { x: 39, y: 453894292.9 },
          ],
          worst: [
            { x: 29, y: 80470096.89 },
            { x: 30, y: 96034523.12 },
            { x: 31, y: 132532815.51 },
            { x: 32, y: 198159734.33 },
          ],
          best: [
            { x: 21, y: 13379783.62 },
            { x: 22, y: 19023405.36 },
            { x: 23, y: 22674820.05 },
            { x: 24, y: 22641138.97 },
          ],
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

  computed: {
    bestData() {
      return this.scenarios[this.selectedScenarioIndex].best;
    },

    worstData() {
      return this.scenarios[this.selectedScenarioIndex].worst;
    },

    averageData() {
      return this.scenarios[this.selectedScenarioIndex].average;
    },
  },

  watch: {
    $route(to, from) {
      if (to.fullPath === "/" && to.fullPath === from.fullPath) {
        console.log("TRYING TO REFRESH THROUGH WATCHING");
        this.refreshData();
      }
    },
  },

  mounted() {
    if (auth.isTokenHere()) {
      console.log("TRYING TO REFRESH THROUGH MOUNTING");
      this.refreshData();
    }
  },

  methods: {
    refreshData() {
      this.updateUserData();
    },

    updateUserData() {
      apiCon.getUser().then((data) => {
        this.user = data;
        if (data === apiCon.userError) {
          this.error = data;
        } else if (
          Object.prototype.hasOwnProperty.call(data, "stockAllocation")
        ) {
          this.user.stockAllocation = parseFloat(this.user.stockAllocation);
        }
      });
    },

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

  provide() {
    return {
      user: computed(() => this.user),
      updateUserStockAllocation: this.updateUserStockAllocation,
      updateUserRetirementAge: this.updateUserRetirementAge,
      updateUserCurrentAge: this.updateUserCurrentAge,
      updateUserPrinciple: this.updateUserPrinciple,

      bestData: computed(() => this.bestData),
      worstData: computed(() => this.worstData),
      averageData: computed(() => this.averageData),

      scenarios: computed(() => this.scenarios),
      updateSelectedScenario: this.updateSelectedScenario,
      patchScenario: this.patchScenario,
      deleteScenario: this.deleteScenario,
      selectedScenarioIndex: computed(() => this.selectedScenarioIndex),
      addScenario: this.addScenario,
    };
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

li {
  display: inline-block;
  margin-left: 5rem;
}
</style>

