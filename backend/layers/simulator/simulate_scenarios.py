"""Core service to run simulation of a given scenario"""

from decimal import Decimal
from domain import Scenario

def simulate_scenario(current_age:int, retirement_age:int, per_stock:Decimal, principle, scenario: Scenario):
    """process the scenario
    
    return the chance of success, best, worst, average result."""

    r = [principle] * (retirement_age - current_age)

    return Decimal("0.8"), r, r, r
    