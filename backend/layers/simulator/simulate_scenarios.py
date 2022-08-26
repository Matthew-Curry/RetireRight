"""Core service to run simulation of a given scenario"""

import random
from decimal import Decimal
from math import sqrt
from statistics import NormalDist

N = 1000
RETIREMENT_LENGTH = 30

STOCK_RETURN = 0.998
STOCK_SD = 0.195
BOND_RETURN = 0.693
BOND_SD = 0.075
COV = 0.006

CHILD_COST = 12980

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
    sum_ending_balance = 0
    closest_av = 0

    max_result = []
    min_result = []
    av_result = []

    num_success = 0

    for n in range(0, N):
        total_assets = principle
        income = scenario.income_inc[current_age]
        returns = dist.samples(years, random.random())
        result = []
        yearly_downpayment_saving = (0.2*scenario.home_cost - scenario.downpayment_savings)/(scenario.age_home - current_age)
        mortgage_payment = (scenario.home_cost *0.8)/scenario.mortgage_length
        kids = 0
        kids_to_adults = set()
        for year in range(0, years):
            age = year + current_age
            # check if income changed this year
            if year in scenario.income_inc:
                income = scenario.income_inc[year]
            
            # if haven't bought a home yet, less the amount of savings for the downpayment, and the yearly rent payment
            if age < scenario.age_home:
                income = income - yearly_downpayment_saving - (scenario.rent *12)
            # if still paying off mortgage, less the yearly paymnent
            elif age > scenario.age_home and age < scenario.age_home + scenario.mortgage_length:
                income = income - scenario.mortgage_rate * mortgage_payment
            
            # check if user had a kid this year
            if age in scenario.age_kids:
                kids += 1
                kids_to_adults.add(age + 18)

            # less all expenses for the year from the income
            income = income - (scenario.food *12) - (scenario.entertainment *12) - (scenario.yearly_travel * 12) - (CHILD_COST * kids)

            # check if kid became adult
            if age in kids_to_adults:
                kids -= 1
            
            # apply income to total assets, then apply investment rate
            total_assets = total_assets + income
            total_assets = total_assets * (1 + returns[year])

            result.append(total_assets)
        
        # apply this result to the global simulation result
        if result[-1] > max_result[-1]:
            max_result = result
        
        if result[-1] > min_result[-1]:
            min_result = result

        sum_ending_balance = sum_ending_balance + result[-1]
        av = sum_ending_balance/n 

        if abs(av - result[-1]) < abs(av - closest_av):
            closest_av = av
            av_result = result 
        
        retirement_yearly_cost = (scenario.food *12) + (scenario.entertainment *12) + (scenario.yearly_travel * 12)
        if not scenario.age_home:
            retirement_yearly_cost += (scenario.rent *12)

        retirement_total_cost = retirement_yearly_cost * RETIREMENT_LENGTH

        if result[-1] > retirement_total_cost:
            num_success += 1
    
    return Decimal(num_success/N), max_result, min_result, av_result
