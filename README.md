# Strategy Evaluation: Manual Strategy vs Strategy Learner

## Main Goal:

Implementd two strategies and compared their performance:

1. Manual Strategy
   Developed with widely-accepted trading indicators, including SMA, Bollinger Band Percentage, Stochastic Oscillator and Rate of Change Crosseovers.
2. Strategy Learner,
   Developed using machine learning algorithm. **Random Tree Learner** is used for this project.

## Environment Setup:

Install miniconda or anaconda (if it is not already installed).  
Create an environment for this class

```shell script
conda env create --file environment.yml
```

```shell script
conda activate ml4t
```

Use **Python 3.6** for this project

## Implementation:

1. For calculating financial indicators used to derive strategies: [indicators](https://github.com/auchmargust/strategy_evaluation/blob/5e3fbebbfc97391b2175dd6ed71ba29d45a8c169/indicators.py)
2. For transforming stock prices dataframes to holding positions, and calculating portfolio values: [marketsimcode](https://github.com/auchmargust/strategy_evaluation/blob/5e3fbebbfc97391b2175dd6ed71ba29d45a8c169/marketsimcode.py)
3. Manual Strategy formulation and implementation: [ManualStrategy](https://github.com/auchmargust/strategy_evaluation/blob/5e3fbebbfc97391b2175dd6ed71ba29d45a8c169/ManualStrategy.py)
4. Random Tree Learner implementation: [RTLearner](https://github.com/auchmargust/strategy_evaluation/blob/5e3fbebbfc97391b2175dd6ed71ba29d45a8c169/RTLearner.py)
5. Strategy Learner formulation, based on Random Tree: [StrategyLearner](https://github.com/auchmargust/strategy_evaluation/blob/5e3fbebbfc97391b2175dd6ed71ba29d45a8c169/StrategyLearner.py)
6. Comparison among Manual Strategy, Strategy Learner, and market benchmark during in and out sample period, including metrics and visualization generation: [Experiment1](https://github.com/auchmargust/strategy_evaluation/blob/5e3fbebbfc97391b2175dd6ed71ba29d45a8c169/experiment1.py)
7. Explore how variations of commission and market impact would affect strategy performances: [Experiment2](https://github.com/auchmargust/strategy_evaluation/blob/5e3fbebbfc97391b2175dd6ed71ba29d45a8c169/experiment2.py)
8. For running the whole project: [testproject](https://github.com/auchmargust/strategy_evaluation/blob/5e3fbebbfc97391b2175dd6ed71ba29d45a8c169/testproject.py)

### Manual Strategy

Price/SMA, B%, and Stochastic Oscillator were used to indicate overbought/sold.

Long when the stock demonstrates oversold signal.Sell when the stock demonstrates overbought signal.


### Strategy Learner

Implemented against Random Tree learner, with leaf size = 5.

X_training: 3 indicators as those used by Manual Strategy and 2 crossover indicators concatenated together during the In-Sample period. Training data has been converted as classification method (-1/+1/0)

Y_training: A dataframe of values +1/-1/0 representing the ideal holding the learner should take at the date based on the future N day return. 

## Performance Analysis

The purple line represented the benchnmark where a portfolio started with $100,000 cash and investing in 1,000 shares of selecteed symbol (JPM stock) on the first trading day and holding that position untill the end of the period. 

The blue and black lines represented LONG and SHORT trades conducted by the manual strategy.

### Manual Strategy Performance Evaluation

![alt text](https://github.com/auchmargust/strategy_evaluation/blob/7a7889b70cc6457a5bac61a225a6ae3368d7756e/Exp1Fig1InSampleManualStrategyvsBenchmark.png)
![alt text](https://github.com/auchmargust/strategy_evaluation/blob/7a7889b70cc6457a5bac61a225a6ae3368d7756e/Exp1Fig2OutSampleManualStrategyvsBenchmark.png)

| Name | CR | ADR | STD | SR
| -----|-----|-- | ------|-------
| Manual Strategy| 0.2536 | 0.000526 | 0.012502|0.668302
| Benchmark | 0.0123 | 0.000168 | 0.017004 | 0.156918

**Conclusion**

In Sample Manual Strategy has substantially outperformed the benchmark: its CR (cumulative return) is almost **21x** benchmark CR and also has a higher Sharpe Ratio.
During Out Sample Period, Manual Strategy still makes profits whereas benchmark is losing money.

Factors that could lead to differences between in and out sample performances include the general financial market environment fluctuations: The phoneomenal global recession started in 2008 during  in-sample period, and as a U.S. bank, JPM is one of the companies impacted the most. Therefore, the company, the industry and the whole financial market may have completely different performances during Out Sample period, in which the indicators selected might now work ideally as hypothesized.
In addition,from Efficient Market Theory, technical analysis can only make money when market is inefficient. In real-life, it is clearly impossible to purely rely on technical indicators to make trading decisions and expect the strategy to make profits consistently.

### Strategy Learner vs Manual Strategy Performance Evaluation

![alt text](https://github.com/auchmargust/strategy_evaluation/blob/297a7c20c840227c975822a337c528f895923327/Exp1Fig3InSampleStrategiesComparison.png)
![alt text](https://github.com/auchmargust/strategy_evaluation/blob/297a7c20c840227c975822a337c528f895923327/Exp1Fig4OutSampleStrategiesComparison.png)

**Conclusion**

Strategy Learner has outperformed than benchmark and manual strategy for in-sample period and out-sample period. Strategy Learner has reached the cumulative return over 50% for in-sample period. The result for in-sample period are expected because we trained the learner using in-sample data, which means trades made during in-sample period are ideal trades to generate desired returns. Therefore they should generate higher return than the benchmark and generally the manual strategy. For out-sample period, it is not definite that Strategy Learner will always outperform.

## Impact Analysis

![alt text](https://github.com/auchmargust/strategy_evaluation/blob/297a7c20c840227c975822a337c528f895923327/Exp2Fig1StrategyReturn.png)
![alt text](https://github.com/auchmargust/strategy_evaluation/blob/297a7c20c840227c975822a337c528f895923327/Exp2Fig2NumofTrades.png)

Market impact is defined to be the amount the price moves against the trader data at each transaction. The price would increase by the impact when buying and decrease by the impact when selling. Hypothetically, a higher impact value would lower the volume traded and negtaively affect the trading strategy performance.

