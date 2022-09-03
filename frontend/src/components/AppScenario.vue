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
    <form v-if="isSelected" @submit.prevent>
      <div class="form-control">
        <label for="rent">Rent</label>
        <input
          id="rent"
          name="rent"
          type="text"
          v-model="rent"
          @input="updateChangedFields('rent')"
        />
      </div>
      <div class="form-control">
        <label for="food">Food</label>
        <input
          id="food"
          name="food"
          type="text"
          v-model="food"
          @input="updateChangedFields('food')"
        />
      </div>
      <div class="form-control">
        <label for="entertainment">Entertainment</label>
        <input
          id="entertainment"
          name="entertainment"
          type="text"
          v-model="entertainment"
          @input="updateChangedFields('entertainment')"
        />
      </div>
      <div class="form-control">
        <label for="yearlyTravel">Yearly Travel</label>
        <input
          id="yearlyTravel"
          name="yearlyTravel"
          type="text"
          v-model="yearlyTravel"
          @input="updateChangedFields('yearlyTravel')"
        />
      </div>
      <div class="form-control">
        <label for="ageHome">Age Home</label>
        <input
          id="ageHome"
          name="ageHome"
          type="text"
          v-model="ageHome"
          @input="updateChangedFields('ageHome')"
        />
      </div>
      <div class="form-control">
        <label for="downpaymentSavings">Downpayment Savings</label>
        <input
          id="downpaymentSavings"
          name="downpaymentSavings"
          type="text"
          v-model="downpaymentSavings"
          @input="updateChangedFields('downpaymentSavings')"
        />
      </div>
      <div class="form-control">
        <label for="mortgageRate">Mortgage Rate</label>
        <input
          id="mortgageRate"
          name="mortgageRate"
          type="text"
          v-model="mortgageRate"
          @input="updateChangedFields('mortgageRate')"
        />
      </div>
      <div class="form-control">
        <label for="mortgageLength">Mortgage Length</label>
        <input
          id="mortgageLength"
          name="mortgageLength"
          type="text"
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
            type="text"
            v-model="ageKids[index]"
            @input="updateChangedFields('ageKids')"
          />
          <button class="deleteButton deleteAgeButton" @click="removeAge(index)">
            Remove Age
          </button>
        </div>
        <button class="saveButton saveAgeButton" v-if="addingKid === false" @click="addingKid = true">
          Add age
        </button>
        <input
          v-if="addingKid"
          v-model="additionalKid"
          id="ageOfKids"
          name="ageOfKids"
        />
        <button class="saveButton saveAgeButton" v-if="addingKid" @click="submitAge">Submit age</button>
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
    </form>
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
  },

  emits: ["selected", "form-submitted", "deleted"],

  data() {
    return {
      hovered: false,
      formVisible: false,
      saveHovered: false,
      deleteHovered: false,
      addingKid: false,
      additionalKid: null,
      changedFields: [],

      // attributes from the data prop
      rent: 0,
      food: 0,
      entertainment: 0,
      yearlyTravel: 0,
      ageHome: 0,
      downpaymentSavings: 0,
      mortgageRate: 0,
      mortgageLength: 0,
    };
  },

  beforeMount() {
    this.rent = this.sourceData.rent;
    this.food = this.sourceData.food;
    this.entertainment = this.sourceData.entertainment;
    this.yearlyTravel = this.sourceData.yearlyTravel;
    this.ageHome = this.sourceData.ageHome;
    this.downpaymentSavings = this.sourceData.downpaymentSavings;
    this.mortgageRate = this.sourceData.mortgageRate;
    this.mortgageLength = this.sourceData.mortgageLength;
    this.ageKids = this.sourceData.ageKids;
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
      this.changedFields.push(field);
    },

    submitAge() {
      this.ageKids.push(this.additionalKid);
      this.additionalKid = null;
      this.addingKid = false;
    },

    removeAge(index) {
        this.ageKids.splice(index,1);
    },

    deleteScenario() {
      this.$emit("deleted", this.scenarioIndex);
    },

    submitForm() {
      // build JSON of only the changed fields
      const patchValues = {};
      for (let field in this.changedFields) {
        patchValues[field] = this.$data[field];
      }
      this.$emit("form-submitted", this.scenarioIndex, patchValues);
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

.form-control {
  margin: 0.5rem 0;
}

label {
  font-weight: bold;
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
    padding: 0.25rem .7rem
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
    padding: 0.25rem .7rem
}

.darkDeleteButton {
  border: 1px solid #68020a;
  background-color: #68020a;
}
</style>