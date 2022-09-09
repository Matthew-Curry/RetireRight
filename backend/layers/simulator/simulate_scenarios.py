"""Core service to run simulation of a given scenario"""
import logging
import random
from decimal import Decimal
from math import sqrt
from statistics import NormalDist

N = 1000
LIFE_EXPECTANCY = 80

STOCK_RETURN = Decimal("0.0998")
STOCK_SD = Decimal("0.195")
BOND_RETURN = Decimal("0.0693")
BOND_SD = Decimal("0.075")
COV = Decimal("0.006")

INFLATION_RATE = Decimal("0.03")

DOWNPAYMENT_PERCENT = Decimal("0.2")

CHILD_COST = 12980

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ResultList:
    """Wrapper class to hold result list in API consistent with frontend and database requirements"""

    def __init__(self, principle):
        self.next_item = 0
        self.list = []

        self.append(principle)

    def append(self, val):
        if isinstance(val, Decimal) == False:
            val = Decimal(str(val))

        self.list.append({'x': self.next_item, 'y': val.quantize(Decimal('.01'))})
        self.next_item += 1

    def get_list(self):
        return self.list

    @property
    def end_value(self):
        return self.list[-1]['y']

def get_total_retirement_cost(food, entertainment, yearly_travel, rent, age_home, current_age, retirement_age, age_home_paid, mortgage_payment):
    """helper method to estimate retirement cost """
    # inflation adjust cost vars to retirement age
    working_time = retirement_age - current_age
    for _ in range(1, working_time):
        food = food * (1 + INFLATION_RATE)
        entertainment = entertainment * (1 + INFLATION_RATE)
        yearly_travel = yearly_travel * (1 + INFLATION_RATE)
        rent = rent * (1 + INFLATION_RATE)

    retirement_yearly_cost = (food *12) + (entertainment *12) + yearly_travel
    home_payoff = 0
    if not age_home:
        retirement_yearly_cost += (rent *12)
    elif retirement_age < age_home_paid:
        home_payoff = (age_home_paid - retirement_age) * mortgage_payment

    total_cost = retirement_yearly_cost + home_payoff
    length = LIFE_EXPECTANCY - retirement_age
    for _ in range(1, length):
        total_cost = retirement_yearly_cost * (1 + INFLATION_RATE)

    return total_cost

def simulate_scenario(user, scenario) -> tuple:
    """Runs asset growth simulation for a user and a scenario
    args:
        user (User): the user object, holds age and investment choice attributes
        scenario (Scenario): the given scenario holding lifestyle choice variables
    returns:
        tuple in form (percent chance of success, best result, worst result, average result)"""
    
    # unpack vars from the user
    current_age = user.currentAge
    retirement_age = user.retirementAge
    per_stock = user.stockAllocation
    principle = user.principle

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
    closest_av = Decimal(float('inf'))

    num_success = 0

    age_kids = set(scenario.ageKids)
    age_home = scenario.ageHome
    home_cost = scenario.homeCost
    downpayment_savings = scenario.downpaymentSavings
    mortgage_factor = 1 + scenario.mortgageRate
    mortgage_length = scenario.mortgageLength
    income_inc = scenario.incomeInc
    # set variables from home decision attributes
    if age_home:
        mortgage_payment = mortgage_factor * yearly_split
        age_home_paid = age_home + mortgage_length
        yearly_split = (home_cost *(1-DOWNPAYMENT_PERCENT))/mortgage_length
        if age_home == current_age:
            yearly_downpayment_saving = 0
        else:
            yearly_downpayment_saving = (DOWNPAYMENT_PERCENT*home_cost - downpayment_savings)/(age_home - current_age)
    else:
        age_home_paid = None
        mortgage_payment = None

    retirement_cost = get_total_retirement_cost(scenario.food, scenario.entertainment, scenario.yearlyTravel, scenario.rent, age_home, 
                                    current_age, retirement_age, age_home_paid, mortgage_payment)

    # inflation factor is one plus the global var holding inflation rate
    inflation_factor = 1 + INFLATION_RATE

    logger.info("Starting simulation")
    for n in range(0, N):
        # initialize total assests and income
        total_assets = principle
        income = scenario.incomeInc[str(current_age)]
        # initialize all vars from the scenario
        rent = scenario.rent
        food = scenario.food
        entertainment = scenario.entertainment
        yearly_travel = scenario.yearlyTravel
        # pull sample of returns for the number of years of the simulation
        logger.info("Generating simulated returns")
        returns = dist.samples(years, seed = random.random())
        # initialize kids to 0, and a set to keep track of when kids become adults
        kids = 0
        kids_to_adults = set()
        # kid cost initialized to global var before adjusting during simulation run
        yearly_kid_cost = CHILD_COST
        # the result to populate, list holding net assets for each year
        result = ResultList(total_assets)
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
            if str(age) in income_inc:
                income = income_inc[str(age)]

            # update the net income to the income
            net_income = income
            
            if age_home:
                # if haven't bought a home yet, less the amount of savings for the downpayment, and the yearly rent payment
                if age < age_home:
                    net_income = net_income - yearly_downpayment_saving - (rent *12)
                # if still paying off mortgage, less the yearly paymnent
                elif age > age_home and age < age_home_paid:
                    net_income = net_income - mortgage_payment
            else:
                net_income = net_income - (rent *12)
            
            # check if user had a kid this year
            if age in age_kids:
                kids += 1
                kids_to_adults.add(age + 18)

            # less all expenses for the year from the income
            net_income = net_income - (food *12) - (entertainment *12) - yearly_travel - (CHILD_COST * kids)

            # check if kid became adult
            if age in kids_to_adults:
                kids -= 1
            
            # apply income to total assets, then apply investment rate
            total_assets = total_assets + net_income
            total_assets = total_assets * (1 + Decimal(returns[year - 1]))

            result.append(total_assets)
        
        # apply this result to the global simulation result
        logger.info(f"Completed run {n}. Recording results..")
        if n == 0:
            max_result = min_result = av_result = result
        else:
            if result.end_value > max_result.end_value:
                max_result = result
        
            if result.end_value < min_result.end_value:
                min_result = result

            sum_ending_balance = sum_ending_balance + result.end_value
            av = sum_ending_balance/n 

            if abs(av - result.end_value) < abs(av - closest_av):
                closest_av = av
                av_result = result 
    
        if result.end_value > retirement_cost:
            num_success += 1
    
    return Decimal(str(num_success/N)), retirement_cost, max_result.get_list(), min_result.get_list(), av_result.get_list()
