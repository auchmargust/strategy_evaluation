import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from util import get_data, plot_data
import indicators as ind
import marketsimcode as mkt

def author():

    return "jfeng89"

# Use SMA & BBP & ROC

def testPolicy(
        symbol,sd,ed,sv=100000
):
    lookback = 20
    order_size = 1000
    symbol = [symbol]
    sma=ind.get_sma(start_date=sd,end_date=ed,syms=symbol,period = lookback)
    sma_cross = pd.DataFrame(0,index = sma.index,columns=sma.columns)
    sma_cross[sma>=1]=1
    sma_cross[1:]=sma_cross.diff()
    sma_cross.ix[0]=0

    top_band,bottom_band,bbp = ind.get_bb(start_date=sd,end_date=ed,syms=symbol,period = lookback,)

    roc = ind.get_roc(start_date=sd,end_date=ed,syms=symbol,period = lookback,)
    sto = ind.get_sto(start_date=sd,end_date=ed,syms=symbol,)

    roc_cross = pd.DataFrame(0,index = roc.index,columns=roc.columns)
    roc_cross[roc>=0]=1
    roc_cross[1:] = roc_cross.diff()
    roc_cross.iloc[0] = 0

    # Construct order dataframe
    orders = sma.copy()
    orders.iloc[:, :] = np.nan

    buy = ((sma[symbol]<0.95) & (bbp[symbol]<0)) & (sto[symbol]<20)
    sell = ((sma[symbol] > 1.05) & (bbp[symbol] > 1)) & (sto[symbol] > 80)
    cross = (sma_cross[symbol] != 0) & (roc_cross[symbol] != 0)

    sell_index = np.where(sell == True)[0]
    buy_index = np.where(buy == True)[0]
    cross_index = np.where(cross == True)[0]
    orders.iloc[sell_index,1] = -1
    orders.iloc[buy_index, 1] = 1
    orders.iloc[cross_index, 1] = 0.0

    # Based on orders dataframe, construct trade dataframes
    del orders['SPY']
    df_trades = orders.copy()
    df_trades = df_trades.loc[sd:,]
    df_trades.ffill(inplace=True)
    df_trades.fillna(0,inplace=True)
    df_trades[1:]=df_trades.diff()
    df_trades.iloc[0]=0
    df_trades = df_trades*order_size
    # df_trades = df_trades.loc[(orders != 0).any(axis=1)]

    return df_trades

def get_graphs():
    in_sample_start_date = dt.datetime(2008, 1, 1)
    in_sample_end_date = dt.datetime(2009, 12, 31)
    out_sample_start_date = dt.datetime(2010, 1, 1)
    out_sample_end_date = dt.datetime(2011, 12, 31)
    starting_val = 100000
    impact = 0.0
    commission = 0.0

    mkt_sim_in = mkt.marketsimcode(symbol="JPM", sd=in_sample_start_date, ed=in_sample_end_date, sv=starting_val,
                                   commission=commission, impact=impact)
    mkt_sim_out = mkt.marketsimcode(symbol="JPM", sd=out_sample_start_date, ed=out_sample_end_date, sv=starting_val,
                                    commission=commission, impact=impact)

    orders_in = testPolicy(symbol="JPM", sd=in_sample_start_date, ed=in_sample_end_date,
                           sv=starting_val)
    manual_strategy_in = mkt_sim_in.get_graph(df_trades=orders_in, graph_title="In Sample Manual Strategy", )
    manual_strategy_in.savefig("Exp1 Fig1 In Sample Manual Strategy vs Benchmark")

    orders_out = testPolicy(symbol="JPM", sd=out_sample_start_date, ed=out_sample_end_date,
                            sv=starting_val)
    manual_strategy_out = mkt_sim_out.get_graph(df_trades=orders_out, graph_title="Out Sample Manual Strategy")
    manual_strategy_out.savefig("Exp1 Fig2 Out Sample Manual Strategy vs Benchmark")

if __name__ == "__main__":
    print("manual strategy.")





