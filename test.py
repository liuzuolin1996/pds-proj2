import pandas as pd
import numpy as np
import pickle

from parser import Parser
from genetic_helper.classes.Monkey import Monkey

parser = Parser()
apple = parser.get("AAPL")
test = pd.read_csv("genetic_helper/dummy.csv")

monkey = Monkey()
monkey.init_random_weights()

x = monkey.trade(apple)

print(x)
