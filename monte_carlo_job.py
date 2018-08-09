import random
import time
from operator import add

INITAL_INVESTMENT = 100000
ANNUAL_INVESTMENT_BUMP = 10000
T = 30
RETURN = 0.11
STD_DEV = 0.18


def create_path(seed):

    random.seed(seed)

    portfolio_value = INITAL_INVESTMENT

    for _ in range(T):

        growth = random.normalvariate(RETURN, STD_DEV)

        portfolio_value += portfolio_value * growth + ANNUAL_INVESTMENT

    return portfolio_value
