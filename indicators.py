""""""

"""MC2-P1: Market simulator.  		  	   		  	  		  		  		    	 		 		   		 		  

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

Student Name: Jingya Feng (replace with your name)  		  	   		  	  		  		  		    	 		 		   		 		  
GT User ID: jfeng89 (replace with your User ID)  		  	   		  	  		  		  		    	 		 		   		 		  
GT ID: 903450072 (replace with your GT ID)  		  	   		  	  		  		  		    	 		 		   		 		  
"""

import datetime as dt
import os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from util import get_data, plot_data


def author():
    return "jfeng89"  # Change this to your user ID

def get_sma(start_date,end_date,syms,period):
    price = get_data(syms, pd.date_range(start_date - dt.timedelta(days=period * 2), end_date))
    normed_price = price / price.iloc[0].values
    # normed_price = normed_price.loc[start_date:,:]
    sma = normed_price.rolling(window=period, min_periods=period).mean()

    price = price.loc[start_date:,:]
    price = price / price.iloc[0].values
    sma = sma.loc[start_date:,:]
    price_sma = normed_price / sma

    return price_sma

def get_bb(start_date,end_date,syms,period):
    price = get_data(syms, pd.date_range(start_date- dt.timedelta(days=period * 2), end_date))
    sma = price.rolling(window=period, min_periods=period).mean()
    rolling_std = price.rolling(window=period, min_periods=period).std()

    top_band = sma + (2 * rolling_std)
    bottom_band = sma - (2 * rolling_std)
    bbp = (price - bottom_band) / (top_band - bottom_band)

    return top_band,bottom_band,bbp

def get_roc(start_date, end_date, syms, period):
    price = get_data(syms, pd.date_range(start_date - dt.timedelta(days=period * 2), end_date))
    normed_price = price / price.iloc[0].values
    roc = normed_price.pct_change(periods=period)
    roc = roc.loc[start_date:, :]
    return roc

def get_sto(start_date, end_date, syms):
    adj_close_price = get_data(syms, pd.date_range(start_date - dt.timedelta(30), end_date))
    close_price = get_data(syms, pd.date_range(start_date - dt.timedelta(30), end_date),colname="Close")
    adj_ratio = adj_close_price/close_price

    highest = get_data(syms, pd.date_range(start_date - dt.timedelta(30), end_date),colname="High")
    lowest = get_data(syms, pd.date_range(start_date - dt.timedelta(30), end_date),colname="Low")

    adj_highest = highest[syms]*adj_ratio[syms]
    adj_lowest = lowest[syms]*adj_ratio[syms]


    adj_highest = adj_highest.rolling(window=14, min_periods=14).max()
    adj_lowest = adj_lowest.rolling(window=14, min_periods=14).min()

    sto = (adj_close_price-adj_lowest)/(adj_highest-adj_lowest)*100
    sto = sto.loc[start_date:, :]
    return sto


def get_cci(start_date, end_date, syms, period):
    adj_close_price = get_data(syms, pd.date_range(start_date - dt.timedelta(period*2), end_date))
    close_price = get_data(syms, pd.date_range(start_date - dt.timedelta(period*2), end_date),colname="Close")
    adj_ratio = adj_close_price/close_price

    highest = get_data(syms, pd.date_range(start_date - dt.timedelta(period*2), end_date),colname="High")
    lowest = get_data(syms, pd.date_range(start_date - dt.timedelta(period*2), end_date),colname="Low")
    adj_highest = highest[syms]*adj_ratio[syms]
    adj_lowest = lowest[syms]*adj_ratio[syms]

    typical_price = (adj_highest+adj_lowest+adj_close_price)/3
    ma = typical_price.rolling(window=period, min_periods=period).mean()
    mad = typical_price.rolling(period).apply(lambda x: pd.Series(x).mad(),raw=True)
    cci = (typical_price-ma)/(0.015*mad)
    cci = cci.loc[start_date:, :]


    return cci


if __name__ == "__main__":
    print("indicators")


