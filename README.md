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

## Strategy Construction Rationale

### Manual Strategy:
Price/SMA, B%, and Stochastic Oscillator were used to indicate overbought/sold.

Long when the stock demonstrates oversold signal.Sell when the stock demonstrates overbought signal.


### Strategy Learner:
Implemented against Random Tree learner, with leaf size = 5.

X_training: 3 indicators as those used by Manual Strategy and 2 crossover indicators concatenated together during the In-Sample period

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

**In conclusion:**
In Sample Manual Strategy has substantially outperformed the benchmark: its CR (cumulative return) is almost **21x** benchmark CR and also has a higher Sharpe Ratio.
During Out Sample Period, Manual Strategy still makes profits whereas benchmark is losing money.
