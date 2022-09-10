<template>
  <section class="base">
    <h2>{{ username }}</h2>
    <div class="form-control">
      <label for="localCurrentAge">Current Age</label>
      <input
        id="localCurrentAge"
        name="localCurrentAge"
        type="number"
        min="0"
        step="1"
        v-model="localCurrentAge"
        @input="updateChangedFields('localCurrentAge')"
      />
    </div>

    <div class="form-control">
      <label for="localRetirementAge">Retirement Age</label>
      <input
        id="localRetirementAge"
        name="localRetirementAge"
        type="number"
        min="0"
        step="1"
        v-model="localRetirementAge"
        @input="updateChangedFields('localRetirementAge')"
        ref="localRetirementAge"
      />
    </div>

    <div class="form-control">
      <label for="localPrinciple">Principle</label>
      <input
        id="localPrinciple"
        name="localPrinciple"
        type="number"
        min="0"
        step="1"
        v-model="localPrinciple"
        @input="updateChangedFields('localPrinciple')"
        ref="localPrinciple"
      />
    </div>

    <div class="form-control">
      <label for="localStockAllocation">Stock Allocation</label>
      <input
        id="localStockAllocation"
        name="localStockAllocation"
        type="number"
        min="0"
        step="0.01"
        max="1"
        v-model="localStockAllocation"
        @input="updateChangedFields('localStockAllocation')"
        ref="localStockAllocation"
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

  emits: ["user-form-submitted"],

  data() {
    return {
      localStockAllocation: null,
      localRetirementAge: null,
      localCurrentAge: null,
      localPrinciple: null,

      changedFields: [],
      nameMap: {
        localStockAllocation: 'stockAllocation',
        localRetirementAge: 'retirementAge',
        localCurrentAge: 'currentAge',
        localPrinciple: 'principle',
      },
      saveHovered: false,
    };
  },

  beforeMount() {
    this.setAttr();
  },

  methods: {
    updateChangedFields(field) {
      if (!this.changedFields.includes(field)) {
        this.changedFields.push(field);
      }
    },

    setAttr() {
      this.localStockAllocation = this.stockAllocation;
      this.localRetirementAge = this.retirementAge;
      this.localCurrentAge = this.currentAge;
      this.localPrinciple = this.principle;
    },

    validateFailure() {

      if (this.localStockAllocation < 0) {
        this.setAttr();
        return "Stock allocation cannot be negative.";
      }

      if (this.localStockAllocation > 1) {
        this.setAttr();
        return "Stock allocation cannot exceed 1.";
      }

      if (this.localRetirementAge <= 0) {
        this.setAttr();
        return "Retirement age must be greater than 0.";
      }

      if (this.localCurrentAge <= 0) {
        this.setAttr();
        return "Current age must be greater than 0.";
      }

      if (this.localPrinciple < 0) {
        this.setAttr();
        return "Investment principle cannot be negative.";
      }

      if (this.localRetirementAge < this.localCurrentAge) {
        this.setAttr();
        return "Retirement age must be greater than current age";
      }
    },

    updateSaveHovered() {
      this.saveHovered = !this.saveHovered;
    },

    submitForm() {
      const msg = this.validateFailure();
      if (msg) {
        alert(msg);
        return;
      }
      // build JSON of only the changed fields
      const patchValues = {};
      for (const field of this.changedFields) {
        if (this.$data[field] === null || this.$data[field] === '') {
          this.$data[field] = 0;
        } 
        const globalName = this.nameMap[field]
        patchValues[globalName] = this.$data[field];
      }

      this.$emit("user-form-submitted", patchValues);

      this.changedFields = [];
    },
  },
};
</script>

<style scoped>
label {
  width: 10rem;
  text-align: left;
}

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
  display: flex;
  flex-shrink: 0;
  align-items: center;
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