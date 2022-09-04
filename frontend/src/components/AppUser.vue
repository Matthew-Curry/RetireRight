<template>
  <section class="base">
    <h2>{{ username }}</h2>
    <div class="form-control">
      <label for="localCurrentAge">Current Age </label>
      <input
        id="localCurrentAge"
        name="localCurrentAge"
        type="number"
        v-model="localCurrentAge"
        @input="updateChangedFields('localCurrentAge')"
      />
    </div>

    <div class="form-control">
      <label for="localRetirementAge">Retirement Age </label>
      <input
        id="localRetirementAge"
        name="localRetirementAge"
        type="number"
        v-model="localRetirementAge"
        @input="updateChangedFields('localRetirementAge')"
      />
    </div>

    <div class="form-control">
      <label for="localPrinciple">Principle </label>
      <input
        id="localPrinciple"
        name="localPrinciple"
        type="number"
        v-model="localPrinciple"
        @input="updateChangedFields('localPrinciple')"
      />
    </div>

    <div class="form-control">
      <label for="localStockAllocation">Stock Allocation </label>
      <input
        id="localStockAllocation"
        name="localStockAllocation"
        type="number"
        v-model="localStockAllocation"
        @input="updateChangedFields('localStockAllocation')"
      />
    </div>
    <button
      class="saveButton"
      @mouseenter="updateSaveHovered"
      @mouseleave="updateSaveHovered"
      @click="submitForm"
      :class="{ darkSaveButton: saveHovered }"
    >
      Update User
    </button>
  </section>
</template>

<script>
export default {
  props: {
    username: {
      type: String,
      required: true,
    },

    stockAllocation: {
      type: Number,
      required: true,
    },

    retirementAge: {
      type: Number,
      required: true,
    },

    currentAge: {
      type: Number,
      required: true,
    },

    principle: {
      type: Number,
      required: true,
    },
  },

  emits: ["updated-stock-allocation", "updated-retirement-age", "updated-current-age", "updated-principle"],

  data() {
    return {
      localStockAllocation: null,
      localRetirementAge: null,
      localCurrentAge: null,
      localPrinciple: null,

      changedFields: [],
      saveHovered: false,
      eventMap: {
        "localStockAllocation": "updated-stock-allocation",
        "localRetirementAge": "updated-retirement-age",
        "localCurrentAge": "updated-current-age",
        "localPrinciple": "updated-principle",
      }
    };
  },

  beforeMount() {
    this.localStockAllocation = this.stockAllocation;
    this.localRetirementAge = this.retirementAge;
    this.localCurrentAge = this.currentAge;
    this.localPrinciple = this.principle;
  },

  methods: {
    updateChangedFields(field) {
      this.changedFields.push(field);
    },

    updateSaveHovered() {
      this.saveHovered = !this.saveHovered;
    },

    submitForm() {
      // emit events for each changed field
      console.log("the changed fields")
      console.log(this.changedFields)
      for (const field of this.changedFields) {
        const eventName = this.eventMap[field]
        const value = this.$data[field]
        this.$emit(eventName, value);
      }

      this.changedFields = [];
    },

  },
};
</script>

<style scoped>
.base {
  margin: 2rem auto;
  max-width: 30rem;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  background-color: rgba(14, 14, 34, 0.795);
  color: aliceblue;
}

.form-control {
  margin: 0.5rem 0;
}

.saveButton {
  font: inherit;
  border: 1px solid #0076bb;
  background-color: #0076bb;
  color: white;
  cursor: pointer;
  padding: 0.75rem 2rem;
  border-radius: 30px;
  margin: 5px;
}

.darkSaveButton {
  border: 1px solid #021c72;
  background-color: #021c72;
}
</style>