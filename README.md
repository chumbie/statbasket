[![Github All Releases](https://img.shields.io/badge/creator-John%20Weldon-green)]()
[![Github All Releases](https://img.shields.io/github/languages/code-size/chumbie/statbasket)]()
[![Github All Releases](https://img.shields.io/tokei/lines/github/chumbie/statbasket)]()
[![Github All Releases](https://img.shields.io/badge/PRs-welcome-yellow)]()


[comment]: <> ([![Github All Releases]&#40;https://img.shields.io/github/downloads/chumbie/statbasket/total&#41;]&#40;&#41;)

# Stat Basket
Stat Basket is a small statistics package intended for use with student 
projects or small datasets (those containing <1 million data points). 
It is implemented with pure python, so no external dependencies are 
required.
## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 
stat-basket.
```bash
pip install statbasket
```
## Usage
The statbasket package includes two classes, *StatBasket* and *StatMe*.
### StatBasket
Using the *StatBasket* class generates all statistical data on initialization,
and individual statistics can be accessed via the StatBasket object attributes:
```python
from statbasket import StatBasket

data = (13, 26, 41, 35, 12)
# Perform all calculations and store in attributes
basket = StatBasket(data, first_data_name="my_data")

print(basket.n)
print(basket.mean)
```
**Output:**
```
5
25.4
```
A string summary of the statistics can be generated using the 
describe() method:
```python
print(basket.describe())
```
**Output:**
```

________________________________________________
|==============================================|
|           DESCRIPTION OF my_data             |
|==============================================|
|----------General Sample Statistics-----------|
|==============================================|
|      Size of Sample (n)             5        |
|     Minimum Value (min)             12       |
|     Maximum Value (max)             41       |
|==============================================|
|---------Measures of Central Tendency---------|
|==============================================|
|         Mean (mean)                25.4      |
|       Median (median)              26.0      |
|         Mode (mode)             multimodal   |
|            Range                   29.0      |
|       Skewness (skew)             0.034      |
|==============================================|
|------------Measures of Variation-------------|
|==============================================|
|        Variance (var)             167.3      |
|  Standard Deviation (stdev)       12.934     |
|    Standard Error (sterr)         5.784      |
|  Coeff. of Variation (cov)        0.509      |
|==============================================|
|--------Confidence Interval Statistics--------|
|==============================================|
|    Confidence Level (cl)           0.95      |
|      alpha, two-tailed            0.025      |
|   t-score (score_critical)        2.776      |
|    Margin of Error (moe)          16.058     |
| CI (mean - moe, mean + moe)  [9.342, 41.458] |
------------------------------------------------
```
### StatMe
Alternatively, if you want to perform calculations on-the-fly, without 
performing the entire batch of calculations at once, you can use the 
*StatMe* class of methods:
```python
from statbasket import StatMe

data = (13, 26, 41, 35, 12)
# Perform single operations on data
mean = StatMe.get_mean(data)
ci = StatMe.get_ci(data, cl=0.99)

print(mean)
print(ci)
```
**Output:**
```
25.4
(-1.2316627975047787, 52.03166279750478)
```
View the individual class docstrings for a full list of available attributes and methods:
```python
from statbasket import StatMe, StatBasket
help(StatMe)
help(StatBasket)
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.
## License
[MIT](https://choosealicense.com/licenses/mit/)