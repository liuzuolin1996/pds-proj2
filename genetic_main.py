import os
os.system("clear")

import pandas as pd
import numpy as np
import pickle

from parser import Parser
from genetic_helper.classes.genetic import Genetic
from genetic_helper.classes.Monkey import Monkey

parser = Parser()
gen = Genetic(num_monkeys=100, monkey_window_size=10, num_keep=2, num_iter=200)

pool = parser.get_pool(n=10)

out = gen.run_pool(pool)

exit()

apple = parser.get("AAPL")
stats = gen.run(apple)
# pickle.dump(stats, open("saved/AAPL.sav", "wb"))

