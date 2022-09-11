<template>
  <section class="base">
    <h2>{{ username }} {{patchValues.currentAge}}</h2>
    <div class="form-control">
      <label for="patchValues.currentAge">Current Age</label>
      <input
        id="patchValues.currentAge"
        name="patchValues.currentAge"
        type="number"
        min="0"
        step="1"
        v-model="patchValues.currentAge"
      />
    </div>

    <div class="form-control">
      <label for="patchValues.retirementAge">Retirement Age</label>
      <input
        id="patchValues.retirementAge"
        name="patchValues.retirementAge"
        type="number"
        min="0"
        step="1"
        v-model="patchValues.retirementAge"
        ref="patchValues.retirementAge"
      />
    </div>

    <div class="form-control">
      <label for="patchValues.principle">Principle</label>
      <input
        id="patchValues.principle"
        name="patchValues.principle"
        type="number"
        min="0"
        step="1"
        v-model="patchValues.principle"
        ref="patchValues.principle"
      />
    </div>

    <div class="form-control">
      <label for="patchValues.stockAllocation">Stock Allocation</label>
      <input
        id="patchValues.stockAllocation"
        name="patchValues.stockAllocation"
        type="number"
        min="0"
        step="0.01"
        max="1"
        v-model="patchValues.stockAllocation"
        ref="patchValues.stockAllocation"
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

  inject: ["castToInt"],

  data() {
    return {
      patchValues: {
        stockAllocation: null,
        retirementAge: null,
        currentAge: null,
        principle: null,
      },

      saveHovered: false,
    };
  },

  beforeMount() {
    this.setAttr();
  },

  methods: {
    setAttr() {
      this.patchValues.stockAllocation = this.stockAllocation;
      this.patchValues.retirementAge = this.retirementAge;
      this.patchValues.currentAge = this.currentAge;
      this.patchValues.principle = this.principle;
    },

    checkBaseFields() {
      if (this.patchValues.stockAllocation < 0) {
        return this.getErrorMsg("Stock allocation cannot be negative.");
      }

      if (this.patchValues.stockAllocation > 1) {
        return this.getErrorMsg("Stock allocation cannot exceed 1.");
      }

      if (this.patchValues.retirementAge <= 0) {
        return this.getErrorMsg("Retirement age must be greater than 0.");
      }

      if (this.patchValues.currentAge <= 0) {
        return this.getErrorMsg("Current age must be greater than 0.");
      }

      if (this.patchValues.principle < 0) {
        return this.getErrorMsg("Investment principle cannot be negative.");
      }

      if (this.patchValues.retirementAge <= this.patchValues.currentAge) {
        return this.getErrorMsg(
          "Retirement age must be greater than current age"
        );
      }

    },

  castBaseFields() {
    this.patchValues.currentAge = this.castToInt(this.patchValues.currentAge);
    this.patchValues.principle = this.castToInt(this.patchValues.principle);
    this.patchValues.retirementAge = this.castToInt(this.patchValues.retirementAge);
    this.patchValues.stockAllocation = this.castToInt(this.patchValues.stockAllocation);
  },

  validateFields() {
    this.castBaseFields();
    const c = this.checkBaseFields();
    if (c) {
        return c;
      }
  },

  getErrorMsg(msg) {
      this.setAttr();
      return msg;
    },

  updateSaveHovered() {
    this.saveHovered = !this.saveHovered;
  },

  submitForm() {
    const msg = this.validateFields();
    if (msg) {
      alert(msg);
      return;
    }

    this.$emit("user-form-submitted", this.patchValues);
  },
  }
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