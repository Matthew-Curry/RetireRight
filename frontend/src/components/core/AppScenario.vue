<template>
  <section
    class="base"
    :class="isExtraClass && extraClass"
    @click="select"
    @mouseenter="updateHovered"
    @mouseleave="updateHovered"
  >
    <h2>Scenario {{ scenarioNumber }}</h2>
    <h3 id="percentage" :class="percentCSSClass">{{ percentSuccess }}</h3>
    <h3 v-if="savingScenario.value === true && selectedScenarioIndex.value === scenarioIndex">Saving Scenario and Running Simmulation...</h3>
    <section v-if="isSelected">
      <div class="form-control flex-box">
        <label class="single-input-label" for="rent">Rent</label>
        <input
          id="rent"
          name="rent"
          type="number"
          min="0"
          v-model="rent"
          @input="updateChangedFields('rent')"
        />
      </div>

      <div class="form-control flex-box">
        <label class="single-input-label" for="food">Food</label>
        <input
          id="food"
          name="food"
          type="number"
          min="0"
          v-model="food"
          @input="updateChangedFields('food')"
        />
      </div>

      <div class="form-control flex-box">
        <label class="single-input-label" for="entertainment"
          >Entertainment</label
        >
        <input
          id="entertainment"
          name="entertainment"
          type="number"
          min="0"
          v-model="entertainment"
          @input="updateChangedFields('entertainment')"
        />
      </div>

      <div class="form-control flex-box">
        <label class="single-input-label" for="yearlyTravel"
          >Yearly Travel</label
        >
        <input
          id="yearlyTravel"
          name="yearlyTravel"
          type="number"
          min="0"
          v-model="yearlyTravel"
          @input="updateChangedFields('yearlyTravel')"
        />
      </div>

      <div class="form-control flex-box">
        <label class="single-input-label" for="ageHome">Age Home</label>
        <input
          id="ageHome"
          name="ageHome"
          type="number"
          min="0"
          step="1"
          v-model="ageHome"
          @input="updateChangedFields('ageHome')"
        />
      </div>

      <div class="form-control flex-box">
        <label class="single-input-label" for="ageHome">Home Cost</label>
        <input
          id="homeCost"
          name="homeCost"
          type="number"
          min="0"
          v-model="homeCost"
          @input="updateChangedFields('homeCost')"
        />
      </div>

      <div class="form-control flex-box">
        <label class="single-input-label" for="downpaymentSavings"
          >Downpayment Savings</label
        >
        <input
          id="downpaymentSavings"
          name="downpaymentSavings"
          type="number"
          min="0"
          v-model="downpaymentSavings"
          @input="updateChangedFields('downpaymentSavings')"
        />
      </div>

      <div class="form-control flex-box">
        <label class="single-input-label" for="mortgageRate"
          >Mortgage Rate</label
        >
        <input
          id="mortgageRate"
          name="mortgageRate"
          type="number"
          step="0.01"
          v-model="mortgageRate"
          @input="updateChangedFields('mortgageRate')"
        />
      </div>

      <div class="form-control flex-box">
        <label class="single-input-label" for="mortgageLength"
          >Mortgage Length</label
        >
        <input
          id="mortgageLength"
          name="mortgageLength"
          type="number"
          min="0"
          v-model="mortgageLength"
          @input="updateChangedFields('mortgageLength')"
        />
      </div>

      <div class="form-control">
        <label for="ageOfKids">Age of Having Child</label>
        <div v-for="(age, index) in ageKids" :key="index">
          <input
            id="ageOfKids"
            name="ageOfKids"
            type="number"
            min="0"
            step="1"
            v-model="ageKids[index]"
            @input="updateChangedFields('ageKids')"
          />
          <button
            class="deleteButton deleteAgeButton"
            @click="removeAge(index)"
          >
            Remove age
          </button>
        </div>
        <button
          class="saveButton saveAgeButton"
          v-if="addingKid === false"
          @click="addingKid = true"
        >
          Add age
        </button>
        <input
          v-if="addingKid"
          v-model="additionalKid"
          id="ageOfKids"
          name="ageOfKids"
          type="number"
          min="0"
          step="1"
          @input="updateChangedFields('ageKids')"
        />
        <button
          class="saveButton saveAgeButton"
          v-if="addingKid"
          @click="submitAge"
        >
          Submit age
        </button>
      </div>

      <div class="form-control">
        <label for="ageIncome"
          >Age of Income Increases. Please include current age.</label
        >
        <div v-for="(imcome, age) in incomeInc" :key="age" class="flex-box">
          <label class="ageIncomeLabel">Age</label>
          <p>{{ age }}</p>
          <label class="valueIncomeLabel">Income</label>
          <input
            class="incomeValue"
            id="ageIncome"
            name="ageIncome"
            type="number"
            min="0"
            v-model="incomeInc[age]"
            @input="
              updateChangedFields('incomeInc');
              incomeValue = income;
            "
          />
          <button
            class="deleteButton deleteAgeButton"
            @click="removeIncomeAge(age)"
          >
            Remove age
          </button>
        </div>
        <button
          class="saveButton saveAgeButton"
          v-if="addingIncome === false"
          @click="addingIncome = true"
        >
          Add age
        </button>
        <div v-if="addingIncome" class="flex-box">
          <label class="ageIncomeLabel">Age</label>
          <input
            id="ageIncome"
            class="ageIncomeValue"
            name="ageIncome"
            type="number"
            v-model="incomeAge"
            @input="updateChangedFields('incomeInc')"
          />
          <label class="valueIncomeLabel">Income</label>
          <input
            class="incomeValue"
            id="ageIncome"
            name="ageIncome"
            type="number"
            v-model="incomeValue"
            @input="updateChangedFields('incomeInc')"
          />
        </div>
        <button
          class="saveButton saveAgeButton"
          v-if="addingIncome"
          @click="submitIncome(age)"
        >
          Submit age
        </button>
      </div>
      <div class="form-control">
        <button
          class="saveButton"
          @mouseenter="updateSaveHovered"
          @mouseleave="updateSaveHovered"
          @click="submitForm"
          :class="{ darkSaveButton: saveHovered }"
        >
          Save Scenario
        </button>
        <button
          class="deleteButton"
          @mouseenter="updateDeleteHovered"
          @mouseleave="updateDeleteHovered"
          @click="deleteScenario"
          :class="{ darkDeleteButton: deleteHovered }"
        >
          Delete Scenario
        </button>
      </div>
    </section>
  </section>
