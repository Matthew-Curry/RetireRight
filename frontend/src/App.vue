<template>
  <main v-if="getScenarioError.length === 0 && getUserError.length === 0">
    <h1 v-if="updatingScenarios == true">Scenarios are currently updating with submitted user info..</h1> 
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
      userRefreshKey: 0,
      updatingScenarios: false,
      getScenarioError: "",
      getUserError: "",
      selectedScenarioIndex: 0,
      scenarios: null,
      savingScenario: false
    };
  },

  computed: {
    bestData() {
      if (!this.scenarios || this.scenarios.length === 0) {
        return []
      }

      return this.scenarios[this.selectedScenarioIndex].best;
    },

    worstData() {
      if (!this.scenarios || this.scenarios.length === 0) {
        return []
      }

      return this.scenarios[this.selectedScenarioIndex].worst;
    },

    averageData() {
      if (!this.scenarios || this.scenarios.length === 0) {
        return []
      }

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
    if (auth.isTokenValid()) {
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

      this.user.UserName = 'matt';
      let userPatchBody = JSON.parse(JSON.stringify(this.user)); 
      const userId = userPatchBody['UserId'];
      delete userPatchBody['UserId'];

      for (const [field, val] of Object.entries(patchValues)) {
        userPatchBody[field] = val
      }
      this.updatingScenarios = true;
      apiCon.patchUser(userPatchBody).then((data) => {
        if (data === apiCon.userPatchError) {
          this.updatingScenarios = false;
          this.userRefreshKey ++;
          alert(data);
        } else {
          userPatchBody['UserId'] = userId;
          this.user = userPatchBody;
          this.scenarios = data;
          this.updatingScenarios = false;
          this.userRefreshKey ++;
          alert("User updated and all scenarios have been re-simulated!");
        }
      });
      
    },

    updateSelectedScenario(newIndex) {
      this.selectedScenarioIndex = newIndex;
    },

    patchScenario(index, patchValues) {
      this.savingScenario = true;
      const scenario = this.scenarios[index];
      // if the patchValues contains a scenario id, this is a patch on an existing scenario
      if (Object.prototype.hasOwnProperty.call(scenario, "ScenarioId")) {
        apiCon.patchScenario(scenario.ScenarioId, patchValues).then((data) => {
          if (data === apiCon.scenarioPatchError) {
            alert(data);
          } else {
            this.scenarios[index] = data;
            this.selectedScenarioIndex = index;
            this.savingScenario = false;
            alert("Scenario updated!");
          }
        });
      } else {
        apiCon.postScenario(patchValues).then((data) => {
          if (data === apiCon.scenarioPostError) {
            alert(data);
          } else {
            this.scenarios[index] = data;
            this.selectedScenarioIndex = index;
            this.savingScenario = false;
            alert("Scenario posted!");
          }
        });
      }
    },

    deleteScenario(index) {
      const scenarioId = this.scenarios[index].ScenarioId;
      apiCon.deleteScenario(scenarioId).then((data) => {
        if (data === apiCon.scenarioDeleteError) {
          alert(data);
        } else {
          this.scenarios.splice(index, 1);
          this.selectedScenarioIndex = 0;
          alert("Scenario Deleted");
        }
      });
      
      this.scenarios.splice(index, 1);
    },

    addScenario() {
      if (this.scenarios.length === 15) {
        alert("Max of 15 scenarios allowed. Please delete or edit an existing scenario.");
        return;
      }

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
      userRefreshKey: computed(() => this.userRefreshKey),

      bestData: computed(() => this.bestData),
      worstData: computed(() => this.worstData),
      averageData: computed(() => this.averageData),

      scenarios: computed(() => this.scenarios),
      updateSelectedScenario: this.updateSelectedScenario,
      patchScenario: this.patchScenario,
      deleteScenario: this.deleteScenario,
      selectedScenarioIndex: computed(() => this.selectedScenarioIndex),
      addScenario: this.addScenario,
      savingScenario: computed(() => this.savingScenario)
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

