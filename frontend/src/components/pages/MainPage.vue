<template>
  <div>
    <h1>RetireRight</h1>
    <p>
      Select a scenario to view the resulting net asset growth in the chart.
      Select "Scenarios" to view, edit, and add scenarios, as well as to see the
      probability of success for each. More information can be found on the
      "About" page.
    </p>
    <div style="float: right">
      <user
        :username="user.value.UserName"
        :stockAllocation="user.value.stockAllocation"
        :retirementAge="user.value.retirementAge"
        :currentAge="user.value.currentAge"
        :principle="user.value.principle"
        @updated-stock-allocation="updateUserStockAllocation"
        @updated-retirement-age="updateUserRetirementAge"
        @updated-current-age="updateUserCurrentAge"
        @updated-principle="updateUserPrinciple"
      ></user>
      <label id="dropdown" for="scenarios">Choose a Scenario:</label>
      <select :value="selectedScenarioIndex.value" name="scenarios" id="scenarios" @change="updateSelectedScenario(parseInt($event.target.value))">
        <option
          v-for="(sourceData, index) in scenarios.value"
          :key="index"
          :value="index"
        >
          Scenario {{ index + 1 }}
        </option>
      </select>
    </div>
    <chart
      :key="selectedScenarioIndex.value"
      :bestData="bestData.value"
      :worstData="worstData.value"
      :averageData="averageData.value"
    ></chart>
  </div>
</template>

<script>
import AppUser from "../core/AppUser.vue";
import TheChart from "../core/TheChart.vue";

import UserInfoStore from '../../cognito/user-info-store';

export default {
  name: "App",

  data() {
    return {
      userInfo: UserInfoStore.state,
    }
  },

  components: {
    user: AppUser,
    chart: TheChart,
  },

  inject: [
    "scenarios",
    "updateSelectedScenario",
    "selectedScenarioIndex",
    "user",
    "updateUserStockAllocation",
    "updateUserRetirementAge",
    "updateUserCurrentAge",
    "updateUserPrinciple",

    "bestData",
    "worstData",
    "averageData",
  ],
};
</script>

<style scoped>
#dropdown {
  font-size: 1.5em;
}



</style>