</template>

<script>
export default {
  props: {
    isSelected: {
      type: Boolean,
      required: true,
    },

    scenarioIndex: {
      type: Number,
      required: true,
    },

    sourceData: {
      type: Object,
      required: true,
    },

    currentAge: {
      type: Number,
      required: true,
    },

  },

  emits: ["selected", "scenario-form-submitted", "deleted"],

  inject: ["savingScenario", "selectedScenarioIndex"],

  data() {
    return {
      hovered: false,
      formVisible: false,
      saveHovered: false,
      deleteHovered: false,
      addingKid: false,
      addingIncome: false,
      additionalKid: null,
      incomeAge: null,
      incomeValue: null,
      changedFields: [],

      // attributes from the data prop
      rent: null,
      food: null,
      entertainment: null,
      yearlyTravel: null,
      ageHome: null,
      homeCost: null,
      downpaymentSavings: null,
      mortgageRate: null,
      mortgageLength: null,
      ageKids: null,
      incomeInc: null,
    };
  },

  beforeMount() {
    this.setAttr();
  },

  watch: {
    sourceData() {
      this.setSimChangeAttr();
    },
  },

  computed: {
    percentSuccess() {
      return (this.sourceData.percentSuccess * 100).toString() + "%";
    },

    isExtraClass() {
      return this.isSelected || this.hovered;
    },

    extraClass() {
      if (this.isSelected) {
        return "selected";
      } else if (this.hovered) {
        return "highlighted";
      }

      return "";
    },

    scenarioNumber() {
      return this.scenarioIndex + 1;
    },

    percentCSSClass() {
      if (this.sourceData.percentSuccess < 0.6) {
        return "Red";
      } else if (this.sourceData.percentSuccess < 0.9) {
        return "Yellow";
      }

      return "Green";
    },
  },

  methods: {
    select() {
      if (!this.isSelected) {
        this.$emit("selected", this.scenarioIndex);
      }
    },

    setAttr() {
      this.rent = this.sourceData.rent;
      this.food = this.sourceData.food;
      this.entertainment = this.sourceData.entertainment;
      this.yearlyTravel = this.sourceData.yearlyTravel;
      this.setSimChangeAttr()
    },

    setSimChangeAttr() {
      this.ageKids = [...this.sourceData.ageKids];
      this.incomeInc = JSON.parse(JSON.stringify(this.sourceData.incomeInc));
      this.ageHome = this.sourceData.ageHome;
      this.homeCost = this.sourceData.homeCost;
      this.downpaymentSavings = this.sourceData.downpaymentSavings;
      this.mortgageRate = this.sourceData.mortgageRate;
      this.mortgageLength = this.sourceData.mortgageLength;
    },

    showForm() {
      this.formVisible = true;
    },

    updateHovered() {
      this.hovered = !this.hovered;
    },

    updateSaveHovered() {
      this.saveHovered = !this.saveHovered;
    },

    updateDeleteHovered() {
      this.deleteHovered = !this.deleteHovered;
    },

    updateChangedFields(field) {
      if (!this.changedFields.includes(field)) {
        this.changedFields.push(field);
      }
    },

    submitAge() {
      this.ageKids.push(this.additionalKid);
      this.additionalKid = null;
      this.addingKid = false;
    },

    removeAge(index) {
      this.ageKids.splice(index, 1);
      this.updateChangedFields('ageKids');
    },

    removeIncomeAge(age) {
      delete this.incomeInc[age];
      this.updateChangedFields('incomeInc');
    },

    submitIncome(age) {
      if (this.incomeAge) {
        delete this.incomeInc[age];
        this.incomeInc[this.incomeAge] = this.incomeValue;
      } else {
        this.incomeInc[age] = this.incomeValue;
      }

      this.incomeAge = null;
      this.incomeValue = null;
      this.addingIncome = false;
    },

    deleteScenario() {
      this.$emit("deleted", this.scenarioIndex);
    },

    validateFailure() {
      if (this.rent < 0) {
        this.setAttr();
        return "Rent cannot be negative.";
      }

      if (this.entertainment < 0) {
        this.setAttr();
        return "Entertainment spending cannot be negative.";
      }

      if (this.food < 0) {
        this.setAttr();
        return "Food spending cannot be negative.";
      }

      if (this.yearlyTravel < 0) {
        this.setAttr();
        return "Yearly travel spending cannot be negative.";
      }

      if (this.downpaymentSavings < 0) {
        this.setAttr();
        return "Downpayment savings cannot be negative.";
      }

      if (this.mortgageRate < 0) {
        this.setAttr();
        return "Mortgage rate cannot be negative.";
      }

      if (this.mortgageRate > 1) {
        this.setAttr();
        return "Mortgage rate cannot be greater than 1.";
      }

      if (this.mortgageLength < 0) {
        this.setAttr();
        return "Mortgage length cannot be negative.";
      }

      if (this.ageHome < 0) {
        this.setAttr();
        return "Age of home purchase cannot be negative.";
      }

      if (this.homeCost < 0) {
        this.setAttr();
        return "Home cost cannot be negative.";
      }

      if (this.ageHome && this.ageHome < this.currentAge) {
        this.setAttr();
        return "Age of home purchase cannot be smaller than the current age.";
      }
      
      if (this.ageHome && !this.homeCost) {
        this.setAttr();
        return "A home cost must be given if an age of home purchase is provided."
      }

      if (this.ageHome && !this.mortgageRate) {
        this.setAttr();
        return "A mortgage rate must be given if an age of home purchase is provided."
      }

      if (this.ageHome && !this.mortgageLength) {
        this.setAttr();
        return "A mortgage length must be given if an age of home purchase is provided."
      }

      if(!this.ageHome && (this.homeCost || this.mortgageRate || this.mortgageLength || this.downpaymentSavings)) {
        this.setAttr();
        return "Cannot provide home related variables without giving a home purchase age and cost."
      }

      for (let age of this.ageKids) {
        if (age == null || age === 'undefined' || age === '') {
          age = 0;
        }

        if (age < this.currentAge) {
          this.setAttr();
          return "No age of having a child can preceed the user's current age.";
        }
      }

      if( Object.keys(this.incomeInc).length === 0){
        this.setAttr();
        return "Income information must be provided."
      }

      let foundMatch = false;
      for (let [age, income] of Object.entries(this.incomeInc)) {

        if (income == null || income === 'undefined' || income === '') {
          income = 0;
          this.incomeInc[age] = income;
        }

        if (age === undefined || age === 'undefined' || age === '') {
          delete this.incomeInc[age];
          age = '0';
          this.incomeInc[age] = income;
        }

        if (age < this.currentAge) {
          this.setAttr();
          return "No age of an income increase can preceed the user's current age.";
        } else if (age == this.currentAge) {
          foundMatch = true;
        }

        if (income < 0) {
          this.setAttr();
          return "Income cannot be negative"
        }
      }

      if (!foundMatch) {
        this.setAttr();
        return "Income for the user's current age must be provided"
      }
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
        if (this.$data[field] == null || this.$data[field] == 'undefined' || this.$data[field] === '') {
          this.$data[field] = 0;
        } 

        patchValues[field] = this.$data[field];
      }
      this.$emit("scenario-form-submitted", this.scenarioIndex, patchValues);

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

.highlighted {
  box-shadow: 0 12px 40px rgba(12, 131, 111, 0.829);
}

.selected {
  box-shadow: 0 12px 45px rgba(7, 73, 62, 0.829);
}

.Red {
  color: rgb(238, 75, 43);
}

.Yellow {
  color: rgb(255, 196, 0);
}

.Green {
  color: rgb(23, 212, 23);
}

form {
  margin: 2rem auto;
  max-width: 25rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  padding: 2rem;
  background-color: #0e0d0d;
}

.flex-box {
  display: flex;
  flex-shrink: 0;
  align-items: center;
}

.single-input-label {
  width: 20rem;
  text-align: left;
}

.form-control {
  margin: 0.5rem 0;
}

label {
  font-weight: bold;
}

.ageIncomeLabel {
  width: 3rem;
}

.valueIncomeLabel {
  width: 4rem;
}

.ageIncomeValue {
  width: 2rem;
}

.incomeValue {
  width: 5rem;
}

h2 {
  font-size: 1rem;
  margin: 0.5rem 0;
}

input,
select {
  display: block;
  width: 100%;
  font: inherit;
  margin-top: 0.5rem;
}

select {
  width: auto;
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

.saveAgeButton {
  font-size: 0.8rem;
  padding: 0.25rem 0.7rem;
}

.darkSaveButton {
  border: 1px solid #021c72;
  background-color: #021c72;
}

.deleteButton {
  font: inherit;
  border: 1px solid #bb0010;
  background-color: #bb0010;
  color: white;
  cursor: pointer;
  padding: 0.75rem 2rem;
  border-radius: 30px;
  margin: 5px;
}

.deleteAgeButton {
  font-size: 0.8rem;
  padding: 0.25rem 0.7rem;
}

.darkDeleteButton {
  border: 1px solid #68020a;
  background-color: #68020a;
}

div.settings {
  display: grid;
  grid-template-columns: max-content max-content;
  grid-gap: 5px;
}
div.settings label {
  text-align: right;
}
div.settings label:after {
  content: ":";
}
</style>