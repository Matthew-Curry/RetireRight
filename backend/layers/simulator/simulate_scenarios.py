"""Core service to run simulation of a given scenario"""
import logging
import random
from decimal import Decimal
from math import sqrt
from statistics import NormalDist

N = 1000
RETIREMENT_LENGTH = 30

STOCK_RETURN = Decimal(0.0998)
STOCK_SD = Decimal(0.195)
BOND_RETURN = Decimal(0.0693)
BOND_SD = Decimal(0.075)
COV = Decimal(0.006)

INFLATION_RATE = Decimal(0.03)

CHILD_COST = 12980

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def simulate_scenario(current_age:int, retirement_age:int, per_stock:Decimal, principle:int, scenario) -> tuple:
    """Runs asset growth simulation subject to a set of user parameters and a scenario
    args:
        current_age (int): the current age of the user
        retirement_age (int): the targeted retirement age of the user
        per_stock (Decimal): the percentage of the user's investment portfolio invested in stocks
        principle (int): initial amount in investment account
        scenario (Scenario): the given scenario holding lifestyle choice variables
    returns:
        tuple in form (percent chance of success, best result, worst result, average result)"""

    years = retirement_age - current_age
    
    r = per_stock * STOCK_RETURN + (1 - per_stock) * BOND_RETURN
    s = sqrt(per_stock**2*STOCK_SD**2 + (1 - per_stock)**2*BOND_SD**2 + 2*per_stock*(1-per_stock)*COV)

    dist = NormalDist(r, s)
    random.seed(45)

    # variables to store results
    max_result = []
    min_result = []
    av_result = []

    sum_ending_balance = 0
    closest_av = 0

    num_success = 0
    
    logger.info("Starting simulation")
    for n in range(0, N):
        # initialize total assests and income
        total_assets = principle
        income = scenario.income_inc[str(current_age)]
        # initialize all vars from the scenario
        rent = scenario.rent
        food = scenario.food
        entertainment = scenario.entertainment
        yearly_travel = scenario.yearly_travel
        age_kids = set(scenario.age_kids)
        age_home = scenario.age_home
        home_cost = scenario.home_cost
        downpayment_savings = scenario.downpayment_savings
        mortgage_rate = scenario.mortgage_rate
        mortgage_length = scenario.mortgage_length
        income_inc = scenario.income_inc
        # pull sample of returns for the number of years of the simulation
        logger.info("Generating simulated returns")
        returns = dist.samples(years, seed = random.random())
        # set variables from home decision attributes
        if age_home:
            yearly_downpayment_saving = (0.2*home_cost - downpayment_savings)/(age_home - current_age)
            mortgage_payment = (home_cost *0.8)/mortgage_length
        # initialize kids to 0, a set to keep track of when kids become adults
        kids = 0
        kids_to_adults = set()
        # inflation factor is one plus the global rate
        inflation_factor = 1 + INFLATION_RATE
        # kid cost initialized to global var before adjusting during simulation run
        yearly_kid_cost = CHILD_COST
        # the result to populate, list holding net assets for each year
        result = []
        logger.info("All variables initialized for simulation run. Starting run..")
        for year in range(1, years + 1):
            # apply inflation adjustment to all cost of living estimates
            rent = inflation_factor * rent
            food = inflation_factor * food
            entertainment = inflation_factor * entertainment
            yearly_travel = inflation_factor * yearly_travel
            yearly_kid_cost = inflation_factor * yearly_kid_cost

            age = year + current_age
            # check if income changed this year
            if age in income_inc:
                income = income_inc[age]
            
            if age_home:
                # if haven't bought a home yet, less the amount of savings for the downpayment, and the yearly rent payment
                if age < age_home:
                    income = income - yearly_downpayment_saving - (rent *12)
                # if still paying off mortgage, less the yearly paymnent
                elif age > age_home and age < age_home + mortgage_length:
                    income = income - mortgage_rate * mortgage_payment
            else:
                income = income - (rent *12)
            
            # check if user had a kid this year
            if age in age_kids:
                kids += 1
                kids_to_adults.add(age + 18)

            # less all expenses for the year from the income
            income = income - (food *12) - (entertainment *12) - (yearly_travel * 12) - (CHILD_COST * kids)

            # check if kid became adult
            if age in kids_to_adults:
                kids -= 1
            
            # apply income to total assets, then apply investment rate
            total_assets = total_assets + income
            total_assets = total_assets * (1 + Decimal(returns[year - 1]))

            result.append(total_assets)
        
        # apply this result to the global simulation result
        logger.info(f"Completed run {n}. Recording results..")
        if n == 0:
            max_result = min_result = av_result = result
        else:
            if result[-1] > max_result[-1]:
                max_result = result
        
            if result[-1] < min_result[-1]:
                min_result = result

            sum_ending_balance = sum_ending_balance + result[-1]
            av = sum_ending_balance/n 

            if abs(av - result[-1]) < abs(av - closest_av):
                closest_av = av
                av_result = result 
        
        retirement_yearly_cost = (food *12) + (entertainment *12) + (yearly_travel * 12)
        if not age_home:
            retirement_yearly_cost += (rent *12)

        retirement_total_cost = retirement_yearly_cost * RETIREMENT_LENGTH

        if result[-1] > retirement_total_cost:
            num_success += 1
    
    return Decimal(num_success/N), max_result, min_result, av_result
