<template>
  <div>
    <header><h1>About RetireRight</h1></header>
    <p align="left">
      RetireRight is a personal finance application designed to help people
      develop a financial plan, and more critically to think about the role
      money has in their lives. The inspiration for the project came from the
      fact that most free investment planning tools simply accept a rate and a
      timeline to graph investment growth projections without accounting for the
      context of a person's lifestyle.
    </p>
    <p align="left">
      RetireRight accepts base user information and invesment allocation
      decisions, which can be reconfigured on the main page. It then accepts a
      set of lifestyle choice variables in the form of a "scenario". A user can
      add up to 15 scenarios. <br />
      <br />

      When updating a scenario, a Monte Carlo simulation will be run for the
      user and scenario information, and a percent chance of success will be
      shown on the top of the scenario. The chance of success is defined as the
      probability the user will have enough money to spend at their estimated
      retirement expenditures through retirement.
    </p>
    <p align="left">
      On the main page, the user can select a scenario to see a graph of the
      worst, average, and best possible outcomes for their invesment based on
      the simualation. This view also shows a line representing the estimated
      total retirement expenditures. <br />
      <br />

      More information can be found at the project's
      <a href="https://github.com/Matthew-Curry/RetireRight">Github repo.</a>
    </p>
  </div>
</template>

<style scoped>
p {
  font-size: 20px;
}
</style>