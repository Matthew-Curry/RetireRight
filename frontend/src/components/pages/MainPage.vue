<template>
  <div>
    <h1>RetireRight</h1>
    <p>
      Select a scenario to view the resulting net asset growth in the chart.
      Select "Scenarios" to view, edit, and add scenarios, as well as to see the
      probability of success for each. More information can be found on the
      "About" page.
    </p>
    <div v-if="user.value" style="float: right">
      <user
        :key="userRefreshKey.value"
        :username="user.value.UserName"
        :stockAllocation="user.value.stockAllocation"
        :retirementAge="user.value.retirementAge"
        :currentAge="user.value.currentAge"
        :principle="user.value.principle"
        @user-form-submitted="patchUser"
      ></user>
      <label id="dropdown" for="scenarios">Choose a Scenario:</label>
      <select
        :value="selectedScenarioIndex.value"
        name="scenarios"
        id="scenarios"
        @change="updateSelectedScenario(parseInt($event.target.value))"
      >
        <option
          v-for="(sourceData, index) in scenarios.value"
          :key="index"
          :value="index"
        >
          Scenario {{ index + 1 }}
        </option>
      </select>
    </div>
    <loadingUser v-else></loadingUser>
    <chart
      v-if="scenarios.value"
      :key="selectedScenarioIndex.value"
      :targetLine="targetLine.value"
      :bestData="bestData.value"
      :worstData="worstData.value"
      :averageData="averageData.value"
    ></chart>
    <loadingScenario v-else></loadingScenario>
  </div>
</template>

<script>
import AppUser from "../core/AppUser.vue";
import TheChart from "../core/TheChart.vue";
import LoadingUser from "../core/LoadingUser.vue";
import LoadingScenario from "../core/LoadingScenario.vue";

export default {
  name: "App",

  components: {
    user: AppUser,
    chart: TheChart,
    loadingUser: LoadingUser,
    loadingScenario: LoadingScenario,
  },

  inject: [
    "scenarios",
    "updateSelectedScenario",
    "selectedScenarioIndex",
    "user",
    "patchUser",
    "userRefreshKey",

    "bestData",
    "worstData",
    "averageData",
    "targetLine",
  ],
};
</script>

<style scoped>
#dropdown {
  font-size: 1.5em;
}
</style>