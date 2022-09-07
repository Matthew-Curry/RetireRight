<template>
  <div>
    <h1>Scenarios</h1>
    <div>
      <ul v-if="scenarios.value">
        <app-scenario
          v-for="(sourceData, index) in scenarios.value"
          :key="index"
          @selected="updateSelectedScenario"
          @scenario-form-submitted="patchScenario"
          @deleted="deleteScenario"
          :currentAge="user.value.currentAge"
          :scenarioIndex="index"
          :isSelected="index === selectedScenarioIndex.value"
          :sourceData="sourceData"
        >
        </app-scenario>
      </ul>
      <loadingScenario v-else></loadingScenario>
    </div>
    <button @click="addScenario">Add Scenario</button>
  </div>
</template>

<script>
import AppScenario from "../core/AppScenario.vue";
import LoadingScenario from "../core/LoadingScenario.vue";

export default {
  name: "App",

  components: {
    "app-scenario": AppScenario,
    loadingScenario: LoadingScenario
  },

  inject: [
    "user",
    "scenarios",
    "updateSelectedScenario",
    "patchScenario",
    "deleteScenario",
    "selectedScenarioIndex",
    "addScenario",
    "savingScenario"
  ],
};
</script>
