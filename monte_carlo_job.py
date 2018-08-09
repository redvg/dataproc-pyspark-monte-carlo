import random
import time
from operator import add
from pyspark import SparkContext

INITAL_INVESTMENT = 100000
ANNUAL_INVESTMENT_BUMP = 10000
T = 30
RETURN = 0.11
STD_DEV = 0.18

NUMBER_OF_PATHS = 10000

sc = SparkContext('local')

def create_path(seed):

    random.seed(seed)

    portfolio_value = INITAL_INVESTMENT

    for _ in range(T):

        growth = random.normalvariate(RETURN, STD_DEV)

        portfolio_value += portfolio_value * growth + ANNUAL_INVESTMENT

    return portfolio_value


print '1st simulation'

'''
The result of the parallelize operation is a resilient distributed dataset (RDD),
which is a collection of elements that are optimized for parallel processing.
In this case, the RDD contains seeds that are based on the current system time.

When creating the RDD, Spark slices the data based on the number of workers
and cores available. In this case, Spark chooses to use eight slices,
 one slice for each core. That's fine for this simulation,
 which has 10,000 items of data. For larger simulations,
 each slice might be larger than the default limit.
 In that case, specifying a second parameter to parallelize can increase
  the number slices, which can help to keep the size of each slice manageable,
  while Spark still takes advantage of all eight cores.
'''

seeds = sc.parallelize([time.time() + i for i in xrange(NUMBER_OF_PATHS)])

'''
The map method passes each seed in the RDD to the grow function and appends
each result to a new RDD, which is stored in results.
Note that this operation, which performs a transformation,
doesn't produce its results right away.
 Spark won't do this work until the results are needed.
 This lazy evaluation is why you can enter code without the constants
 being defined.
'''

path = seeds.map(create_path)

path_result = path.reduce(add)

average = path_result / float(NUMBER_OF_PATHS)

print average
