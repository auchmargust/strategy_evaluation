import datetime as dt
import os

import numpy as np
import pandas as pd
from util import get_data, plot_data
import marketsimcode as mkt
import ManualStrategy as ms
import StrategyLearner as sl
import matplotlib.pyplot as plt

def author():
    return "jfeng89"

def exp1():
    in_sample_start_date = dt.datetime(2008, 1, 1)
    in_sample_end_date = dt.datetime(2009, 12, 31)
    out_sample_start_date = dt.datetime(2010, 1, 1)
    out_sample_end_date = dt.datetime(2011, 12, 31)
    starting_val = 100000
    # order_size = 1000
    impact = 0.0
    commission = None

    # Setting up different market simulations for in & out sample
    mkt_sim_in = mkt.marketsimcode(symbol="JPM", sd=in_sample_start_date, ed=in_sample_end_date, sv=starting_val,
                               commission=commission, impact=impact)
    mkt_sim_out = mkt.marketsimcode(symbol="JPM", sd=out_sample_start_date, ed=out_sample_end_date, sv=starting_val,
                                commission=commission, impact=impact)

    # Manual Strategy In Sample
    ms_orders_in = ms.testPolicy(symbol="JPM", sd=in_sample_start_date, ed=in_sample_end_date,
                              sv=starting_val)
    ms_in = mkt_sim_in.compute_portvals(order=ms_orders_in)
    ms_in = ms_in[:] / ms_in.iloc[0].values

    # Manual Strategy Out Sample
    ms_orders_out = ms.testPolicy(symbol="JPM", sd=out_sample_start_date, ed=out_sample_end_date,
                               sv=starting_val)
    ms_out = mkt_sim_out.compute_portvals(order=ms_orders_out )
    ms_out = ms_out[:] / ms_out.iloc[0].values

    # Initiating Strategy Learner
    learner = sl.StrategyLearner(verbose=False, impact=0.0, commission=0.0)
    # Training Strategy Learner
    learner.add_evidence(symbol="JPM", sd=in_sample_start_date, ed=in_sample_end_date,
                         sv=100000)

    # Strategy Learner In Sample
    sl_orders_in = learner.testPolicy(symbol="JPM",
                                      sd=in_sample_start_date,
                                      ed=in_sample_end_date,
                                      sv=starting_val)
    sl_in = mkt_sim_in.compute_portvals(order=sl_orders_in)
    sl_in = sl_in[:] / sl_in.iloc[0].values

    # Strategy Learner Out Sample
    sl_orders_out = learner.testPolicy(
        symbol="JPM", sd=out_sample_start_date,
        ed=out_sample_end_date,
        sv=starting_val)
    sl_out = mkt_sim_out.compute_portvals(order=sl_orders_out)
    sl_out = sl_out[:] / sl_out.iloc[0].values

    # In Sample Benchmark
    b_orders_in = pd.DataFrame(0, index=ms_orders_in.index, columns=['JPM'])
    b_orders_in.loc[ms_orders_in.index[0]] = 1000
    b_in = mkt_sim_in.compute_portvals(
        order=b_orders_in
    )
    b_in = b_in[:] / b_in.iloc[0].values
    
    # Out Sample Benchmark
    b_orders_out = pd.DataFrame(0, index=ms_orders_out.index, columns=['JPM'])
    b_orders_out.loc[ms_orders_out.index[0]] = 1000
    b_out = mkt_sim_out.compute_portvals(
        order=b_orders_out
    )
    b_out = b_out[:] / b_out.iloc[0].values

    # Plots
    plt.figure(figsize=(16, 8))
    plt.grid()
    plt.title("In Sample Strategies Comparison")
    plt.xlim(in_sample_start_date, in_sample_end_date)
    plt.xlabel("Date")
    plt.ylabel("Return")
    plt.plot(ms_in, label="Manual Strategy", color="red")
    plt.plot(sl_in, label="Strategy Learner", color="yellow")
    plt.plot(b_in, label=f"Benchmark", color="blue")
    plt.legend()
    fig = plt.gcf()
    fig.savefig("Exp1 Fig3 In Sample Strategies Comparison")

    plt.figure(figsize=(16, 8))
    plt.grid()
    plt.title("Out Sample Strategies Comparison")
    plt.xlim(out_sample_start_date, out_sample_end_date)
    plt.xlabel("Date")
    plt.ylabel("Return")
    plt.plot(ms_out, label="Manual Strategy", color="red")
    plt.plot(sl_out, label="Strategy Learner", color="yellow")
    plt.plot(b_out, label=f"Benchmark", color="blue")
    plt.legend()
    fig = plt.gcf()
    fig.savefig("Exp1 Fig4 Out Sample Strategies Comparison")


if __name__ == "__main__":
    print("---Experiment 1---")
    exp1()