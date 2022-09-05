<template>
  <div>
    <h1>RetireRight</h1>
    <p>
      Select a scenario to view the resulting net asset growth in the chart. Select "Scenarios" to
      view, edit, and add scenarios, as well as to see the probability of success for each. More information
      can be found on the "About" page.
    </p>
    <div style="float: right">
      <user
        :username="user.value.username"
        :stockAllocation="user.value.stockAllocation"
        :retirementAge="user.value.retirementAge"
        :currentAge="user.value.currentAge"
        :principle="user.value.principle"
        @updated-stock-allocation="updateUserStockAllocation"
        @updated-retirement-age="updateUserRetirementAge"
        @updated-current-age="updateUserCurrentAge"
        @updated-principle="updateUserPrinciple"
      ></user>
    </div>
    <chart
      :bestData="bestData.value"
      :worstData="worstData.value"
      :averageData="averageData.value"
    ></chart>
  </div>
</template>

<script>
import AppUser from "../domain/AppUser.vue";
import TheChart from "../domain/TheChart.vue";

export default {
  name: "App",

  components: {
    'user': AppUser,
    'chart': TheChart,
  },

  inject: [
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
