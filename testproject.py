import datetime as dt
import os

import numpy as np
import pandas as pd
from util import get_data, plot_data
import marketsimcode as mkt
import ManualStrategy as ms
import StrategyLearner as sl
import matplotlib.pyplot as plt
import experiment1 as exp1
import experiment2 as exp2
import random

def seed():
    return 903450072

if __name__ == "__main__":
    print("---Test Project---")

    np.random.seed(903450072)
    random.seed(903450072)
    ms.get_graphs()
    exp1.exp1()
    exp2.exp2()