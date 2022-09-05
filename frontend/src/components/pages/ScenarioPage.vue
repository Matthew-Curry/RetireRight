<template>
  <div>
    <h1>Scenarios</h1>
    <div>
      <ul>
          <app-scenario
            v-for="(sourceData, index) in scenarios.value"
            :key="index"
            @selected="updateSelectedScenario"
            @form-submitted="patchScenario"
            @deleted="deleteScenario"
            :scenarioIndex="index"
            :isSelected="index === selectedScenarioIndex.value"
            :sourceData="sourceData"
          >
          </app-scenario>
      </ul>
    </div>
    <button @click="addScenario">
      Add Scenario
    </button>
  </div>
</template>

<script>
import AppScenario from "../domain/AppScenario.vue";

export default {
  name: "App",

  components: {
    'app-scenario': AppScenario
  },

  inject: [
    "scenarios",
    "updateSelectedScenario",
    "patchScenario",
    "deleteScenario",
    "selectedScenarioIndex",
    "addScenario"
  ],
};
</script>
