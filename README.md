# Strategy Evaluation: Manual Strategy vs Strategy Learner

## Main Goal:

Implementd two strategies and compared their performance:

1. Manual Strategy
   Developed with widely-accepted trading indicators, including SMA, Bollinger Band Percentage, Stochastic Oscillator and Rate of Change Crosseovers.
2. strategy learner,
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

## Use **Python 3.6** for this project

## Strategy Construction

### Manual Strategy:

Long when the stock demonstrates oversold signal, and to sell when the stock demonstrates overbought signal.
Price/SMA, B%, and Stochastic Oscillator were used to indicate overbought/sold.

### Strategy Learner:

---

## Performance Analysis

For charts in this section, the purple line represented the benchnmark where a portfolio started with $100,000 cash and investing in 1,000 shares of selecteed symbol (JPM stock) on the first trading day and holding that position untill the end of the period. The blue and black lines represented LONG and SHORT trades conducted by the manual strategy.

### Manual Strategy Performance Evaluation

[image](Exp1 Fig1 In Sample Manual Strategy vs Benchmark.png "Fig1")
[image](Exp1 Fig2 Out Sample Manual Strategy vs Benchmark.png "Fig2")

| Name | CR | ADR | STD | SR
| Manual Strategy| 0.2536 | 0.000526 | 0.012502|0.668302
| Benchmark | 0.0123 | 0.000168 | 0.017004 | 0.156918

In Sample Manual Stragtegy has substantially outperfromed the benchmark: its Cumulative Return is almost 21x benchmark CR and also has a higher Sharpe Ratio.
During Out Sample Period, Manual Strategy still makes profits whereas benchmark is losing money.
