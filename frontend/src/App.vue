<template>
  <main v-if="getScenarioError.length === 0 && getUserError.length === 0">
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
  </main>
  <div v-else>
    <div v-if="getScenarioError.length > 0">
      {{ getScenarioError }}
    </div>
    <div v-if="getUserError.length > 0">
      {{ getUserError }}
    </div>
  </div>
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
      getScenarioError: "",
      getUserError: "",
      selectedScenarioIndex: 0,
      scenarios: null,
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
        this.refreshData();
      }
    },
  },

  mounted() {
    if (auth.isTokenHere()) {
      this.refreshData();
    }
  },

  methods: {
    refreshData() {
      this.getUser();
      this.getScenarios();
    },

    getScenarios() {
      apiCon.getScenarios().then((data) => {
        if (data === apiCon.scenariosError) {
          this.getScenarioError = data;
        } else {
          this.scenarios = data;
        }
      });
    },

    getUser() {
      apiCon.getUser().then((data) => {
        if (data === apiCon.userError) {
          this.getUserError = data;
        } else {
          this.user = data;
        }

        if (Object.prototype.hasOwnProperty.call(data, "stockAllocation")) {
          this.user.stockAllocation = parseFloat(this.user.stockAllocation);
        }
      });
    },

    patchUser(patchValues) {
      if (Object.keys(patchValues).length === 0) {
        alert("No fields were changed, so there is nothing to update.");
        return;
      }

      apiCon.patchUser(patchValues).then((data) => {
        if (data === apiCon.userPatchError) {
          alert(data);
        } else {
          alert("User updated!");
        }
      });
    },

    updateSelectedScenario(newIndex) {
      this.selectedScenarioIndex = newIndex;
    },

    patchScenario(index, patchValues) {
      const scenario = this.scenarios[index];
      // if the patchValues contains a scenario id, this is a patch on an existing scenario
      if (Object.prototype.hasOwnProperty.call(scenario, "ScenarioId")) {
        apiCon.patchScenario(scenario.ScenarioId, patchValues).then((data) => {
          if (data === apiCon.scenarioPatchError) {
            alert(data);
          } else {
            this.scenarios[index] = data;
            this.selectedScenarioIndex = index;
            alert("Scenario updated!");
          }
        });
      } else {
        apiCon.postScenario(patchValues).then((data) => {
          if (data === apiCon.scenarioPostError) {
            alert(data);
          } else {
            console.log(data);
            this.scenarios[index] = data;
            this.selectedScenarioIndex = index;
            alert("Scenario posted!");
          }
        });
      }
    },

    deleteScenario(index) {
      const scenarioId = this.scenarios[index];
      apiCon.deleteScenario(scenarioId).then((data) => {
        if (data === apiCon.scenarioDeleteError) {
          alert(data);
        } else {
          this.scenarios.splice(index, 1);
          alert("Scenario Deleted");
        }
      });
      
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
  },

  provide() {
    return {
      user: computed(() => this.user),
      patchUser: this.patchUser,

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

