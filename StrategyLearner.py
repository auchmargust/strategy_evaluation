""""""  		  	   		  	  		  		  		    	 		 		   		 		  
"""  		  	   		  	  		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  	  		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  	  		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  	  		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  	  		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  	  		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  	  		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  	  		  		  		    	 		 		   		 		  
or edited.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  	  		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  	  		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  	  		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
Student Name: Jingya Feng(replace with your name)  		  	   		  	  		  		  		    	 		 		   		 		  
GT User ID: jfeng89 (replace with your User ID)  		  	   		  	  		  		  		    	 		 		   		 		  
GT ID:  (replace with your GT ID)  		  	   		  	  		  		  		    	 		 		   		 		  
"""  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		  	  		  		  		    	 		 		   		 		  
import random  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		  	  		  		  		    	 		 		   		 		  
import util as ut
import RTLearner as rt
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from util import get_data, plot_data
import indicators as ind
import marketsimcode as mkt
  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  	  		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output.  		  	   		  	  		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		  	  		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		  	  		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		  	  		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		  	  		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    # constructor  		  	   		  	  		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.0, commission=0.0,):
        """  		  	   		  	  		  		  		    	 		 		   		 		  
        Constructor method  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		  	  		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		  	  		  		  		    	 		 		   		 		  
        self.commission = commission
        self.learner = rt.RTLearner(leaf_size=5)
        # N day return
        self.N = 1
        # N day return% for buy
        self.YBUY = self.impact*5
        # N day return% for sell
        self.YSELL =self.impact*5

  	# Helper method to get indicators as Xtrain and Xtest
    def get_indicators(
                self,
                symbol,
                sd,
                ed,
                lookback
    ):
        syms = [symbol]
        sma = ind.get_sma(start_date=sd, end_date=ed, syms=syms, period=lookback,)
        sma_cross = pd.DataFrame(0, index=sma.index, columns=sma.columns)
        sma_cross[sma >= 1] = 1
        sma_cross[1:] = sma_cross.diff()
        sma_cross.ix[0] = 0
        top_band, bottom_band, bbp = ind.get_bb(start_date=sd, end_date=ed, syms=syms, period=lookback,
                                                )
        roc = ind.get_roc(start_date=sd, end_date=ed, syms=syms, period=lookback, )
        sto = ind.get_sto(start_date=sd, end_date=ed, syms=syms, )
        # cci = ind.get_cci(start_date=sd, end_date=ed, syms=syms, period=lookback, debug=False)
        roc_cross = pd.DataFrame(0, index=roc.index, columns=roc.columns)

        indicators = pd.concat((sma[syms].loc[sd:, ]
                                     ,bbp[syms].loc[sd:, ],
                                     sto[syms].loc[sd:, ],
                                     sma_cross[syms].loc[sd:, ],
                                     roc_cross[syms].loc[sd:, ]),axis=1,keys=['SMA','BBP','STO','SMA_X','ROC_X'])

        return indicators


    # this method should create a QLearner, and train it for trading  		  	   		  	  		  		  		    	 		 		   		 		  
    def add_evidence(  		  	   		  	  		  		  		    	 		 		   		 		  
        self,  		  	   		  	  		  		  		    	 		 		   		 		  
        symbol,
        sd,
        ed,
        sv=10000,  		  	   		  	  		  		  		    	 		 		   		 		  
    ):  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
        Trains your strategy learner over a given time frame.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol to train on  		  	   		  	  		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		  	  		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  	  		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		  	  		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  	  		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		  	  		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		  	  		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		  	  		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
        # add your code to do learning here  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
        # Get Prices

        syms = [symbol]  		  	   		  	  		  		  		    	 		 		   		 		  
        dates = pd.date_range(sd, ed)

        # Get X values:  indicators: sma, sma_cross, bollinger band, rate of change cross and stochastic oscillator
        indicators = self.get_indicators(symbol=symbol,
                sd=sd,
                ed=ed,
                lookback = 20
                )


        prices = get_data(syms, dates)
        prices = pd.DataFrame(prices, index=prices.index, columns=prices.columns)
        prices = prices[syms]  # only portfolio symbols

        if self.impact == 0.0 or self.impact == None:
            # Get Y values: classify LONG, SHORT or CASH based on future returns
            daily_rets = prices.copy()
            # Calculate returns based on future data
            daily_rets = daily_rets.diff(periods=self.N) / daily_rets
            daily_rets = daily_rets.shift(-self.N)
        else:
            buy_prices = prices.copy()
            sell_prices = prices.copy()
            buy_prices = buy_prices[syms] * (1 + self.impact)
            sell_prices = sell_prices[syms] * (1 - self.impact)

            daily_returns_buy = buy_prices.copy()
            daily_returns_buy.values[self.N:,:] =  (sell_prices.values[self.N:,]-buy_prices.values[:-self.N,:])
            daily_returns_buy = daily_returns_buy.shift(-self.N)

            daily_returns_sell = sell_prices.copy()
            daily_returns_sell.values[self.N:,:] = (buy_prices.values[self.N:,]-sell_prices.values[:-self.N,:])
            daily_returns_sell = daily_returns_sell.shift(-self.N)

            daily_rets = daily_returns_buy + daily_returns_sell
            daily_rets = daily_rets/prices

        # Construct order: long when next day's price goes up (daily return >0) and short when next day's price goes down(daily return <0)
        orders = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
        orders[daily_rets[syms]>self.YBUY] = 1
        orders[daily_rets[syms] < self.YSELL] = -1
        orders = orders.loc[sd:, ]

        self.learner.add_evidence(data_x=indicators,data_y=orders[syms])


    # this method should use the existing policy and test it against new data  		  	   		  	  		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		  	  		  		  		    	 		 		   		 		  
        self,  		  	   		  	  		  		  		    	 		 		   		 		  
        symbol,
        sd,
        ed,
        sv=10000,  		  	   		  	  		  		  		    	 		 		   		 		  
    ):  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
        Tests your learner using data outside of the training data  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol that you trained on on  		  	   		  	  		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		  	  		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  	  		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		  	  		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  	  		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		  	  		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		  	  		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		  	  		  		  		    	 		 		   		 		  
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		  	  		  		  		    	 		 		   		 		  
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		  	  		  		  		    	 		 		   		 		  
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		  	  		  		  		    	 		 		   		 		  
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		  	  		  		  		    	 		 		   		 		  
        :rtype: pandas.DataFrame  		  	   		  	  		  		  		    	 		 		   		 		  
        """
        order_size = 1000
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices = get_data(syms, dates)
        prices = pd.DataFrame(prices, index=prices.index, columns=prices.columns)
        prices = prices[syms]

        # Getting indicators as test data...
        Xtest = self.get_indicators(symbol=symbol,
                                sd=sd,
                                ed=ed,
                                lookback=20
                                )
        Xtest = Xtest.loc[sd:, ]

        #Getting orders through learnng...
        order_learned = self.learner.query(Xtest=Xtest)

        #Getting trades dataframes from orders data frame
        df_trades = order_learned.copy()
        df_trades = pd.DataFrame(df_trades,index=prices.index,columns=[syms])
        df_trades.ffill(inplace=True)
        df_trades.fillna(0, inplace=True)
        df_trades[1:] = df_trades.diff()
        df_trades = df_trades*order_size

        return df_trades
  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		  	  		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")
    learner = StrategyLearner(verbose = False, impact = 0.005, commission=0.0)
    learner.add_evidence(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
    df_trades = learner.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)


    '''Test for ML4T-220'''
    in_sample_start_date = dt.datetime(2008, 1, 1)
    in_sample_end_date = dt.datetime(2009, 12, 31)
    out_sample_start_date = dt.datetime(2010, 1, 1)
    out_sample_end_date = dt.datetime(2011, 12, 31)
    starting_val = 100000
    # order_size = 1000
    impact = 0.0
    commission = 0.0
    np.random.seed(903450072)
    random.seed(903450072)
    # Setting up different market simulations for in & out sample
    mkt_sim_in = mkt.marketsimcode(symbol="JPM", sd=in_sample_start_date, ed=in_sample_end_date, sv=starting_val,
                                   commission=commission, impact=impact)
    result = mkt_sim_in.compute_portvals(order=df_trades)
    result = result[:] / result.iloc[0].values
    prices = get_data(["JPM"], pd.date_range(in_sample_start_date,in_sample_end_date))
    prices = prices["JPM"]
    prices = prices/prices[0]

    # Plots
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(result, label="Strategy Learner", color="red")
    ax.plot(prices, label="Prices", color="yellow")
    plt.grid()
    plt.title("In Sample Strategies Comparison")
    plt.xlim(in_sample_start_date, in_sample_end_date)
    plt.xlabel("Date")
    plt.ylabel("Return")
    plt.grid()
    plt.show()
    print("...")
