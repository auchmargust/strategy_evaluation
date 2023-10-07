import datetime as dt
import os

import numpy as np
import pandas as pd
from util import get_data, plot_data
import ManualStrategy as ms
import StrategyLearner as sl
import matplotlib.pyplot as plt

class marketsimcode(object):
    def __init__(self,symbol, sd,ed,sv, impact, commission):
        self.symbol = symbol
        self.sd = sd
        self.ed = ed
        self.sv = sv
        self.impact = impact
        if commission is None:
            self.commission = 0
        else:
            self.commission = commission
    def author(self):
        return "jfeng89"  # Change this to your user ID

    def compute_portvals(self,
        order,
    ):
        syms = [self.symbol]
        start_date = self.sd
        end_date = self.ed

        # Construct price dataframe
        prices = get_data(syms, pd.date_range(start_date, end_date))
        prices = prices[syms] # remove SPY
        prices['Cash']=1.0
        prices = pd.DataFrame(prices,index = prices.index,columns=prices.columns)

        buy_prices=prices.copy()
        sell_prices = prices.copy()

        buy_prices = buy_prices[syms] * (1+self.impact)
        sell_prices = sell_prices[syms]*(1-self.impact)


        #Construct trade dataframe
        trades = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
        trades['Cash'] = 0
        for index, row in order.iterrows():
            trade_shares = row[syms].values[0]
            if trade_shares>0:
                price = buy_prices.loc[buy_prices.index == index, syms].values[0]
                cash_used = (-trade_shares)*price -self.commission
                trades.loc[trades.index == index,syms] += trade_shares
                trades.loc[trades.index == index, 'Cash'] += cash_used
            else:
                price = sell_prices.loc[sell_prices.index == index, syms].values[0]
                cash_used = (-trade_shares)*price -self.commission
                trades.loc[trades.index == index, syms] += trade_shares
                trades.loc[trades.index == index, 'Cash'] += cash_used


        #Construct holding dataframe
        holdings = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
        holdings.loc[trades.index[0],'Cash'] += self.sv
        holdings.loc[holdings.index>=start_date,:] += trades.loc[holdings.index>=start_date,:]
        for i in range(1, holdings.shape[0]):
            holdings.ix[i,:] = holdings.ix[i-1, :] + holdings.ix[i,:]

        #Construct values dataframe
        values = holdings*prices

        #Get portfolio values
        portvals = pd.DataFrame(index=values.index)
        portvals['Value']=values.sum(axis=1)
        return portvals

    def get_stats(self,portvals):
        if isinstance(portvals, pd.DataFrame):
            portvals = portvals[
                portvals.columns[0]]  # just get the first column
        else:
            "warning, code did not return a DataFrame"

        rfr = 0.0
        sf = 252.0
        daily_returns = (portvals / portvals.shift(1)) - 1
        daily_returns.iloc[0] = 0
        daily_returns = daily_returns[1:]

        cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [
            (portvals[-1] / portvals[0]) - 1,
            daily_returns.mean(),
            daily_returns.std(),
            (sf ** 0.5) * (daily_returns.mean() - rfr) / daily_returns.std(),
        ]
        return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio

    def get_graph(self,
            df_trades,graph_title,
    ):
        port_val = self.compute_portvals(
            order=df_trades
        )
        port_val = port_val[:] / port_val.iloc[0].values
        port_stat = self.get_stats(portvals=port_val)

        benchmark_order = pd.DataFrame(0, index=df_trades.index, columns=['JPM'])
        benchmark_order.loc[df_trades.index[0]] = 1000
        benchmark_val = self.compute_portvals(
            order=benchmark_order
        )
        benchmark_val = benchmark_val[:] / benchmark_val.iloc[0].values
        b_stat = self.get_stats(portvals=benchmark_val)

        # Get performance data
        comprison_table = pd.DataFrame([port_stat, b_stat],
                                       columns=['CR', 'ADR', 'STD', 'SR'],
                                       index=['Strategy', 'Benchmark']
                                       )

        fn = f'{graph_title} v.s Benchmark Performance Comparison.txt'
        with open(fn, 'a') as f:
            line = comprison_table.to_string(header=True, index=True)
            f.write(line)

        # Create graph
        fig, ax = plt.subplots(figsize=(16, 8))
        short_trades = df_trades[df_trades[self.symbol] < 0]
        long_trades = df_trades[df_trades[self.symbol] > 0]
        for trade in short_trades.index:
            ax.axvline(trade, color='black', )
        for trade in long_trades.index:
            ax.axvline(trade, color='blue', )
        ax.plot(port_val, label=f"{graph_title}", color='red')
        ax.plot(benchmark_val, label="Benchmark", color='purple')
        plt.xlabel("Date")
        plt.ylabel("Normalized Portfolio Value")
        plt.grid()
        plt.xlim(df_trades.index[0], df_trades.index[-1])
        plt.title(f"{graph_title} Return v.s. Benchmark Portfolio Return")
        ax.legend()
        return fig


if __name__ == "__main__":
    print("marketsim")


   



