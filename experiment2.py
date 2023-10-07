import datetime as dt
import random

import numpy as np
import pandas as pd
from util import get_data, plot_data
import marketsimcode as mkt
import ManualStrategy as ms
import StrategyLearner as sl
import matplotlib.pyplot as plt

def author():
    return "jfeng89"

def get_result(symbol, sd, ed, sv,commission, impact):
    mkt_sim = mkt.marketsimcode(symbol=symbol, sd=sd, ed=ed, sv=sv,
                                commission=commission, impact=impact)

    # Initiating Strategy Learner
    exp2learner = sl.StrategyLearner(verbose=False, impact=impact, commission=commission)

    # Training Strategy Learner
    exp2learner.add_evidence(symbol=symbol, sd=sd, ed=ed,
                         sv=sv)

    # Strategy Learner In Sample
    order = exp2learner.testPolicy(symbol=symbol,
                                      sd=sd,
                                      ed=ed,
                                      sv=sv
                                      )
    number_of_trades = np.count_nonzero(order)
    port_val = mkt_sim.compute_portvals(order)
    port_val = port_val[:] / port_val.iloc[0].values
    port_stat = mkt_sim.get_stats(port_val)

    return order,port_val,port_stat,number_of_trades


def exp2():
    in_sample_start_date = dt.datetime(2008, 1, 1)
    in_sample_end_date = dt.datetime(2009, 12, 31)
    starting_val = 100000
    commission = 0.0
    measurements = [0.0025,0.005,0.0075,0.01,0.05]
    portstats = []
    trade_num=[]

    plt.figure(figsize=(16, 8))
    plt.grid()
    plt.title("In Sample Strategies Learner Return with Different Impact")

    plt.xlabel("Date")
    plt.ylabel("Return")
    for i in measurements:
        order, portval, portstat,number_of_trades = get_result(symbol="JPM", sd=in_sample_start_date, ed=in_sample_end_date,
                                              sv=starting_val, impact=i, commission=commission)
        plt.plot(portval, label=f"Strategy with impact = {i}")
        portstats.append(portstat)
        trade_num.append(number_of_trades)
        #portstats.append(portstat)
    plt.xlim(in_sample_start_date, in_sample_end_date)
    plt.legend()
    # plt.show()
    fig = plt.gcf()
    fig.savefig("Experiment2 Fig1 Strategy Return")

    trade_num=pd.DataFrame(trade_num, columns=['Number of Trades'], index=np.array(measurements).T)
    plt.figure(figsize=(16, 8))
    plt.grid()
    plt.title("Number of Trades with Different Impact Measurements")
    plt.xlabel("Market Impact")
    plt.ylabel("Number of Trades")
    plt.plot(trade_num, label=f"Number of Trades")
    plt.legend()
    # plt.show()
    fig = plt.gcf()
    fig.savefig("Experiment2 Fig2 Number of Trades")


    # Get performance data
    # trade_num = pd.DataFrame(trade_num,)
    line = pd.DataFrame(portstats,columns=['CR', 'ADR', 'STD', 'SR'],index = np.array(measurements).T)

    fn = 'Impact Analaysis.txt'
    with open(fn, 'a') as f:
        line = line.to_string(header=True, index=True)
        f.write(line)

if __name__ == "__main__":
    print("---Experiment 2---")
    np.random.seed(903450072)
    random.seed(903450072)
    exp2()








